from operator import call
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

from libs import langfuse_handler

# 初始化聊天模型，需替换为你的 API 地址和密钥
# 若使用本地兼容 OpenAI API 的模型，修改 base_url
chat = ChatOpenAI(
    model="Qwen/Qwen2.5-72B-Instruct",
    openai_api_base="https://api.siliconflow.cn/v1",
    openai_api_key="sk-nsswwpfvuompvcqcseqsfbhjysigfiiybqyeznikustuhucq",
    temperature=0
)

def main():
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'q':
            break
        # 构建人类消息
        messages = [HumanMessage(content=user_input)]
        # 获取模型回复
        response = chat(messages, callbacks=[langfuse_handler])
        print(f"机器人: {response.content}")

if __name__ == "__main__":
    main()
