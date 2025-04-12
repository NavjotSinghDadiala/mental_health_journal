import tkinter as tk
import math

# ---------------------------- CONSTANTS ------------------------------- #
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
FONT_NAME = "Courier"
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro Timer", fg="green")
    check_marks.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text="Long Break", fg="red")
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Short Break", fg="pink")
    else:
        count_down(WORK_MIN * 60)
        title_label.config(text="Work Time", fg="green")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    minutes = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"

    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro Timer - By AI Madhav")
window.config(padx=100, pady=50, bg="#f7f5dd")

title_label = tk.Label(text="Pomodoro Timer", fg="green", bg="#f7f5dd", font=(FONT_NAME, 40, "bold"))
title_label.grid(column=1, row=0)

try:
    tomato_img = tk.PhotoImage(file="tomato.png")  # Try to load from current directory
except:
    # Create a simple colored circle as fallback
    tomato_img = tk.PhotoImage(width=100, height=100)
    tomato_img.put("#FF0000", to=(0, 0, 100, 100))  # Red circle

canvas = tk.Canvas(width=200, height=224, bg="#f7f5dd", highlightthickness=0)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = tk.Button(text="Start", command=start_timer, font=(FONT_NAME, 12), highlightthickness=0)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", command=reset_timer, font=(FONT_NAME, 12), highlightthickness=0)
reset_button.grid(column=2, row=2)

check_marks = tk.Label(fg="green", bg="#f7f5dd", font=(FONT_NAME, 15))
check_marks.grid(column=1, row=3)

window.mainloop()
