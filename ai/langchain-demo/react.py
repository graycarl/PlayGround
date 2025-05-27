from dotenv import load_dotenv
from langfuse.callback import CallbackHandler
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import BaseTool
from langchain.schema import HumanMessage
from langgraph.prebuilt import create_react_agent
from langfuse.decorators import langfuse_context, observe

load_dotenv()

# 创建安全的数学计算工具
class SafeMathTool(BaseTool):
    name: str = "Calculator"
    description: str = "适用于解决数学问题，当你需要进行数学计算时使用这个工具。" \
                       "请注意工具的底层使用 linux 的 bc 工具进行计算，" \
                       "所以请确保输入的表达式是 bc 兼容的数学表达式。"

    def _run(self, expression: str) -> str:
        import subprocess
        try:
            # 使用bc计算，-l参数加载数学库
            process = subprocess.Popen(['bc', '-l'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            stdout, stderr = process.communicate(input=expression + '\n')
            if stderr:
                return f"计算错误: {stderr.strip()}"
            return stdout.strip()
        except Exception as e:
            return f"计算错误: {str(e)}"

llm_math = SafeMathTool()
tools = [llm_math]

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3",
    # model="Qwen/Qwen2.5-72B-Instruct",
    openai_api_base="https://api.siliconflow.cn/v1",
    openai_api_key="sk-nsswwpfvuompvcqcseqsfbhjysigfiiybqyeznikustuhucq",
    temperature=0,
    streaming=False
)

agent = create_react_agent(llm, tools)

@observe
def chatbot_response(user_input):
    langfuse_handler = langfuse_context.get_current_langchain_handler()
    # 构建人类消息
    messages = [HumanMessage(content=user_input)]
    # 获取模型回复
    # response = agent.invoke(dict(messages=messages))
    response = agent.invoke(dict(messages=messages), config={"callbacks": [langfuse_handler]})
    return response["messages"][-1].content

def main():
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'q':
            break
        response = chatbot_response(user_input)
        print(f"机器人: {response}")


if __name__ == "__main__":
    main()
