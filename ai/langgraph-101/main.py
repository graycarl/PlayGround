from typing import TypedDict, Annotated

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama


llm = ChatOllama(model="qwen3:4b")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State) -> State:
    msg = llm.invoke(state["messages"])
    return {
        "messages": [msg],
    }


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def stream_graph_updates(user_input: str) -> None:
    state = {
        "messages": [
            SystemMessage("You are a helpful assistant. /no_think"),
            HumanMessage(user_input),
        ]
    }
    for event in graph.stream(state):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


def main():
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            print("\nExiting...")
            break
        if user_input.lower() in ("exit", "quit", "q", "bye"):
            break
        stream_graph_updates(user_input)


if __name__ == "__main__":
    main()
