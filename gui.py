import tkinter as tk
import speech_recognition as sr
import random
import logging

try:
    from assistant import Assistant
except ImportError as e:
    print(f"Error importing Assistant: {e}")
    Assistant = None

class BlueLightScreensaver:
    def __init__(self, master):
        self.master = master
        self.master.update_idletasks()  # Ensure dimensions are loaded
        
        self.canvas = tk.Canvas(master, bg='lightblue', width=self.master.winfo_width(), height=self.master.winfo_height())
        self.canvas.pack(fill=tk.BOTH, expand=True)

        try:
            self.background_image = tk.PhotoImage(file="AI_Assistant/background.png")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
            self.master.background_image = self.background_image  # Prevent garbage collection
        except Exception as e:
            logging.error(f"Error loading background image: {e}")

        self.draw_effect()

    def draw_effect(self):
        """Creates a dynamic blue light effect on the GUI background."""
        self.canvas.delete("effects")  # Delete only effects, keep background
        
        for _ in range(100):
            x1 = random.randint(0, self.canvas.winfo_width())
            y1 = random.randint(0, self.canvas.winfo_height())
            x2 = x1 + random.randint(20, 100)
            y2 = y1 + random.randint(20, 100)
            self.canvas.create_oval(x1, y1, x2, y2, fill='blue', outline='', tags="effects")

        self.master.after(1000, self.draw_effect)  # Redraw every second

class AssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("Personal AI Assistant")
        master.configure(bg='#87CEEB')

        self.screensaver = BlueLightScreensaver(master)

        self.label_frame = tk.Frame(master, bg='#87CEEB')
        self.label_frame.pack(pady=10)

        self.label = tk.Label(self.label_frame, text="Enter your command:", bg='#87CEEB', font=('Arial', 16, 'bold'))
        self.label.pack()

        self.command_entry = tk.Entry(self.label_frame, font=('Arial', 12))
        self.command_entry.pack()

        self.response_label = tk.Label(master, text="", bg='#87CEEB', font=('Arial', 12))
        self.response_label.pack(pady=10)

        self.button_frame = tk.Frame(master, bg='#87CEEB')
        self.button_frame.pack(pady=10)

        try:
            self.submit_icon = tk.PhotoImage(file="submit_icon.png")
            self.voice_icon = tk.PhotoImage(file="voice_icon.png")
        except:
            self.submit_icon = tk.PhotoImage(width=20, height=20)
            self.voice_icon = tk.PhotoImage(width=20, height=20)

        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.process_command,
                                       bg='#4682B4', fg='white', font=('Arial', 12, 'bold'), 
                                       image=self.submit_icon, compound=tk.LEFT)

        self.voice_button = tk.Button(self.button_frame, text="Voice Command", command=self.activate_voice_command,
                                      bg='#4682B4', fg='white', font=('Arial', 12, 'bold'), 
                                      image=self.voice_icon, compound=tk.LEFT)

        self.submit_button.pack(side=tk.LEFT, padx=5)
        self.voice_button.pack(side=tk.LEFT, padx=5)

        self.assistant = Assistant() if Assistant else None

    def activate_voice_command(self):
        """Activates voice recognition for commands."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.response_label.config(text="Listening... Please speak clearly.")
            self.master.update()
            recognizer.adjust_for_ambient_noise(source, duration=1)

            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                self.response_label.config(text=f"You said: {command}")
                if self.assistant:
                    self.assistant.process_command(command.lower())
            except sr.UnknownValueError:
                self.response_label.config(text="Sorry, I could not understand the command.")
            except sr.RequestError:
                self.response_label.config(text="Check your internet connection.")
            except sr.WaitTimeoutError:
                self.response_label.config(text="No voice detected, try again.")

    def process_command(self):
        """Processes the command entered in the text box."""
        command = self.command_entry.get().strip()
        if not command:
            self.response_label.config(text="Please enter a command!")
            return

        if self.assistant:
            response = self.assistant.process_command(command)
            self.response_label.config(text=response)

if __name__ == "__main__":
    root = tk.Tk()
    gui = AssistantGUI(root)
    root.mainloop()
