from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langfuse.callback import CallbackHandler

load_dotenv()
langfuse_handler = CallbackHandler()

# 使用最新LangChain API初始化聊天模型
chat = ChatOpenAI(
    model="Qwen/Qwen2.5-72B-Instruct",
    base_url="https://api.siliconflow.cn/v1",
    api_key="sk-nsswwpfvuompvcqcseqsfbhjysigfiiybqyeznikustuhucq",
    temperature=0
)

def main():
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'q':
            break
        
        # 使用最新API调用方式
        response = chat.invoke([HumanMessage(content=user_input)], 
                             config={"callbacks": [langfuse_handler]})
        print(f"机器人: {response.content}")

if __name__ == "__main__":
    main()
