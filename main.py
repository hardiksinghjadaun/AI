import requests
from gui import AssistantGUI  # Import the GUI class
import tkinter as tk  # Import tkinter


if __name__ == "__main__":
    import os
    api_key = os.getenv("your api key")  # Retrieve API key from environment variable

    root = tk.Tk()  # Create the main window
    gui = AssistantGUI(root)
    root.mainloop()