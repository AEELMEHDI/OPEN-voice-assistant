import threading
import queue
import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import pyttsx3
import webbrowser as web
import pywhatkit as kit
from time import sleep
from datetime import datetime
import os
from screenshot import screenshot  # Import the screenshot function

# Your local modules
from news import get_news
from meteo import get_temperature

# -------------------- Core assistant functions --------------------


log_queue = queue.Queue()

def append_log(text: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_queue.put(f"[{timestamp}] {text}")

# === Text-to-Speech Function ===
def speak(text):
    append_log(f"OPEN says: {text}")
    engine = pyttsx3.init()
    # default voice selection (index 1 if available)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        try:
            engine.setProperty('voice', voices[1].id)
        except Exception:
            pass
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 260)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Speak in French if French voice found
def speakf(text):
    append_log(f"OPEN (fr) says: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    for v in voices:
        if "fr" in v.id or "french" in v.name.lower():
            engine.setProperty("voice", v.id)
            break
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Passive listen (wake word)
def passive_listen(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1
        append_log("Listening for wake word...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
            query = recognizer.recognize_google(audio, language='en-in')
            append_log(f"Heard (wake): {query}")
            return query.lower()
        except Exception as e:
            append_log(f"Passive listen error: {e}")
            return ""

# Command listening
def take_command(timeout=6, phrase_time_limit=6):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1
        append_log("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except Exception as e:
            append_log(f"Microphone listen error: {e}")
            return ""
    try:
        command = recognizer.recognize_google(audio, language='en-in')
        append_log(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry Boss, I didn't catch that.")
        return ""
    except Exception as e:
        append_log(f"Recognition error: {e}")
        speak("Something went wrong.")
        return ""

# Execute commands (trimmed: uses append_log for GUI)
def execute(command: str):
    command = command.lower()
    append_log(f"Executing: {command}")
#greetings==========================================================
    if "hello" in command or "hi" in command:
        speak("Hello Boss, how can I assist you today?")
# name=====================================================================    
    elif "name" in command:
        speak("YOU are my BOSS ELMEHDI and I am OPEN, your personal AI assistant.")
 # exit commands========================================================       
    elif any(w in command for w in ["stop", "exit", "quit", "close", "terminate", "shutdown", "bye"]):
        speak("Goodbye Boss!")
        # the GUI will handle the shutdown
        return "exit"
# introduce yourself========================================================    
    elif any(w in command for w in ["everyone", "greet everyone", "greet all", "greet", "introduce yourself"]):
        speak("Hello everyone, I am OPEN, your personal AI assistant.")
#google search, youtube, wikipedia, movies, find/search, gmail, assist, time, date, telegram, drive, code, focus mode, screenshot, news, weather========================================================        
    elif "google" in command:
        query = command.replace("google", "").replace("open", "").strip()
        speak(f"Searching Google for {query}" if query else "Opening Google.")
        web.open(f"https://www.google.com/search?q={query}" if query else "https://www.google.com")
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        kit.playonyt(song)
    elif "wikipedia" in command:
        speak("Opening Wikipedia for you Boss...")
        query = command.replace("wikipedia", "").replace('open', "").strip()
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}" if query else "https://www.wikipedia.org"
        web.open(url)
    elif "movies" in command:
        speak("Opening movie websites...")
        web.open("https://wecima.video/")
        web.open("https://tv1.egydead.live/")
    elif "find" in command or "search" in command:
        query = command.replace("find", "").replace("search", "").strip()
        if query:
            speak(f"Searching online for {query}")
            kit.search(query)
        else:
            speak("Please provide a search term.")
    elif "gmail" in command:
        speak("Opening Gmail...")
        sleep(0.3)
        web.open("https://mail.google.com/")
    elif "assist" in command:
        speak("Opening AI assistant chats...")
        web.open("https://chat.deepseek.com")# Update this URL to your preferred AI assistant chat if needed
        web.open("https://chat.openai.com/")# Update this URL to your preferred AI assistant chat if needed
     # scroll up and down, left click========================================================   
    elif "youtube" in command:
        query = command.replace("youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={query}" if query else "https://www.youtube.com"
        web.open(url)
        speak("Opening YouTube for you Boss.")
# time and date========================================================        
    elif 'time' in command:
        current_time = datetime.now().strftime("%H:%M %p")
        speak(f"The current time is {current_time}")
    elif 'date' in command:
        current_date = datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}")
# telegram, drive, code, focus mode, screenshot, news, weather========================================================        
    elif "telegram" in command:
        try:
            speak(f"Opening TELEGRAM...")
            path = r"C:\Users\hp\AppData\Roaming\Telegram Desktop\Telegram.exe"# Update this path to your Telegram executable if needed
            os.startfile(path)
        except Exception as e:
            speak("Sorry, I couldn't open TELEGRAM.")
            append_log(str(e))
    elif 'drive' in command:
        try:
            speak(f"Opening Google Drive...")
            web.open("https://drive.google.com/drive")# Update this URL if you want to open a specific folder in Google Drive
        except Exception as e:
            speak("Sorry, I couldn't open Google Drive.")
            append_log(str(e))
    elif "code" in command or "v s code" in command or "visual studio code" in command:
        try:
            speak(f"Opening Visual Studio Code...")
            path = r"C:\Users\hp\AppData\Local\Programs\Microsoft VS Code\Code.exe"# Update this path to your Visual Studio Code executable if needed
            os.startfile(path)
        except Exception as e:
            speak("Sorry, I couldn't open Visual Studio Code.")
            append_log(str(e))
    elif "focus mode" in command:
        speak("Starting a Pomodoro timer for 25 minutes.")
        for x in range(1500, 0, -1):
            if stop_event.is_set():
                append_log("Pomodoro cancelled")
                break
            sec = x % 60
            min = int(x / 60) % 60
            h = int(x / 3600)
            append_log(f"Timer: {h:02} | {min:02} | {sec:02}")
            sleep(1)
        speak("Time is UP!!!!!!")
    elif "screenshot" in command or "screen shot" in command:  
        try:
            speak("Taking a screenshot for you Boss...")
            screenshot()  # Call the screenshot function
            speak("Screenshot taken and saved.")
        except Exception as e:
            speak("Sorry, I couldn't take the screenshot.")
            append_log(str(e))  
    elif "news" in command:
        speak("Fetching the latest news headlines for you Boss...")
        try:
            news = get_news(6)
            speakf(news if news else "Sorry, I couldn't fetch the news right now.")
        except Exception as e:
            append_log(str(e))
            speak("Sorry, I couldn't fetch the news right now.")
    elif "weather" in command or "météo" in command or "meteo" in command:
        speak("Fetching the latest weather information for you Boss...")
        try:
            meteo = "Température en Casablanca " + get_temperature()
            speakf(meteo if meteo else "Sorry, I couldn't fetch the weather right now.")
        except Exception as e:
            append_log(str(e))
            speak("Sorry, I couldn't fetch the weather right now.")
    else:
        speak("I don't recognize that command yet Boss.")

# -------------------- Assistant threading control --------------------
stop_event = threading.Event()
assistant_thread = None

def assistant_loop():
    append_log("Assistant started")
    speak("Welcome back, Boss.")
    while not stop_event.is_set():
        full_query = passive_listen().lower()
        if "open" in full_query :
            append_log("Wake word detected.")
            command = full_query.replace("open", "").strip()
            if command:
                res = execute(command)
                if res == "exit":
                    stop_event.set()
                    break
                speak("up")
            else:
                # if no command captured, try explicit take_command
                cmd = take_command()
                if cmd:
                    res = execute(cmd)
                    if res == "exit":
                        stop_event.set()
                        break
        # small sleep to avoid tight loop
        sleep(0.1)
    append_log("Assistant stopped")

# -------------------- Tkinter UI --------------------
class NexusGUI:
    def __init__(self, root):
        self.root = root
        #root.iconbitmap("img.ico")

        root.title("Nexus - OPEN Assistant")
        root.geometry("800x600")
        root.configure(bg="#120101")

        # Controls frame
        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(fill=tk.X, padx=8, pady=6)

        self.start_btn = tk.Button(ctrl_frame, text="Start Assistant", command=self.start_assistant)
        self.start_btn.pack(side=tk.LEFT, padx=4)

        self.stop_btn = tk.Button(ctrl_frame, text="Stop Assistant", command=self.stop_assistant, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=4)

        self.passive_btn = tk.Button(ctrl_frame, text="Passive Listen (once)", command=self.do_passive_listen)
        self.passive_btn.pack(side=tk.LEFT, padx=4)

        self.speak_entry = tk.Entry(ctrl_frame, width=40)
        self.speak_entry.pack(side=tk.LEFT, padx=6)
        self.speak_btn = tk.Button(ctrl_frame, text="Speak Text", command=self.do_speak_text)
        self.speak_btn.pack(side=tk.LEFT, padx=4)

        # Manual command frame
        cmd_frame = tk.Frame(root)
        cmd_frame.pack(fill=tk.X, padx=8, pady=6)
        tk.Label(cmd_frame, text="Manual Command:").pack(side=tk.LEFT)
        self.cmd_entry = tk.Entry(cmd_frame, width=60)
        self.cmd_entry.pack(side=tk.LEFT, padx=6)
        tk.Button(cmd_frame, text="Send", command=self.send_manual_command).pack(side=tk.LEFT)

        # Log view
        self.log_box = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # status bar
        self.status_var = tk.StringVar(value="Stopped")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Start polling the log queue
        self.root.after(200, self.poll_log_queue)

    def poll_log_queue(self):
        while not log_queue.empty():
            try:
                msg = log_queue.get_nowait()
            except queue.Empty:
                break
            self.log_box.configure(state='normal')
            self.log_box.insert(tk.END, msg + "\n")
            self.log_box.configure(state='disabled')
            self.log_box.see(tk.END)
        self.root.after(200, self.poll_log_queue)

    def start_assistant(self):
        global assistant_thread, stop_event
        if assistant_thread and assistant_thread.is_alive():
            messagebox.showinfo("Info", "Assistant is already running.")
            return
        stop_event.clear()
        assistant_thread = threading.Thread(target=assistant_loop, daemon=True)
        assistant_thread.start()
        self.status_var.set("Running")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        append_log("Start button pressed")

    def stop_assistant(self):
        global stop_event
        stop_event.set()
        self.status_var.set("Stopping...")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        append_log("Stop button pressed")

    def do_passive_listen(self):
        # Run passive_listen once in background to avoid freezing GUI
        def task():
            res = passive_listen()
            if res:
                append_log(f"Passive result: {res}")
        threading.Thread(target=task, daemon=True).start()

    def do_speak_text(self):
        text = self.speak_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Enter text to speak")
            return
        threading.Thread(target=speak, args=(text,), daemon=True).start()

    def send_manual_command(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        append_log(f"Manual command: {cmd}")
        # execute in background
        def task():
            res = execute(cmd)
            if res == "exit":
                append_log("Exit requested by manual command")
        threading.Thread(target=task, daemon=True).start()

# -------------------- Run UI --------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = NexusGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (stop_event.set(), root.destroy()))
    root.mainloop()
#nexus gui===========================================================
