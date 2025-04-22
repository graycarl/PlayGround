"""
Run evaluation for react model
"""
import argparse
import logging
import dotenv
import langfuse
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

import react

dotenv.load_dotenv()
langfuse = langfuse.Langfuse()
llm = ChatOpenAI(
    model="Qwen/Qwen2.5-32B-Instruct",
    openai_api_base="https://api.siliconflow.cn/v1",
    openai_api_key="sk-nsswwpfvuompvcqcseqsfbhjysigfiiybqyeznikustuhucq",
    temperature=0
)


def run_dataset(dataset_name: str, run_name: str):
    dataset = langfuse.get_dataset(dataset_name)
    for item in dataset.items:
        logging.info(f">>>> Evaluating item: {item.id}")
        with item.observe(run_name=run_name) as trace_id:
            logging.info(f"Input: {item.input}")
            response = react.chatbot_response(item.input)
            logging.info(f"Response: {response}")
            logging.info(f"Expected output: {item.expected_output}")

            # checks if output is semantically similar to the expected value,
            # using a cosine similarity threshold.
            langfuse.score(
                trace_id=trace_id,
                name="semantic_similarity",
                value=get_item_score(item.expected_output, response),
            )


def get_item_score(expected_output, output):
    """Using semantic similarity to score the item"""
    sys_prompt = """
    你是一个用于评估大模型输出和预期输出相似度的工具，用户会输入 expected_output 和 output，
    请你给出一个 0-1 的分数，0 表示完全不相似，1 表示完全相似。

    请在 reponse 中只返回数字，表示相似度分数，范围是 0-1。
    """
    messages = [
        SystemMessage(content=sys_prompt),
        HumanMessage(content=f"expected_output: {expected_output}\n\noutput: {output}"),
    ]
    response = llm(messages)
    return float(response.content.strip()[:4])


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Run evaluation for react model")
    parser.add_argument("dataset_name", type=str, help="Name of the dataset")
    parser.add_argument("run_name", type=str, help="Name of the run")
    args = parser.parse_args()

    # Run the evaluation
    run_dataset(args.dataset_name, args.run_name)
