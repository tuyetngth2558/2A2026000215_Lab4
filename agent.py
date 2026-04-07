from typing import Annotated
import sys

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from openai import AuthenticationError
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from tools import calculate_budget, search_flights, search_hotels

load_dotenv()
try:
    # On Windows PowerShell, force UTF-8 output to avoid UnicodeEncodeError.
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)


def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print("Trả lời trực tiếp")

    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
builder.add_edge("tools", "agent")

graph = builder.compile()


if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        try:
            result = graph.invoke({"messages": [("human", user_input)]})
            final = result["messages"][-1]
            print(f"\nTravelBuddy: {final.content}")
        except AuthenticationError:
            print(
                "\nLỗi xác thực OpenAI API key (401). "
                "Vui lòng kiểm tra file .env và cập nhật OPENAI_API_KEY hợp lệ."
            )
            print("Gợi ý: tạo key mới tại https://platform.openai.com/api-keys")
        except Exception as exc:
            print(f"\nĐã xảy ra lỗi khi xử lý yêu cầu: {exc}")
