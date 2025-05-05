
from typing import TypedDict, Annotated

import dotenv
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_exa.tools import ExaSearchResults


dotenv.load_dotenv()
llm = ChatOllama(model="qwen3:14b")
tools = [
    ExaSearchResults(),
]
llm_with_tools = llm.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State) -> State:
    msg = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [msg],
    }


class ToolNode:
    """A node that run the tool requested in the last message."""
    def __init__(self, tools: list) -> None:
        self.tools = {tool.name: tool for tool in tools}

    def __call__(self, state: State) -> State:
        if messages := state["messages"]:
            message = messages[-1]
        else:
            raise ValueError("No messages in state")
        outputs = []
        for tool_call in message.tool_calls:
            func = self.tools[tool_call['name']]
            result = func.invoke(tool_call['args'])
            outputs.append(ToolMessage(
                content=result,
                name=tool_call['name'],
                tool_call_id=tool_call['id'],
            ))
        return { "messages": outputs }


def route_tools(state: State) -> str:
    message = state["messages"][-1]
    if getattr(message, "tool_calls", None):
        return "tools"
    else:
        return END


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", route_tools)
graph_builder.add_edge("tools", "chatbot")

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
            message = value["messages"][-1]
            if isinstance(message, ToolMessage):
                continue
            print(f'{message.type}: {message.content}')
