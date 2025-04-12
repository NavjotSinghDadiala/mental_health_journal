import tkinter as tk
from tkinter import messagebox
import threading
import os

def run_assistant():
    python_path = r"C:\Users\dadia\AppData\Local\Programs\Python\Python312\python.exe"

    script_path = "D:\\programming\\hackathonn\\mudakshar\\assistantmain.py"
    
    os.system(f'start "" "{python_path}" "{script_path}"')

def launch_assistant():
    threading.Thread(target=run_assistant).start()

# Create GUI window
root = tk.Tk()
root.title("Akshar - AI Assistant")
root.geometry("400x300")

title = tk.Label(root, text="🧠 Akshar Assistant", font=("Arial", 16))
title.pack(pady=20)

start_btn = tk.Button(root, text="Start Assistant", command=launch_assistant, font=("Arial", 14), bg="lightgreen")
start_btn.pack(pady=10)

exit_btn = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14), bg="tomato")
exit_btn.pack(pady=10)

root.mainloop()
