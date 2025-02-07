import os
import shutil


def backup_py_to_txt(py_file_path, backup_dir="backups"):
    try:
        # Check if the .py file exists
        if not os.path.exists(py_file_path):
            print(f"Error: File '{py_file_path}' not found.")
            return None

        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)  # Create directory and any necessary parent directories.

        # Construct the backup file path
        py_file_name = os.path.basename(py_file_path)
        backup_file_name = os.path.splitext(py_file_name)[0] + ".txt"
        backup_file_path = os.path.join(backup_dir, backup_file_name)

        # Copy the contents of the .py file to the .txt file
        shutil.copyfile(py_file_path, backup_file_path)

        print(f"File '{py_file_path}' backed up to '{backup_file_path}' successfully.")
        return backup_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


py_file = "final UI.py"
backup_location = os.getcwd()  # !!! get the current directory !!!
backup_file_path = backup_py_to_txt(py_file, backup_location)

if backup_file_path:
    print(f"Backup created at: {backup_file_path}")
else:
    print("Backup failed.")
