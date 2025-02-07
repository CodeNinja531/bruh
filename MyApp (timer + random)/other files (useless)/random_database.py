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

        names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Iris', 'Jack']
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


def update(data_list):
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

# Retrieve data as list
names = retrieve()
print(names)
