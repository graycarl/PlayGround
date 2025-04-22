# from langchain_openai import ChatOpenAI
import libs
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# llm = ChatOpenAI(
#     model="Qwen/Qwen2.5-72B-Instruct",
#     openai_api_base="https://api.siliconflow.cn/v1",
#     openai_api_key="sk-nsswwpfvuompvcqcseqsfbhjysigfiiybqyeznikustuhucq",
#     temperature=0
# )
llm = ChatOllama(model="qwen2.5:14b")

tagging_prompt = ChatPromptTemplate.from_template("""
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
""")


class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(description="The language the text is written in")


# LLM
llm = llm.with_structured_output(
    Classification
)

inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
prompt = tagging_prompt.invoke({"input": inp})
response = llm.invoke(prompt, config={"callbacks": [libs.langfuse_handler]})

print(response.model_dump())
