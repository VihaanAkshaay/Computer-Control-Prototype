from langgraph import Graph, Node, Agent
from langchain.chat_models import ChatOpenAI
import os

# Function to open Firefox
def open_firefox_logic(context=None) -> str:
    """
    Opens the Firefox browser on the system.
    """
    try:
        from appscript import app
        firefox = app('Firefox')
        firefox.activate()
        return "Firefox opened successfully!"
    except Exception as e:
        return f"Failed to open Firefox: {e}"

# Function to search a website (e.g., YouTube)
def search_website_logic(context=None) -> str:
    """
    Navigates to a website in the Firefox browser using AppleScript.
    The website URL is taken from user input in the context.
    """
    try:
        website = context.get("website", "https://www.youtube.com")  # Default to YouTube
        applescript = f'''
        tell application "Firefox"
            activate
            open location "{website}"
        end tell
        '''
        os.system(f'osascript -e \'{applescript}\'')
        return f"Navigated to {website} in Firefox!"
    except Exception as e:
        return f"Failed to navigate to the website: {e}"

# Initialize an AI agent
llm = ChatOpenAI(temperature=0, model="gpt-4")
agent = Agent(llm)

# Define nodes
open_firefox_node = Node(
    name="Open Firefox",
    logic=open_firefox_logic
)

search_website_node = Node(
    name="Search Website",
    logic=search_website_logic
)

# Define the graph
graph = Graph(
    nodes=[open_firefox_node, search_website_node],
    edges=[
        ("Open Firefox", "Search Website")  # Search Website depends on Firefox being open
    ]
)

# Execute the graph
if __name__ == "__main__":
    # Get user input
    user_website = input("Enter the website URL to navigate to (default: YouTube): ").strip()
    if not user_website:
        user_website = "https://www.youtube.com"  # Default to YouTube

    print("Executing LangGraph workflow...")
    # Pass user input as context to the graph
    results = graph.run(agent, context={"website": user_website})

    for node_name, result in results.items():
        print(f"Node: {node_name} -> Result: {result}")

