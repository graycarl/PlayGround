import ollama
import sys
from utils import colored, function_to_schema  # 新增导入

def look_up_item(search_query):
    """Use to find item ID.
    Search query can be a description or keywords."""
    item_id = "item_132612938"
    print(colored("Found item:", "green"), item_id)
    return item_id


def execute_refund(item_id, reason="not provided"):
    print(colored("\n\n=== Refund Summary ===", "green"))
    print(colored(f"Item ID: {item_id}", "green"))
    print(colored(f"Reason: {reason}", "green"))
    print("=================\n")
    print(colored("Refund execution successful!", "green"))
    return "success"
    

tools = [look_up_item, execute_refund]

def chat_with_qwen():
    # 初始化聊天历史，添加系统提示词
    messages = [
        {
            "role": "system",
            "content": (
                "You are a customer support agent for ACME Inc.\n"
                "Always answer in a sentence or less.\n"
                "Follow the following routine with the user:\n"
                "1. First, ask probing questions and understand the user's problem deeper.\n"
                " - unless the user has already provided a reason.\n"
                "2. Propose a fix (make one up).\n"
                "3. ONLY if not satisfied, offer a refund.\n"
                "4. If accepted, search for the ID and then execute refund."
            )
        }
    ]
    
    print(colored("欢迎使用ACME客服助手！", 'green'))
    
    while True:
        try:
            user_input = input(colored("客户: ", 'blue'))
        except EOFError:
            print(colored("\n对话中断，再见！",'magenta'))
            break
        
        tool_schemas = [function_to_schema(func) for func in tools]
        messages.append({"role": "user", "content": user_input})
        response = ollama.chat(model='qwen2.5:14b', messages=messages, tools=tool_schemas)
        messages.append(response['message'])

        if response['message'].get('tool_calls'):
            tool_calls = response['message']['tool_calls']
            for tool_call in tool_calls:
                tool_output = run_tool_call(tool_call)
                messages.append({
                    "role": "tool",
                    "name": tool_call['function']['name'],
                    "content": tool_output
                })
        assistant_reply = response['message']['content']
        if assistant_reply:
            print(colored("客服:", 'cyan'), assistant_reply)


def run_tool_call(tool_call):
    tool_map = {func.__name__: func for func in tools}
    function_name = tool_call['function']['name']
    function_args = tool_call['function']['arguments']
    print(f"执行函数: {function_name}")
    print(f"参数: {function_args}")
    tool = tool_map.get(function_name)
    if tool:
        return tool(**function_args)
    else:
        return f"Error: 找不到函数 {function_name}"

if __name__ == "__main__":
    chat_with_qwen()