import tkinter as tk
from tkinter import Menu
import pygame
import datetime
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("This is just a title")
        self.geometry("500x400")
        self.iconbitmap('timer.jpg')

        # Initialize container for pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to hold pages
        self.pages = {}

        # Add pages to the container
        for Page in (timer, PageTwo):
            page_name = Page.__name__
            page = Page(parent=self.container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Create the menu
        self.create_menu()

        # Show the first page
        self.show_page("timer")

    def create_menu(self):
        # Create the menu bar for navigation.
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # Add a "Pages" menu
        pages_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Pages", menu=pages_menu)

        # Add items to switch between pages
        pages_menu.add_command(label="Timer", command=lambda: self.show_page("timer"))
        pages_menu.add_command(label="Page Two", command=lambda: self.show_page("PageTwo"))

    def show_page(self, page_name):
        # Bring the given page to the front.
        page = self.pages[page_name]
        page.tkraise()
        self.title("this is just a " + page_name)

class timer(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # timer variables
        self.is_running = False
        self.start_time = 0
        self.duration = 60
        self.mute = False

        # initialize pygame for sound
        pygame.init()

        # create window elements
        self.time_label = tk.Label(self, text="00:00:00.0", font=('Arial', 30))
        self.time_label.pack(pady=20)

        self.duration_entry = tk.Entry(self, font=('Arial', 16), width=10)
        self.duration_entry.pack(pady=10)
        self.duration_entry.insert(0, "60")

        self.tip_label = tk.Label(self, text="countdown time (s)", font=('Arial', 10))
        self.tip_label.pack(pady=2)

        self.start_button = tk.Button(self, text="start", font=('Arial', 18), width=10, height=1)
        self.start_button.pack(pady=10)

        self.mute_button = tk.Button(self, text="mute", font=('Arial', 15), width=10, height=1)
        self.mute_button.pack(pady=1)

        self.nothing = tk.Button(self, text="nothing here", font=('Arial', 10), width=16, height=1)
        self.nothing.pack(pady=97)

        self.stop_button = tk.Button(self, text="stop", font=('Arial', 18), width=10, height=1)
        self.stop_button.pack(pady=1000)

        # button click functions
        self.start_button.config(command=self.start_button_click)
        self.stop_button.config(command=self.stop_button_click)
        self.mute_button.config(command=self.mute_button_click)
        self.nothing.config(command=self.nothing_click)

        # Center the timer frame within the parent container
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.place(relx=0.5, rely=0.5, anchor="center")

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        second = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 10)  # Calculate milliseconds
        # print(hours, minutes, seconds, milliseconds)
        return f"{hours:02d}:{minutes:02d}:{second:02d}.{milliseconds:01d}"

    def update_time(self):
        if self.is_running:
            remaining_time = self.duration - (datetime.datetime.now() - self.start_time).total_seconds()
            if remaining_time <= 0:
                self.is_running = False
                self.start_button.config(text="Start")
                self.time_label.config(text=self.format_time(0))
                if not self.mute:
                    pygame.mixer.music.load("../sound/alarm.mp3")
                    pygame.mixer.music.play()
            else:
                self.time_label.config(text=self.format_time(float(remaining_time)))
                self.after(100, self.update_time)

    def start_button_click(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="start")
        else:
            self.duration = int(self.duration_entry.get())
            self.start_time = datetime.datetime.now()
            self.is_running = True
            self.start_button.config(text="stop")
            self.update_time()

    def stop_button_click(self):
        self.is_running = False
        self.start_button.config(text="start")
        self.mute_button.config(text="mute")
        self.time_label.config(text=self.format_time(0))

    def mute_button_click(self):
        self.mute = not self.mute
        if self.mute:
            self.mute_button.config(text="unmute")
        else:
            self.mute_button.config(text="mute")

    def nothing_click(self):
        url = "https://www.youtube.com/watch?v=E4WlUXrJgy4"
        os.system("start " + url)




class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # PageTwo content
        label = tk.Label(self, text="This is Page Two", font=("Arial", 16))
        label.pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()