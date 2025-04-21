import ollama
import sys

# 新增颜色控制方法
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
    # 初始化聊天历史
    messages = []
    
    # 修改为带颜色的欢迎信息
    print(colored("欢迎使用Qwen2.5-14b聊天助手！", 'green') + colored("输入'退出'结束对话。", 'yellow'))
    
    while True:
        # 修改用户输入提示为蓝色
        user_input = input(colored("你: ", 'blue'))
        
        # 检查是否退出
        if user_input.lower() == '退出':
            print(colored("对话结束，再见！", 'magenta'))
            break
            
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = ollama.chat(
                model='qwen2.5:14b',
                messages=messages
            )
            
            # 修改助手回复为青色
            assistant_reply = response['message']['content']
            print(colored("助手:", 'cyan'), assistant_reply)
            
            messages.append({"role": "assistant", "content": assistant_reply})
            
        except Exception as e:
            print(colored(f"发生错误: {e}", 'red'))
            break

if __name__ == "__main__":
    chat_with_qwen()
