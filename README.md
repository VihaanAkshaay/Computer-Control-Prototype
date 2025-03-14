# **Computer Control Project**

## **Overview**
This is an initial stage prototype of my attempt towards replicating Anthropic's Computer Control for Mac.

## **Current Features**
- **Simulate Typing**: Simulate keyboard typing with the `TypeTool`.
- **Mouse Automation**: Perform mouse clicks at specific or random positions using the `ClickTool`.
- **Screenshot Capture**: Capture full-screen or region-specific screenshots with `ScreenshotTool`.
- **Image Loading & Analysis**: Load images or analyze them using advanced tools like GPT-4 Vision.
- **App Management**: Check for installed applications and open them programmatically.
- **Web Navigation**: Open Safari and navigate to specified URLs.
- **Pause Execution**: Temporarily pause execution for a specified time.
- **Search Capabilities**: Integrated search tool using TavilySearchResults.

## **Project Structure**
```
computer-control-project/
├── computer_control_project/  # Main package folder
│   ├── __init__.py            # Marks this as a package
│   ├── computer_tools.py      # Core tools (TypeTool, ClickTool, etc.)
│   ├── file_management.py     # File management utilities
│   ├── prog.py                # Main logic and tool orchestration
│   ├── utils.py               # Helper functions (e.g., display graph)
├── main.py                    # Entry point for the program
├── requirements.txt           # List of dependencies
├── .gitignore                 # Files to ignore in version control
├── README.md                  # Project documentation
```

## **Getting Started**

### **Prerequisites**
- Python 3.8 or higher
- A virtual environment (recommended)
- Required dependencies (listed in `requirements.txt`)

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/VihaanAkshaay/computer-control-project.git
   cd computer-control-project
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### **Usage**
1. Run the main program:
   ```bash
   python main.py
   ```

2. Follow the interactive prompts to use the tools.

### **Example Commands**
- Command in Natural Language:
  ```
  User: can you open safari, go to https://codepen.io/rlacorne/pen/wvWJxM and click somewhere on the screen and then go to http://bigtyper.com/?txt= and click somewhere on the screen and type your favorite word with 1 second delay between each step  and finally take a screenshot please?

  ```
