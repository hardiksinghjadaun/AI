import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import requests
import pyautogui
from datetime import datetime
from tkinter import filedialog

class Assistant:
    def __init__(self):
        """Initialize the AI assistant with a speech recognizer and text-to-speech engine."""
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()

    def speak(self, text):
        """Convert text to speech and speak it out."""
        self.speaker.say(text)
        self.speaker.runAndWait()

    def listen(self):
        """Listen for user voice input and return recognized text."""
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")

                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio)
                print(f"You said: {command}")
                return command.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            self.speak("Could not request results, check your internet connection.")
            return None
        except sr.WaitTimeoutError:
            self.speak("Listening timed out, try speaking again.")
            return None
        except OSError as e:
            self.speak("Microphone error detected. Please check your microphone settings.")
            return None

    def get_weather(self, city):
        """Fetch the weather data for a given city."""
        print(f"Fetching weather for city: {city}")

        api_key = "your api key"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The weather in {city} is {weather_description} with a temperature of {temperature}°C."
        else:
            return "Sorry, I couldn't fetch the weather data."

    def generate_essay(self, topic):
        """Generate a simple essay based on the given topic."""
        introduction = f"This essay discusses the topic of {topic}."
        body = f"{topic} is an important subject because it allows us to explore various aspects related to it."
        conclusion = f"In conclusion, understanding {topic} is crucial for our knowledge."
        return f"{introduction}\n\n{body}\n\n{conclusion}\n"

    def process_command(self, command):
        """Process user command and execute actions accordingly."""
        if command is None:
            return

        print(f"Processing command: {command}")

        if "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            self.speak("Opening YouTube.")

        elif "write an essay on" in command:
            topic = command.replace("write an essay on", "").strip()
            if not topic:
                self.speak("Please specify a topic for the essay.")
                return

            self.speak(f"Writing an essay on {topic}.")
            essay = self.generate_essay(topic)

            self.speak("Please open a text editor, and I will start typing.")
            pyautogui.sleep(3)
            pyautogui.typewrite(essay)

        elif "play music" in command:
            music_file_path = filedialog.askopenfilename(title="Select a music file")
            if not music_file_path:
                self.speak("No file selected.")
            else:
                os.system(f'start "" "{music_file_path}"')
                self.speak("Playing music.")

        elif "what time is it" in command:
            current_time = datetime.now().strftime("%H:%M")
            self.speak(f"The current time is {current_time}.")

        elif "open calculator" in command:
            os.system("calc")
            self.speak("Opening Calculator.")

        elif "open word" in command:
            os.system("start winword")
            self.speak("Opening Microsoft Word.")

        elif "open excel" in command:
            os.system("start excel")
            self.speak("Opening Microsoft Excel.")

        elif "open powerpoint" in command:
            os.system("start powerpnt")
            self.speak("Opening Microsoft PowerPoint.")

        elif "open file explorer" in command:
            os.system("explorer")
            self.speak("Opening File Explorer.")

        elif "open task manager" in command:
            os.system("taskmgr")
            self.speak("Opening Task Manager.")

        elif "open control panel" in command:
            os.system("control")
            self.speak("Opening Control Panel.")

        elif "open settings" in command:
            os.system("start ms-settings:")
            self.speak("Opening Settings.")

        elif "open command prompt" in command:
            os.system("cmd")
            self.speak("Opening Command Prompt.")

        else:
            self.speak("Sorry, I can't help with that. Please try a different command.")
            print(f"Unrecognized command: {command}")

    def run(self):
        """Start the AI assistant and continuously listen for commands."""
        self.speak("Hello! I am your personal AI assistant.")
        while True:
            command = self.listen()
            if command:
                self.process_command(command)

if __name__ == "__main__":
    assistant = Assistant()
    assistant.run()
