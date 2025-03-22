from langgraph.checkpoint.memory import MemorySaver

from typing import Annotated

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

import computer_control_project.utils as utils
import computer_control_project.computer_tools as computer_tools
import os


from PIL import ImageGrab, Image
from langchain_core.tools import BaseTool
from io import BytesIO

# Setting API keys

class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Initialize Graph and Tools at Module Level ---
graph_builder = StateGraph(State)
memory = MemorySaver()

########### TOOLS! ###############
type_tool = computer_tools.TypeTool()
image_tool = computer_tools.ScreenshotTool()
click_tool = computer_tools.ClickTool()
load_image_tool = computer_tools.LoadImageTool()
load_and_analyze_tool = computer_tools.LoadAndAnalyzeImageTool()
open_app_tool = computer_tools.OpenAppTool()
go_website_tool = computer_tools.GoToWebpageTool(open_app_tool)
pause_tool = computer_tools.PauseTool()
search_tool = TavilySearchResults(max_results=2)

tool_node = ToolNode(tools=[search_tool, image_tool, click_tool, type_tool, load_image_tool, load_and_analyze_tool, open_app_tool, go_website_tool, pause_tool])

graph_builder.add_node("tools", tool_node)

llm = ChatOpenAI(temperature=0.3, model="gpt-4o")
llm_with_tools = llm.bind_tools(tools=[search_tool, image_tool, click_tool, type_tool, load_image_tool, load_and_analyze_tool, open_app_tool, go_website_tool, pause_tool])

# Chatbot node
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_conditional_edges("chatbot", tools_condition)

# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}

# --- Define the function to process user input ---
def process_user_input(user_input: str) -> list:
    responses = []
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config):
        for value in event.values():
            responses.append(value["messages"][-1].content)
    return responses

# --- Define the function to reset the chat ---
def reset_chat():
    memory.reset()

# --- Define function to look at the chat history ---
def look_at_chat_history():
    print(memory.get_all_entries())
    return {"messages": [{"role": "assistant", "content": "Chat history: " + str(memory.get_all_entries())}]}

# --- Optional: CLI interface for local testing ---
def main():
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            elif user_input.lower() in ["reset", "r"]:
                reset_chat()
                continue
            else:
                outputs = process_user_input(user_input)
                for output in outputs:
                    print("Assistant:", output)
                    
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()