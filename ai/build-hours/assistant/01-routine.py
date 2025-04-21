import ollama
import sys

def colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"

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
    
    print(colored("欢迎使用ACME客服助手！", 'green') + colored("输入'退出'结束对话。", 'yellow'))
    
    while True:
        user_input = input(colored("客户: ", 'blue'))
        
        if user_input.lower() == '退出':
            print(colored("对话结束，再见！", 'magenta'))
            break
            
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = ollama.chat(
                model='qwen2.5:14b',
                messages=messages
            )
            
            assistant_reply = response['message']['content']
            print(colored("客服:", 'cyan'), assistant_reply)
            
            messages.append({"role": "assistant", "content": assistant_reply})
            
        except Exception as e:
            print(colored(f"发生错误: {e}", 'red'))
            break

if __name__ == "__main__":
    chat_with_qwen()