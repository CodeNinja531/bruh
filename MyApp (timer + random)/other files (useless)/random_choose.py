import random
import tkinter as tk
from tkinter import messagebox
import sqlite3


def initial():
    """
    Creates a table named 'names' with a single 'name' column and inserts 10 sample names.
    Checks if the table already exists before creating it.
    """
    conn = sqlite3.connect('../database/names.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM names")
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE names (name TEXT)''')

        names = ['Frank', 'Jeffery', 'Casper', 'Jaden']
        cursor.executemany("INSERT INTO names (name) VALUES (?)", [(name,) for name in names])

    conn.commit()
    conn.close()

def retrieve():
    """
    Retrieve all names from the 'names' table and returns them as a Python list.
    """
    conn = sqlite3.connect('../database/names.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM names")
    names = cursor.fetchall()
    names_list = [name[0] for name in names]

    conn.close()
    return names_list


def update_db(data_list):
  """
  Replaces the entire 'names' table with the provided list of names.
  """
  conn = sqlite3.connect('../database/names.db')
  cursor = conn.cursor()

  # Delete existing data
  cursor.execute("DELETE FROM names")

  # Insert new data
  cursor.executemany("INSERT INTO names (name) VALUES (?)", [(name,) for name in data_list])

  conn.commit()
  conn.close()


# Create table and insert data
initial()


def stark():
    text = text_widget.get("1.0", tk.END)
    text_list = text.split("\n")
    filtered_list = [line.strip() for line in text_list if line.strip()]
    update_db(filtered_list)
    # number of random results
    num_results = entry_widget.get()
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


window = tk.Tk()
window.title("Random choose")
window.configure(bg='white', width=800, height=600,)
text_widget = tk.Text(window, width=40, height=10)

# initial
initial_list = retrieve()
for name in initial_list:
    text_widget.insert(tk.END, name + "\n")

text_widget.pack()

# label
label_widget = tk.Label(window, text="Amount to be chosen：")
label_widget.pack()
entry_widget = tk.Entry(window)
entry_widget.pack()

# button
button_widget = tk.Button(window, text="choose", command=stark)
button_widget.pack()


window.mainloop()
