import sqlite3
import os
import csv  # Use the csv module for better handling of special characters

def db_to_txt(db_filepath, txt_filepath, delimiter=",", header=True):
    """Exports all tables from a SQLite database to a single text file,
       handling special characters using the csv module.
    """
    try:
        conn = sqlite3.connect(db_filepath)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]

        with open(txt_filepath, 'w', encoding='utf-8', newline='') as txtfile:  # newline='' for consistent line endings
            csv_writer = csv.writer(txtfile, delimiter=delimiter, quoting=csv.QUOTE_NONNUMERIC)  # Use csv writer

            for table_name in table_names:
                try:
                    cursor.execute(f"PRAGMA table_info(\"{table_name}\")")
                    columns_info = cursor.fetchall()
                    column_names = [column[1] for column in columns_info]

                    if header:
                        txtfile.write(f"Table: {table_name}\n")
                        csv_writer.writerow(column_names)  # Write header using csv writer

                    cursor.execute(f"SELECT * FROM \"{table_name}\"")
                    rows = cursor.fetchall()

                    for row in rows:
                        row_str = [str(item) for item in row]  # Convert to string if needed
                        csv_writer.writerow(row_str)  # Use csv writer for data rows

                    txtfile.write("\n")  # Separator between tables

                except sqlite3.Error as e:
                    print(f"SQLite error with table '{table_name}': {e}")
                except Exception as e:
                    print(f"An error occurred with table '{table_name}': {e}")

        print(f"Successfully exported all tables to '{txt_filepath}'")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


# Example Usage (same as before):
db_file = "names.db"
txt_file = "db.txt"

if os.path.exists(db_file):
    db_to_txt(db_file, txt_file)
else:
    print(f"Error: Database file '{db_file}' not found.")