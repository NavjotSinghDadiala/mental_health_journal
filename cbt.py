import tkinter as tk
from tkinter import messagebox
import datetime
import os

# Log directory
if not os.path.exists("logs"):
    os.makedirs("logs")

# === CORE FUNCTIONS ===
def log_thought(thought):
    if not thought.strip():
        messagebox.showwarning("Empty Entry", "Please enter a thought to log.")
        return
    with open("logs/thought_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {thought}\n")
    messagebox.showinfo("Logged", "Your thought has been logged.")
    entry_thought.delete(0, tk.END)

def cbt_reframe():
    thought = entry_thought.get()
    if not thought.strip():
        messagebox.showwarning("Empty Entry", "Enter a thought to reframe.")
        return
    top = tk.Toplevel()
    top.title("CBT Reframe Exercise")

    tk.Label(top, text=f"Original Thought: {thought}", wraplength=400).pack(pady=5)
    tk.Label(top, text="Evidence FOR the thought:").pack()
    text_for = tk.Text(top, height=3, width=50)
    text_for.pack()

    tk.Label(top, text="Evidence AGAINST the thought:").pack()
    text_against = tk.Text(top, height=3, width=50)
    text_against.pack()

    tk.Label(top, text="Balanced Reframe:").pack()
    text_reframe = tk.Text(top, height=3, width=50)
    text_reframe.pack()

    def save_reframe():
        with open("logs/reframes.txt", "a") as f:
            f.write(f"\nDate: {datetime.datetime.now()}\n")
            f.write(f"Original: {thought}\n")
            f.write(f"For: {text_for.get('1.0', 'end').strip()}\n")
            f.write(f"Against: {text_against.get('1.0', 'end').strip()}\n")
            f.write(f"Reframe: {text_reframe.get('1.0', 'end').strip()}\n")
        messagebox.showinfo("Saved", "Your reframe has been saved.")
        top.destroy()

    tk.Button(top, text="Save Reframe", command=save_reframe).pack(pady=10)

# === GUI SETUP ===
root = tk.Tk()
root.title("Offline CBT Buddy")
root.geometry("500x300")

lbl_title = tk.Label(root, text="🧠 CBT Thought Journal", font=("Helvetica", 16, "bold"))
lbl_title.pack(pady=10)

entry_thought = tk.Entry(root, width=60)
entry_thought.pack(pady=5)

btn_log = tk.Button(root, text="Log Thought", width=20, command=lambda: log_thought(entry_thought.get()))
btn_log.pack(pady=5)

btn_reframe = tk.Button(root, text="CBT Reframe Exercise", width=20, command=cbt_reframe)
btn_reframe.pack(pady=5)

root.mainloop()
