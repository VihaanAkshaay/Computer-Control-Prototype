
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
#os.environ["TAVILY_API_KEY"] = ""



class State(TypedDict):
    messages: Annotated[list, add_messages]


def main():
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

    #tool_node = ToolNode(tools=[search_tool, image_tool])
    tool_node = ToolNode(tools=[search_tool, image_tool, click_tool, type_tool, load_image_tool, load_and_analyze_tool, open_app_tool, go_website_tool, pause_tool])

    graph_builder.add_node("tools", tool_node)

    llm = ChatOpenAI(temperature=0.3, model="gpt-4o")
    llm_with_tools = llm.bind_tools(tools=[search_tool,image_tool, click_tool, type_tool, load_image_tool, load_and_analyze_tool, open_app_tool, go_website_tool, pause_tool])

    # Chatbot node
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )

    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    graph = graph_builder.compile(checkpointer=memory)


    # Visualise the graph:
    #utils.display_graph(graph)

    # Running the chatbot:
    def stream_graph_updates(user_input: str):
        for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config):
            for value in event.values():
                # Print the assistant's latest response
                print("Assistant:", value["messages"][-1].content)
                
                # Check if the tool node has been used and extract tool outputs
                '''
                if "tool_output" in value:
                    tool_output = value["tool_output"]
                    print("Tool Output:", tool_output)  # Debugging: See the raw tool response
                    
                    # Extract URLs if available
                    if isinstance(tool_output, list):  # Assuming the tool returns a list of results
                        for result in tool_output:
                            if "url" in result:
                                print("URL:", result["url"])
                '''

            
    config = {"configurable": {"thread_id":"1"}}

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            # Update and maintain the state
            stream_graph_updates(user_input)
            #snapshot = graph.get_state(config)
            #print("Snapshot:", snapshot)
        except Exception as e:
            print(f"An error occurred: {e}")
            break