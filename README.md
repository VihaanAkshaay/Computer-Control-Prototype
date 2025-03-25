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
├── computer_control_project/    # Main "library" package for your project
│   ├── __init__.py             # Makes this folder a Python package
│   ├── computer_tools.py       # Core tools (e.g., TypeTool, ClickTool)
│   ├── file_management.py      # File handling utilities (open, read, etc.)
│   ├── prog.py                 # Main logic / orchestration functions
│   └── utils.py                # Helper functions (display graphs, logging, etc.)
├── myserver/                   # Additional package for your server code
│   ├── __init__.py             # Marks this as a package
│   └── main.py                 # FastAPI entry point (defines `app` and `main()`)
├── setup.py                    # Minimal setup script to make project pip-installable
├── requirements.txt            # Pin or list your dependencies here
├── main.py                     # (Optional) An extra script if you need a CLI or quick start
├── .gitignore                  # Files/folders to exclude from Git (venv, build artifacts, etc.)
└── README.md                   # This file, with usage/setup/build instructions
```
## **Getting Started**

### **Prerequisites**
- Python 3.8 or higher
- A virtual environment (recommended)
- Required dependencies (listed in `requirements.txt`)

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/vihaanakshaay/computer-control-project.git
   cd computer-control-project
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  
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

## Dev Notes

### 1. Create and activate a new venv
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .
```

### 3. Verify imports
```bash
python -c "import computer_control_project.computer_tools; print('Success!')"
python -c "import myserver.main; print('Success!')"
```

### 4. Create the one executable file
```bash
shiv . \        
  --compressed \
  -o api_server.pyz \
  -e myserver.main:main \
  -p `python -c "import site; print(site.getsitepackages()[0])"`
```

### 5. Run the 'one executable' file
```
./api_server.pyz
```

### 6. Check if the file is working
- To check if the file is working: go to http://localhost:8000/docs and try the endpoints.