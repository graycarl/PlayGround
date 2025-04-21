from langchain.agents import initialize_agent, Tool
from langchain_community.llms import OpenAI
from langchain_community.tools import BaseTool
from math import *

from libs import langfuse_handler

# 创建安全的数学计算工具
class SafeMathTool(BaseTool):
    name: str = "Calculator"
    description: str = "适用于解决数学问题，当你需要进行数学计算时使用这个工具"
    
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

# 初始化大语言模型，这里使用 OpenAI，你可以替换成兼容的模型
llm = OpenAI(
    model="Qwen/Qwen2.5-72B-Instruct",
    openai_api_base="https://api.siliconflow.cn/v1",
    openai_api_key="sk-nsswwpfvuompvcqcseqsfbhjysigfiiybqyeznikustuhucq",
    temperature=0
)

# 初始化 REACT 范式的 Agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# 运行 Agent 来回答问题，修改问题为数学问题
question = "123 的平方加上 456 是多少？"
result = agent.run(question, callbacks=[langfuse_handler])
print(result)