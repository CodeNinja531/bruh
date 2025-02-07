import tkinter as tk
from tkinter import ttk
from tkinter import Menu, messagebox
import pygame
import datetime
import random
import sqlite3
import os
import math


# Database iz here
class db:
    """
    Very fun database thing
    """
    def __init__(self):
        """Initialize the database connection and ensure the table exists."""
        self.conn = sqlite3.connect('database/names.db')
        self.cursor = self.conn.cursor()
        self.create_default()

    def create_default(self):
        # create many tables
        # ICT
        try:
            self.cursor.execute("SELECT item FROM S5ICT")
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE S5ICT (item TEXT)''')
            students = ['Frank', 'Jeffery', 'Casper', 'Jaden', 'Harry', 'Oscar', 'Matos', ]
            self.cursor.executemany("INSERT INTO S5ICT (item) VALUES (?)", [(student,) for student in students])
            self.conn.commit()

        # teacher
        try:
            self.cursor.execute("SELECT item FROM teachers")
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE teachers (item TEXT)''')
            teachers = ['Mr. Hui', 'Our dearest Mr. Hui', 'Handsome Mr. Hui', 'Angry Mr. Hui']
            self.cursor.executemany("INSERT INTO teachers (item) VALUES (?)", [(teacher,) for teacher in teachers])
            self.conn.commit()

        # numbers(1-10)
        try:
            self.cursor.execute("SELECT item FROM \"numbers(1-10)\"")
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE "numbers(1-10)" (item TEXT)''')
            numbers = list(range(1, 11))
            self.cursor.executemany("INSERT INTO \"numbers(1-10)\" (item) VALUES (?)",
                                    [(num,) for num in numbers])
            self.conn.commit()

        # numbers(1-30)
        try:
            self.cursor.execute("SELECT item FROM \"numbers(1-30)\"")
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE "numbers(1-30)" (item TEXT)''')
            numbers = list(range(1, 31))
            self.cursor.executemany("INSERT INTO \"numbers(1-30)\" (item) VALUES (?)",
                                    [(num,) for num in numbers])
            self.conn.commit()

        # genshin
        try:
            self.cursor.execute("SELECT item FROM Genshin")
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE Genshin (item TEXT)''')
            genshin_list = ["HuTao", "Furina", "Naganohara Yoimiya", "Yae Miko", "ShenHe", "Raiden Shogun", "Kamisato Ayaka", ]
            self.cursor.executemany("INSERT INTO Genshin (item) VALUES (?)",
                                    [(i,) for i in genshin_list])
            self.conn.commit()

        # <custom>
        try:
            self.cursor.execute("SELECT item FROM \"<custom>\"")
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE "<custom>" (item TEXT)''')

    def retrieve(self, table):
        # Retrieve all names from the 'names' table.
        self.cursor.execute(f"SELECT item FROM \"{table}\"")
        names = self.cursor.fetchall()
        return [name[0] for name in names]

    def update(self, data_list, table):
        """Replace all entries in the 'names' table with the provided list of names."""
        self.cursor.execute(f"DELETE FROM \"{table}\"")
        self.cursor.executemany(f"INSERT INTO \"{table}\" (item) VALUES (?)", [(name,) for name in data_list])
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()


# APP --------------------------------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("This is just a title")
        self.geometry("420x400")

        # Initialize pygame for sound
        pygame.init()

        # Initialize container for pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to hold pages
        self.pages = {}

        # Add pages to the container
        for Page in (timer, Random, BuyCoffee, help):
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
        menu_bar.add_cascade(label="Tools", menu=pages_menu)
        menu_bar.add_command(label="Help", command=lambda: self.show_page("help"))

        # Add items to switch between pages
        pages_menu.add_command(label="Timer", command=lambda: self.show_page("timer"))
        pages_menu.add_command(label="Random Chooser", command=lambda: self.show_page("Random"))
        pages_menu.add_command(label="Buy me a coffee", command=lambda: self.show_page("BuyCoffee"))

    def show_page(self, page_name):
        # Bring page to the front
        page = self.pages[page_name]
        page.tkraise()
        self.title("this is just a " + page_name)

        # Set the icon based on the page
        if page_name == "timer":
            self.set_icon("photos/timer.ico")
        elif page_name == "Random":
            self.set_icon("photos/dice.ico")
        elif page_name == "BuyCoffee":
            self.set_icon("photos/wife.ico")
        elif page_name == 'help':
            self.set_icon("photos/help.ico")

    def set_icon(self, icon_path):
        try:
            self.iconbitmap(icon_path)
        except tk.TclError:
            pass


# timer-------------------------------------------------------------------------------
class timer(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Timer variables
        self.is_running = False
        self.start_time = 0
        self.duration = 60
        self.mute = False
        self.tick = 100

        # Timer body
        self.time_label = tk.Label(self, text="00:00:00.0", font=('Arial', 30))
        self.time_label.pack(pady=20)

        # textbox for input
        self.duration_entry = tk.Entry(self, font=('Arial', 16), width=10)
        self.duration_entry.pack(pady=10)
        self.duration_entry.insert(0, "60")

        # textbox reminder
        self.tip_label = tk.Label(self, text="countdown time (s)(integer)", font=('Arial', 10))
        self.tip_label.pack(pady=2)

        # button (start and stop)
        self.start_button = tk.Button(self, text="start", font=('Arial', 18), width=10, height=1)
        self.start_button.pack(pady=16)

        # very nice quiet button
        self.mute_button = tk.Button(self, text="mute", font=('Arial', 15), width=10, height=1)
        self.mute_button.pack(pady=1)

        # Just a funny prank
        self.nothing = tk.Button(self, text="nothing here", font=('Arial', 10), width=16, height=1)
        self.nothing.pack(pady=98)

        # useless (just a decoration)
        self.stop_button = tk.Button(self, text="stop", font=('Arial', 18), width=10, height=1)
        self.stop_button.pack(pady=100)

        # Button click functions(link to function)
        self.start_button.config(command=self.start_button_click)
        self.stop_button.config(command=self.stop_button_click)
        self.mute_button.config(command=self.mute_button_click)
        self.nothing.config(command=self.nothing_click)

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        second = int(seconds % 60)
        small_seconds = int((seconds - int(seconds)) * 10)
        return f"{hours:02d}:{minutes:02d}:{second:02d}.{small_seconds:01d}"

    def update_time(self):
        """
        At certain time interval(self.tick), sync with datetime.
        When remaining_time <= 0, play music
        """
        if self.is_running:
            remaining_time = self.duration - (datetime.datetime.now() - self.start_time).total_seconds()
            if remaining_time <= 0:
                self.is_running = False
                self.start_button.config(text="Start")
                self.time_label.config(text=self.format_time(0))
                if not self.mute:
                    for i in range(3):
                        pygame.mixer.music.load("sound/alarm.mp3")
                        pygame.mixer.music.play()
            else:
                self.time_label.config(text=self.format_time(float(remaining_time)))
                self.after(self.tick, self.update_time)

    def start_button_click(self):
        """
        Change button name to stop/start
        Check time is valid or not
        Start the other functions
        """
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="start")
        else:
            try:
                self.duration = int(math.ceil(eval(self.duration_entry.get())))
            except:
                messagebox.showwarning("Alert", "Time in wrong format")
                self.duration = 60
                self.duration_entry.delete(0, tk.END)
                self.duration_entry.insert(0, "60")
                return
            else:
                if self.duration <= 0 or float(eval(self.duration_entry)) != self.duration:
                    messagebox.showwarning("Alert", "please enter an integer >0")
                    self.duration = 60
                    self.duration_entry.delete(0, tk.END)
                    self.duration_entry.insert(0, "60")
                    return
                
            self.start_time = datetime.datetime.now()
            self.is_running = True
            self.start_button.config(text="stop")
            self.update_time()

    def stop_button_click(self):
        """
        Useless, just for testing and decoration
        """
        self.is_running = False
        self.start_button.config(text="start")
        self.mute_button.config(text="mute")
        self.time_label.config(text=self.format_time(0))

    def mute_button_click(self):
        """
        To mute the oiiaio
        Change the button name to mute/unmute
        """
        self.mute = not self.mute
        if self.mute:
            self.mute_button.config(text="unmute")
        else:
            self.mute_button.config(text="mute")

    def nothing_click(self):
        url = "https://bit.ly/3BlS71b"
        os.system(f"start {url}")


# random--------------------------------------------------------------------------------
class Random(tk.Frame):
    """
    Generate random results according the DB data
    Changeable random list
    Changeable amount of item to be chosen
    Random lists: ['S5ICT', 'teachers', 'numbers(1-10)', 'numbers(1-30)', 'Genshin', '<custom>', ]
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # initialize database
        self.db = db()  # Create an instance of the DB class for database operations

        # Labe reminder
        self.label_widget = tk.Label(self, text="Please enter the items below:")
        self.label_widget.pack(pady=0)

        # Text widget (changeable, for random list edit)
        self.text_widget = tk.Text(self, width=40, height=10)
        self.text_widget.pack(pady=10)

        # Populate initial names
        initial_list = self.db.retrieve('S5ICT')
        for name in initial_list:
            self.text_widget.insert(tk.END, name + "\n")

        # Dropdown list
        self.table_options = ['S5ICT', 'teachers', 'numbers(1-10)', 'numbers(1-30)', 'Genshin', '<custom>', ]
        self.selected_table = tk.StringVar(value=self.table_options[0])

        # Dropdown table setup
        self.table_dropdown = ttk.Combobox(self, textvariable=self.selected_table, values=self.table_options,
                                           state="readonly")
        self.table_dropdown.pack(pady=5)
        self.table_dropdown.current(0)

        # Bind dropdown to function _on_change
        self.table_dropdown.bind("<<ComboboxSelected>>", self._on_dropdown_change)
        self._on_dropdown_change()  # Initialize text widget

        # Entry for number of results
        self.label_widget = tk.Label(self, text="Amount to be chosen:")
        self.label_widget.pack(pady=1)

        self.entry_widget = tk.Entry(self)
        self.entry_widget.pack(pady=5)

        # Button to choose
        self.button_widget = tk.Button(self, text="choose", command=self.choose_random)
        self.button_widget.pack(pady=10)

    def _populate_items(self):
        table = self.selected_table.get()
        original_list = self.db.retrieve(table)
        for name in original_list:
            self.text_widget.insert(tk.END, name + "\n")

    def _on_dropdown_change(self, event=1):
        """
        event: place holder (useless)
        Called when user changes the dropdown option
        """
        if event:
            table = self.selected_table.get()
            data = self.db.retrieve(table)
            self._populate_itmes()
            self.text_widget.delete("1.0", tk.END)
            for item in data:
                self.text_widget.insert(tk.END, item + "\n")

    def choose_random(self):
        """
        When choose button pressed, update the input to DB
        randomly chooses and show result in popup messagebox
        """
        text = self.text_widget.get("1.0", tk.END)
        text_list = text.split("\n")
        filtered_list = [line.strip() for line in text_list if line.strip()]
        
        # update the data to DB
        table = self.selected_table.get()
        if table not in ['numbers(1-10)', 'numbers(1-30)', ]:
            self.db.update(filtered_list, table)

        # Number of random results
        num_results = self.entry_widget.get()
        try:
            num_results = int(num_results)
        except ValueError:
            messagebox.showwarning("Alert", "Please enter an integer")
            return

        if len(filtered_list) > 0:
            if num_results <= len(filtered_list):
                random_elements = random.sample(filtered_list, num_results)
                result_str = "\n".join(random_elements)
                messagebox.showinfo("Result", f"\n{result_str}")
            else:
                messagebox.showwarning("Alert", "Value out of range")
        else:
            messagebox.showwarning("Alert", "Blank list")


# coffee--------------------------------------------------------------------------------------
class BuyCoffee(tk.Frame):
    """
    A page for people to support me
    attatched a cute HuTao (my wife)
    and an alipay collect coin code
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # sentence
        label = tk.Label(self, text="Support the developer with a coffee :)")
        label.pack(pady=20)

        # support button connected to pop screen
        button = tk.Button(self, text="Buy me a coffee", command=self.buy_coffee)
        button.pack(pady=8)

        # HuTao image
        self.coffee_image = tk.PhotoImage(file="photos/hutao.png")
        image_label = tk.Label(self, image=self.coffee_image)
        image_label.pack()

    def buy_coffee(self):
        """
        Popup screen for payment
        When button pressed...
        """
        """
        ------------------ useless original code ------------------------
        url = "https://drive.google.com/file/d/1in5D_qa6Kuk7LTvteFFGD1asNAzJNSum/view?usp=sharing"
        os.system(f"start {url}")
        """
        # make a toplevel popup screen
        popup = tk.Toplevel(self)
        popup.title("gimme some $$$")

        # show alipay code photo
        alipay = tk.PhotoImage(file="photos/alipay.png")
        image_label = tk.Label(popup, image=alipay)
        image_label.pack()


class help(tk.Frame):
    """
    A literally useless help page
    shows some bad jokes
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # text label
        label = tk.Label(self, text="Sorry, there is nothing I can do to help you")
        label.pack(pady=20)

        # Image of Pimon (fun)
        self.paimon = tk.PhotoImage(file="photos/paimon.png")
        image_label = tk.Label(self, image=self.paimon)
        image_label.pack(pady=10)

        # text label above image
        label = tk.Label(self, text="Maybe you need this")
        label.pack()
        
        # arrow pic (small)
        self.arrow = tk.PhotoImage(file="photos/arrow.png")
        image_label = tk.Label(self, image=self.arrow)
        image_label.pack(pady=10)

        # Another prank button for mental help
        button = tk.Button(self, text="Mental support", command=self.support)
        button.pack()
       
    def support(self):
        """
        Shall we talk, shall we talk -- Eason Chan
        """
        url = "https://www.shallwetalk.hk/zh/get-help/online-support/"
        os.system(f"start {url}")


# Start and initialize the App
if __name__ == "__main__":
    app = App()
    app.mainloop()
