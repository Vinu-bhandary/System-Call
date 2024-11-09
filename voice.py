import tkinter as tk
from tkinter import ttk
import threading
import speech_recognition as sr
import winreg
import pyttsx3
import time
from file_operation_test import create_folder, rename_folder, move_folder, delete_folder, open_folder, find_folder

recognizer = sr.Recognizer()
engine = pyttsx3.init()

with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
        desktop = winreg.QueryValueEx(key, "Desktop")[0]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_text(text):
    if "open folder" in text:
        name = text.replace("open folder ","").strip().split(" ")
        if name[-1] == "desktop":
            path = desktop+"\\"+name[0]
        elif name[-1] == "download":
            path = find_folder("Downloads")+"\\"+name[0]
        else:
            path = find_folder(name[-1].capitalize())+"\\"+name[0]
        result = open_folder(path)
    
    elif "rename folder" in text:
        name = text.replace("rename folder ","").strip().split(" ")
        if name[3] == "desktop":
            f_path = desktop
        elif name[3] == "download":
            f_path = find_folder("Downloads")
        else:
            f_path = find_folder(name[3].capitalize())
    
        new_name = f_path+"\\"+name[-1]
        path = f_path+"\\"+name[0]
        result = rename_folder(path, new_name)
    
    elif "delete folder" in text:
        name = text.replace("delete folder ","").strip().split(" ")
        if name[-1] == "desktop":
            path = desktop+"\\"+name[0]
        elif name[-1] == "download":
            path = find_folder("Downloads")+"\\"+name[0]
        else:
            path = find_folder(name[-1].capitalize())+"\\"+name[0]
        result = delete_folder(path)
    
    elif "create folder" in text:
        name = text.replace("create folder ","").strip().split(" ")
        if name[-1] == "desktop":
            path = desktop+"\\"+name[0]
        elif name[-1] == "download":
            path = find_folder("Downloads")+"\\"+name[0]
        else:
            path = find_folder(name[-1].capitalize())+"\\"+name[0]
        result = create_folder(path)

    if result == 'TrueC':
        update_text("Folder created successfully")
        speak("Folder created successfully")
    elif result == 'TrueR':
        update_text("Folder renamed successfully")
        speak("Folder renamed successfully")
    elif result == 'TrueD':
        update_text("Folder deleted successfully")
        speak("Folder deleted successfully")
    elif result == 'TrueO':
        update_text("Folder opened successfully")
        speak("Folder opened successfully")
    else:
        update_text(result)
        speak("Failed to perform the operation")

def listen_and_display():
    with sr.Microphone() as source:
        update_status("Listening...", "green")  
        audio = recognizer.listen(source)
        
        update_status("Recognising...", "yellow")  

        try:
            text = recognizer.recognize_google(audio)
            update_text(text)
            time.sleep(1)
            process_text(text)

        except sr.UnknownValueError:
            text = "Sorry, I didn't understand that."
            update_text(text)
            speak(text)
        except sr.RequestError:
            text = "Could not request results; check your network connection."
            update_text(text)
            speak(text)
        
        update_status("Click 'Start' to speak", "blue")
        update_text("")  

def update_text(text):
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, text)
    text_area.config(state=tk.DISABLED)

def update_status(message, color):
    status_label.config(text=message)
    status_label.config(fg=color)
    if color:
        animate_status()

def animate_status():
    original_color = status_label.cget("fg")
    for i in range(5):  
        status_label.config(fg="lightgreen")
        root.update()
        time.sleep(0.1)
        status_label.config(fg=original_color)
        root.update()
        time.sleep(0.1)

def start_assistant():
    threading.Thread(target=listen_and_display).start()

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x400")
root.configure(bg="#f0f0f5")

style = ttk.Style()
style.configure("TButton", font=("Arial", 14), padding=10)
style.configure("TLabel", font=("Arial", 14), background="#f0f0f5")
style.configure("TFrame", background="#f0f0f5")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

status_label = tk.Label(main_frame, text="Click 'Start' to speak", font=("Arial", 14), fg="blue", bg="#f0f0f5")
status_label.pack(pady=10)

text_area = tk.Text(main_frame, height=7, width=45, font=("Arial", 12), wrap="word", bg="#e6e6fa", fg="#333")
text_area.pack(pady=10)
text_area.config(state=tk.DISABLED)
text_area.config(highlightthickness=1, highlightbackground="#d1d1e0")

start_button = ttk.Button(main_frame, text="🎤 Start Listening", command=start_assistant, style="TButton")
start_button.pack(pady=20)

root.mainloop()
