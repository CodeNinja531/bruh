import tkinter as tk
import datetime
import pygame

pygame.init()

# create window
window = tk.Tk()
window.title("Countdown timer")
window.geometry('500x400')
window.iconbitmap('timer.jpg')

# time showcase
time_label = tk.Label(window, text="00:00:00", font=('Arial', 30))
time_label.pack(pady=20)

# enter duration
duration_entry = tk.Entry(window, font=('Arial', 16), width=10)
duration_entry.pack(pady=10)
duration_entry.insert(0, "60")

# reminder
tip_label = tk.Label(window, text="countdown time (s)", font=('Arial', 10))
tip_label.pack(pady=2)

# button!!!
start_button = tk.Button(window, text="start", font=('Arial', 18), width=10, height=1)
start_button.pack(pady=10)

# button2!!
mute_button = tk.Button(window, text="mute", font=('Arial', 15), width=10, height=1)
mute_button.pack(pady=1)

# button3!!
stop_button = tk.Button(window, text="stop", font=('Arial', 18), width=10, height=1)
stop_button.pack(pady=100)


# __init__
is_running = False
start_time = 0
duration = 60
mute = False


def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def update_time():
    global is_running, start_time, duration
    if is_running:
        remaining_time = duration - (datetime.datetime.now() - start_time).total_seconds()
        if remaining_time <= 0:
            # END here---------------------------------------------
            is_running = False
            start_button.config(text="Start")
            time_label.config(text=format_time(0))
            if mute == False:
                pygame.mixer.music.load("../sound/alarm.mp3")
                pygame.mixer.music.play()
        else:
            time_label.config(text=format_time(int(remaining_time)))
            # 1 second
            window.after(100, update_time)


# buttons
def start_button_click():
    global is_running, start_time, duration
    if is_running:
        # stop
        is_running = False
        start_button.config(text="start")
    else:
        # start
        duration = int(duration_entry.get())
        start_time = datetime.datetime.now()
        is_running = True
        start_button.config(text="stop")
        update_time()

# stop timer
def stop_button_click():
    global is_running
    is_running = False
    start_button.config(text="start")
    mute_button.config(text="mute")
    time_label.config(text=format_time(0))


def mute_button_click():
    global mute
    if mute:
        mute = False
        mute_button.config(text="mute")
    else:
        mute = True
        mute_button.config(text="unmute")

# button clicking config
start_button.config(command=start_button_click)
stop_button.config(command=stop_button_click)
mute_button.config(command=mute_button_click)

# loop
window.mainloop()
