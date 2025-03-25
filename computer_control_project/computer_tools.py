import pyautogui
import random
from PIL import ImageGrab, Image
from io import BytesIO
import base64
import time
import openai

import pyautogui
import random
import os
import subprocess

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from langchain_core.tools import BaseTool
from pydantic import PrivateAttr
import subprocess

class TypeTool(BaseTool):
    name: str = "type_text"
    description: str = "Simulates typing text using the keyboard."

    def _run(self, query: str) -> dict:
        """
        Simulates typing the provided text using the keyboard.
        """
        try:
            # Ensure the query is not empty
            if not query.strip():
                raise ValueError("No text provided to type.")
            
            # Add a short delay
            time.sleep(0.5) 

            # Use pyautogui to type the text
            pyautogui.typewrite(query)

            # Return a confirmation message
            return {
                "messages": [
                    {"role": "assistant", "content": f'Typed the text: "{query}".'}
                ]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"Error typing the text: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. (Optional: Raise an error if async is not supported.)
        """
        raise NotImplementedError("This tool does not support async calls.")

class ClickTool(BaseTool):
    name: str = "click_bottom_half"
    description: str = "Performs a mouse click at a specific point or a random point in the bottom half of the screen."

    def _run(self, query: str) -> dict:
        """
        Performs a mouse click at a specific point if provided, otherwise clicks a random point in the bottom half of the screen.
        """
        try:
            # Get screen dimensions
            screen_width, screen_height = pyautogui.size()

            # Parse the query to check for specific coordinates
            coordinates = query.strip().split(",") if query else []
            if len(coordinates) == 2:
                try:
                    # Convert coordinates to integers
                    x = int(coordinates[0].strip())
                    y = int(coordinates[1].strip())

                    # Ensure the coordinates are within the screen boundaries
                    if x < 0 or x >= screen_width or y < screen_height // 2 or y >= screen_height:
                        raise ValueError("The specified coordinates are out of bounds.")
                except ValueError:
                    return {
                        "messages": [{"role": "assistant", "content": "Invalid coordinates. Please provide valid integers for x and y."}]
                    }
            else:
                # Generate random coordinates in the bottom half if no valid coordinates are provided
                x = random.randint(0, screen_width - 1)
                y = random.randint(screen_height // 2, screen_height - 1)

            # Move the mouse to the position and click
            pyautogui.moveTo(x, y)
            pyautogui.click()

            # Wait for the click to register
            pyautogui.sleep(0.5)

            # Return a confirmation message
            return {
                "messages": [
                    {"role": "assistant", "content": f"Mouse clicked at: ({x}, {y})."}
                ]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"Error performing the mouse click: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. (Optional: Raise an error if async is not supported.)
        """
        raise NotImplementedError("This tool does not support async calls.")

class ScreenshotTool(BaseTool):
    name: str = "capture_screenshot"
    description: str = "Captures a screenshot with optional dimensions x, y, width, height and saves it with a specified name."

    def _run(self, query: str) -> dict:
        """
        Captures a screenshot with optional dimensions and saves it with a specified name.
        """
        try:
            # Parse the query for dimensions and filename
            query_parts = query.split(",") if query else []
            x, y, width, height, filename = None, None, None, None, None

            if len(query_parts) >= 4:
                # Extract dimensions (x, y, width, height)
                x = int(query_parts[0].strip())
                y = int(query_parts[1].strip())
                width = int(query_parts[2].strip())
                height = int(query_parts[3].strip())

            if len(query_parts) == 5:
                # Extract filename
                filename = query_parts[4].strip()
            elif len(query_parts) < 5:
                # Default filename
                filename = "screenshot.png"

            # Validate filename
            if not filename.endswith(".png"):
                filename += ".png"
            if "/" in filename or "\\" in filename:
                raise ValueError("Invalid filename. Please provide a simple name without directory paths.")

            # Capture the screenshot
            if x is not None and y is not None and width is not None and height is not None:
                bbox = (x, y, x + width, y + height)
                screenshot = ImageGrab.grab(bbox=bbox)
            else:
                # Capture the full screen
                screenshot = ImageGrab.grab()

            # Save the screenshot with the given filename
            screenshot.save(filename, format="PNG")

            # Return confirmation message
            return {
                "messages": [
                    {"role": "assistant", "content": f"The screenshot has been captured and saved as '{filename}' in the current directory."}
                ]
            }
        except ValueError as ve:
            return {
                "messages": [{"role": "assistant", "content": str(ve)}]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"Error capturing or saving the screenshot: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. (Optional: Raise an error if async is not supported.)
        """
        raise NotImplementedError("This tool does not support async calls.")

class LoadImageTool(BaseTool):
    name: str = "load_image"
    description: str = "Loads an image from a specified file path and returns its content."

    def _run(self, query: str) -> dict:
        """
        Loads an image from a specified file path and returns its content in Base64 format.
        """
        try:
            # Ensure the query contains the file path
            file_path = query.strip()
            if not file_path:
                raise ValueError("No file path provided to load the image.")

            # Open the image file
            with Image.open(file_path) as img:
                # Convert the image to a Base64 string
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                buffered.seek(0)  # Reset buffer position
                image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Return the image content
            return {
                "messages": [
                    {"role": "assistant", "content": "The image has been loaded successfully."},
                    {"role": "assistant", "content": f"data:image/png;base64,{image_data}"}
                ]
            }
        except FileNotFoundError:
            return {
                "messages": [{"role": "assistant", "content": f"File not found: {file_path}. Please check the file path and try again."}]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"Error loading the image: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. (Optional: Raise an error if async is not supported.)
        """
        raise NotImplementedError("This tool does not support async calls.")

class LoadAndAnalyzeImageTool(BaseTool):
    name: str = "load_and_analyze_image"
    description: str = "Loads an image from a specified file path, analyzes it using GPT-4 Vision, and returns the description."

    def _run(self, query: str) -> dict:
        """
        Loads an image from a file, encodes it as Base64, and passes it back for analysis.
        """
        try:
            # Ensure the query contains the file path
            file_path = query.strip()
            if not file_path:
                raise ValueError("No file path provided to load the image.")

            # Open the image file
            with Image.open(file_path) as img:
                # Convert the image to Base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                buffered.seek(0)
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Construct the assistant's response to include the image as Base64
            response_content = f"data:image/png;base64,{image_base64}"

            return {
                "messages": [
                    {"role": "assistant", "content": "The image has been loaded successfully."},
                    {"role": "assistant", "content": response_content}
                ]
            }

        except FileNotFoundError:
            return {
                "messages": [{"role": "assistant", "content": f"File not found: {file_path}. Please check the file path and try again."}]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"Error processing the image: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. Raise an error if async is not supported.
        """
        raise NotImplementedError("This tool does not support async calls.")
    
class OpenAppTool(BaseTool):
    name: str = "check_and_open_app"
    description: str = "Checks if an app is installed on the Mac and opens it if it exists."

    def _run(self, query: str) -> dict:
        """
        Checks if the specified app is installed and opens it.
        """
        try:
            # Get the app name from the query
            app_name = query.strip()
            if not app_name:
                raise ValueError("No app name provided to check.")

            # Directories to search for apps
            app_directories = [
                "/Applications",
                "/System/Applications",
                os.path.expanduser("~/Applications"),
            ]

            # Check if the app exists
            app_path = None
            for directory in app_directories:
                potential_path = os.path.join(directory, f"{app_name}.app")
                if os.path.exists(potential_path):
                    app_path = potential_path
                    break

            if not app_path:
                return {
                    "messages": [
                        {"role": "assistant", "content": f"The app '{app_name}' is not installed on this Mac."}
                    ]
                }

            # Open the app using AppleScript
            subprocess.run(["open", app_path], check=True)

            # Return a success message
            return {
                "messages": [
                    {"role": "assistant", "content": f"The app '{app_name}' was found and has been opened."}
                ]
            }

        except ValueError as ve:
            return {
                "messages": [{"role": "assistant", "content": str(ve)}]
            }
        except subprocess.CalledProcessError:
            return {
                "messages": [{"role": "assistant", "content": f"Failed to open the app '{app_name}'."}]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"An error occurred: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. Raise an error if async is not supported.
        """
        raise NotImplementedError("This tool does not support async calls.")

class GoToWebpageTool(BaseTool):
    name: str = "go_to_webpage"
    description: str = "Uses Safari to navigate to a specified webpage. Opens Safari if it's not already running."

    _open_app_tool: BaseTool = PrivateAttr()

    def __init__(self, open_app_tool):
        """
        Initialize the tool with a reference to the OpenAppTool.
        """
        super().__init__()
        self._open_app_tool = open_app_tool  # Use PrivateAttr for the tool reference

    def _run(self, query: str) -> dict:
        """
        Opens Safari (via OpenAppTool if needed) and navigates to the specified webpage.
        """
        try:
            # Ensure the query contains a valid URL
            url = query.strip()
            if not url.startswith("http://") and not url.startswith("https://"):
                raise ValueError("Invalid URL. Please provide a valid URL starting with http:// or https://.")

            # Use OpenAppTool to ensure Safari is open
            safari_response = self._open_app_tool._run("Safari")
            if "not installed" in safari_response["messages"][0]["content"]:
                return safari_response

            # Use AppleScript to open the URL in Safari
            applescript = f"""
            tell application "Safari"
                open location "{url}"
                activate
            end tell
            """
            subprocess.run(["osascript", "-e", applescript], check=True)

            # Return success message
            return {
                "messages": [
                    {"role": "assistant", "content": f"Safari has navigated to the webpage: {url}"}
                ]
            }

        except ValueError as ve:
            return {
                "messages": [{"role": "assistant", "content": str(ve)}]
            }
        except subprocess.CalledProcessError:
            return {
                "messages": [{"role": "assistant", "content": f"Failed to navigate to the webpage: {url}"}]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"An error occurred: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. Raise an error if async is not supported.
        """
        raise NotImplementedError("This tool does not support async calls.")

class PauseTool(BaseTool):
    name: str = "pause"
    description: str = "Pauses execution for a specified amount of time (in seconds)."

    def _run(self, query: str) -> dict:
        """
        Pauses execution for the specified amount of time in seconds.
        """
        try:
            # Parse the query to get the duration in seconds
            duration = float(query.strip())
            if duration < 0:
                raise ValueError("Duration must be a non-negative number.")

            # Pause execution
            time.sleep(duration)

            # Return success message
            return {
                "messages": [
                    {"role": "assistant", "content": f"Paused for {duration} seconds."}
                ]
            }

        except ValueError:
            return {
                "messages": [{"role": "assistant", "content": "Invalid input. Please provide a valid number of seconds to pause."}]
            }
        except Exception as e:
            return {
                "messages": [{"role": "assistant", "content": f"An error occurred: {e}"}]
            }

    def _arun(self, query: str) -> dict:
        """
        Asynchronous version of the tool. Raise an error if async is not supported.
        """
        raise NotImplementedError("This tool does not support async calls.")

