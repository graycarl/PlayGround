import asyncio
from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

# 1. 定义状态
class MyState(TypedDict):
    messages: Annotated[list, operator.add]
    step: int

# 2. 定义图节点
def node_a(state: MyState):
    print("--- 正在执行 [Node A] ---")
    new_messages = state["messages"] + ["消息来自 Node A"]
    return {"messages": new_messages, "step": state["step"] + 1}

def node_b_fails(state: MyState):
    print("--- 正在执行 [Node B] (即将失败) ---")
    # 模拟一个在处理过程中发生的灾难性故障
    raise ValueError("一个预料之中的失败！")

# 3. 构建图
builder = StateGraph(MyState)
builder.add_node("node_a", node_a)
builder.add_node("node_b_fails", node_b_fails)
builder.set_entry_point("node_a")
builder.add_edge("node_a", "node_b_fails")
builder.add_edge("node_b_fails", END)

# 4. 设置 Checkpointer (必须)
# 我们使用内存中的 aiosqlite，你也可以换成文件 ("checkpoints.sqlite")
memory_saver = InMemorySaver()
app = builder.compile(checkpointer=memory_saver)

# 5. 定义回滚逻辑
async def run_with_rollback(config):
    # 定义线程 ID
    thread_id = config["configurable"]["thread_id"]

    # [关键步骤 1]：在调用 astream 之前，获取当前状态快照
    print(f"\n[Thread: {thread_id}] 正在获取调用前的状态快照...")
    snapshot_before = await app.aget_state(config)

    # 如果有快照，提取其 'values'，否则使用空字典
    state_before_values = snapshot_before.values if snapshot_before.values else {'messages': [], 'step': 0}
    print(f"[Thread: {thread_id}] 调用前状态: {state_before_values}")

    try:
        print(f"[Thread: {thread_id}] 尝试调用 astream...")
        # [关键步骤 2]：在 try 块中执行 astream
        async for event in app.astream(
            {"messages": ["初始消息"], "step": 0},
            config=config
        ):
            print(f"Stream event: {event.get('data')}")
            pass

    except Exception as e:
        print(f"\n[Thread: {thread_id}] 捕获到异常: {e}")
        print("!!! 开始回滚 !!!")

        # [关键步骤 3]：如果发生异常，使用旧的状态值恢复（覆盖）检查点
        # aupdate_state 会覆盖掉 node_a 留下的部分完成的状态
        await app.aupdate_state(config, state_before_values)

        print(f"[Thread: {thread_id}] 状态已回滚。")

    finally:
        # 验证状态
        print(f"\n[Thread: {thread_id}] 检查最终状态...")
        final_state = await app.aget_state(config)
        print(f"[Thread: {thread_id}] 最终持久化状态: {final_state.values if final_state else '{}'}")


async def main():
    # 场景 1: 第一次运行 (状态为空)
    config_1 = {"configurable": {"thread_id": "thread-1"}}
    await run_with_rollback(config_1)
    # 预期结果：thread-1 的最终状态应该回滚到 {} (空)

    print("\n" + "="*30 + "\n")

    # 场景 2: 已有状态的运行
    config_2 = {"configurable": {"thread_id": "thread-2"}}

    # 先成功运行一次，建立一个 "上次成功" 的状态
    print("[Thread: 2] 首先设置一个初始状态 (运行 node_a 并停止)")
    await app.ainvoke({"messages": ["T2 初始"], "step": 10}, config_2, interrupt_after="node_a")
    initial_state_t2 = await app.aget_state(config_2)
    print(f"[Thread: 2] 设置完毕，当前状态: {initial_state_t2.values}")

    # 现在运行带回滚逻辑的 astream
    await run_with_rollback(config_2)
    # 预期结果：thread-2 的最终状态应该回滚到 T2 初始的状态，
    # 而不是 node_a (第二次运行) 之后、node_b_fails 之前的状态。

if __name__ == "__main__":
    asyncio.run(main())
