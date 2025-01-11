import shutil
import requests
import sys
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import messagebox,PhotoImage,font,Entry

#from tkinter import after
#To Fetch Database Names
def DB_names():
    file_path = "desktop/NED DBMS/DB_names.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    return []
# Function to handle the input of fields in sequence
def enter_fields(num_of_fields, database_name, password, field_details=[]):
    if len(field_details) >= num_of_fields:
        # Save database details and fields to files when all fields are entered
        save_database(database_name, password, field_details)
        return

    # Create a new window for each field entry
    field_window = tk.Tk()
    field_window.title(f"Enter Field {len(field_details) + 1}")
    field_window.geometry("300x200")

    # Function to handle field submission
    def submit_field():
        field_name = field_name_entry.get()
        field_length = field_length_entry.get()
        if field_name and field_length.isdigit():
            field_details.append({"field_name": field_name, "length": int(field_length)})
            field_window.destroy()
            # Open the next field entry window
            enter_fields(num_of_fields, database_name, password, field_details)
        else:
            messagebox.showerror("Invalid Input", "Please enter valid field name and length (as a number).")

    # Widgets for field input
    tk.Label(field_window, text=f"Enter name for field {len(field_details) + 1}:").pack(pady=5)
    field_name_entry = tk.Entry(field_window, width=30)
    field_name_entry.pack(pady=5)

    tk.Label(field_window, text="Enter maximum length for this field:").pack(pady=5)
    field_length_entry = tk.Entry(field_window, width=30)
    field_length_entry.pack(pady=5)

    tk.Button(field_window, text="Submit", command=submit_field, width=15).pack(pady=5)

    field_window.mainloop()

# Function to save database and its fields
def save_database(database_name, password, field_details):
    # Create the database folder
    db_folder = f"desktop/NED DBMS/{database_name}"
    os.makedirs(db_folder, exist_ok=True)

    # Save the password to a file
    with open(os.path.join(db_folder, "password.txt"), "w") as f:
        f.write(password)

    # Save the database fields to a file
    with open(os.path.join(db_folder, "DB_info.txt"), "w") as f:
        f.write(str({"database_name": database_name, "fields": field_details}))

    # Creating DB_records.txt for Record addition
    with open(os.path.join(db_folder,"DB_records.txt"),"w") as w:
        pass
    # Append database name to global list
    with open("desktop/NED DBMS/DB_names.txt", "a") as f:
        f.write(f"{database_name}\n")

    messagebox.showinfo("Success", f"Database '{database_name}' created successfully!")

# Function to create a new database
def create_database():
    create_db_window = tk.Tk()
    create_db_window.title("Create Database")
    create_db_window.geometry("400x300")

    # Function to handle database creation
    def submit_database():
        database_name = db_name_entry.get()
        password = db_password_entry.get()
        num_of_fields = num_fields_entry.get()

        if database_name and password and num_of_fields.isdigit():
            if find_database(database_name):
                messagebox.showerror("Error", f"Database '{database_name}' already exists!")
            else:
                create_db_window.destroy()
                enter_fields(int(num_of_fields), database_name, password)
        else:
            messagebox.showerror("Invalid Input", "Please provide valid inputs.")

    # Widgets for database creation
    tk.Label(create_db_window, text="Enter Database Name:").pack(pady=10)
    db_name_entry = tk.Entry(create_db_window, width=30)
    db_name_entry.pack(pady=5)

    tk.Label(create_db_window, text="Enter Password:").pack(pady=10)
    db_password_entry = tk.Entry(create_db_window, width=30, show="*")
    db_password_entry.pack(pady=5)

    tk.Label(create_db_window, text="Enter Number of Fields:").pack(pady=10)
    num_fields_entry = tk.Entry(create_db_window, width=30)
    num_fields_entry.pack(pady=5)

    tk.Button(create_db_window, text="Submit", command=submit_database, width=15).pack(pady=20)

    create_db_window.mainloop()

# Function to check if a database exists
def find_database(database_name):
    db_names_path = "desktop/NED DBMS/DB_names.txt"
    if os.path.exists(db_names_path):
        with open(db_names_path, "r") as file:
            if database_name in file.read().splitlines():
                return True
    return False

def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download&confirm=1"

    session = requests.Session()

    response = session.get(URL, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def main():
    if len(sys.argv) >= 3:
        file_id = sys.argv[1]
        destination = sys.argv[2]
    else:
        file_id = "1blXS-1qBhKFZ6DWXoUboHrjdJb0b-o1h"
        destination = "desktop/image.png"
    print(f"dowload {file_id} to {destination}")
    download_file_from_google_drive(file_id, destination)


if not os.path.exists("desktop/image.png"):
    main()
else:
    pass

r1=tk.Tk()
r1.geometry("900x600")
r1.title("NED DBMS")
photo=PhotoImage(file="desktop/image.png")
image_label=tk.Label(r1,image=photo)
image_label.pack(pady=20)
def Exit_main():
    r1.destroy()

def List_Database():
    DB_names_path= "Desktop/NED DBMS/DB_names.txt"
    # Check if the DB_names.txt file exists
    if not os.path.exists(DB_names_path):
        messagebox.showerror("Error", "DB_names.txt file not found.")
        return

    # Read database names from the file
    with open(DB_names_path, "r") as f:
        databases = [line.strip() for line in f.readlines()]

    if not databases:
        messagebox.showinfo("Info", "No databases available to display.")
        return

    # Create the Treeview Window
    list_db_window = tk.Tk()
    list_db_window.title("List of Databases")
    list_db_window.geometry("400x300")

    tk.Label(list_db_window, text="Available Databases", font=("Arial", 14)).pack(pady=10)

    # Create a Treeview widget
    tree = ttk.Treeview(list_db_window, columns=("Database"), show="headings", height=10)
    tree.heading("Database", text="Database Name")
    tree.column("Database", width=350, anchor="center")
    tree.pack(pady=10)

    # Insert database names into the Treeview
    for db_name in databases:
        tree.insert("", "end", values=(db_name,))

    # Add an Exit button
    tk.Button(list_db_window, text="Exit", command=list_db_window.destroy, width=10).pack(pady=20)

    list_db_window.mainloop()


def Delete_database():
    """
    Function to Delete in Database file.
        """
    DB_names_path= "desktop/NED DBMS/DB_names.txt"
    if not os.path.exists(DB_names_path):
        messagebox.showerror("Error", "DB_names.txt file not found. Cannot Delete Database.")
        return

    def load_names():
        with open(DB_names_path, "r") as file:
            return [line.strip() for line in file]

    def save_records(updated_DB):
        with open(DB_names_path, "w") as file:
            for DB in updated_DB:
                file.write(str(DB) + "\n")    
    
    All_DB_names = load_names()

    if not All_DB_names:
        messagebox.showinfo("Info", "No Databases found to Delete.")
        return

    def Delete_Database(selected_index):
        database_folder_path= f"desktop/NED DBMS/{All_DB_names[selected_index]}"
        try:
            shutil.rmtree(database_folder_path)
            messagebox.showinfo("Success",f"Directory {All_DB_names[selected_index]} deleted successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error","The directory does not exist.")
        except PermissionError:
            messagebox.showwarning("Permission Denied","You do not have permission to delete this directory.")
        except Exception as e:
            messagebox.showerror("Error",f"An error occurred: {e}")
        del All_DB_names[selected_index]
        save_records(All_DB_names)
        
    def select_Database_to_Delete():
        selected_line = line_entry.get()

        if selected_line.isdigit():
            selected_index = int(selected_line) - 1
            if 0 <= selected_index < len(All_DB_names):
                Delete_window.destroy()
                Delete_Database(selected_index)
            else:
                messagebox.showerror("Error", "Invalid line number.")
        else:
            messagebox.showerror("Error", "Please enter a valid line number.")

    Delete_window = tk.Tk()
    Delete_window.title("Delete Database")
    Delete_window.geometry("500x400")

    tk.Label(Delete_window, text="Available Databases:", font=("Arial", 12)).pack(pady=10)

    for i, names in enumerate(All_DB_names, start=1):
        tk.Label(Delete_window, text=f"{i}: {names}").pack(anchor="w", padx=20)

    tk.Label(Delete_window, text="Enter line number to Delete:").pack(pady=10)
    line_entry = tk.Entry(Delete_window, width=10)
    line_entry.pack(pady=5)

    tk.Button(Delete_window, text="Select", command=select_Database_to_Delete, width=10).pack(pady=20)

    Delete_window.mainloop()

def HELP():
    if os.path.exists("Desktop/NED DBMS/HELP.txt"):
        Help_window=tk.Tk()
        Help_window.geometry("450x250")
        tk.Label(Help_window,text=open("Desktop/NED DBMS/HELP.txt","r").read()).pack()
        Help_window.mainloop()
    else:
        messagebox.showerror("Error", "HELP.txt file does not exists!. please paste given HELP file to NED DBMS Folder.")
def Open_database():
    # Exit to main window
    def Exit():
        Options_menu.destroy()

    # Fetch all existing database names (mocking the DB_names function)
    database_names = []
    for db_name in DB_names():
        database_names.append(db_name)

    # Check for any databases available
    if not database_names:
        messagebox.showwarning("No Databases","No databases available. Please create a database first.")
        return

    # Create the default window
    Options_menu = tk.Tk()
    Options_menu.title("Existing Databases")
    Options_menu.geometry('300x250')

    # Create a frame inside the window
    Options_frame = tk.Frame(Options_menu, height=200, width=200, bg="#FFFFC5")
    Options_frame.pack(pady=10)
    #Label for instruction
    tk.Label(Options_frame,text="Select From Avaliable Databases",bg="#FFFFC5").place(x=15,y=2)
    # Create the list of options
    Options_list = database_names.copy()

    # Variable to keep track of the option selected in OptionMenu
    value_inside = tk.StringVar()

    # Set the default value of the variable
    value_inside.set("Database")

    # Create the OptionMenu widget and pass the options_list and value_inside to it
    custom_font = font.Font(family="Arial", size=8) 
    question_menu = tk.OptionMenu(Options_frame, value_inside, *Options_list)
    question_menu.config(font=custom_font, width=14, height=1)
    menu=question_menu["menu"]
    menu.config(font=custom_font)
    question_menu.place(x=20, y=60)


    # Function to handle the submit button action
    def print_answers():
        # Password Window
        def Password_Window():
            password_window = tk.Tk()
            password_window.geometry("400x200")
            tk.Label(password_window, text=f"Enter password for database {selected_db}:", font=("Arial", 12)).pack(pady=20)

            # Define a proper Entry widget
            password_entry = tk.Entry(password_window, show="*")
            password_entry.pack(pady=20)
            
            def Features_window():
                if os.path.exists(DB_info_path) and os.path.exists(DB_record_path):
                    def submit_button_clicked():
                        # Fetching Fields And Their Lengths From DB_info.txt  
                        field_read=open(DB_info_path,"r").read()
                        database_info=eval(field_read)
                        field_details=database_info["fields"]

                        
                        # To Add Record
                        def Add_Record(field_details, DB_record_path):
                            # Check if the records file exists
                            if not os.path.exists(DB_record_path):
                                messagebox.showerror("Error", "DB_records.txt file not found. Cannot add records.")
                                return

                            def save_and_continue():
                                record = {}
                                for field, entry in zip(field_details, entries):
                                    field_name = field['field_name']
                                    field_value = entry.get()
                                    if len(field_value) > field['length']:
                                        messagebox.showerror("Error", f"Value for '{field_name}' exceeds maximum length of {field['length']}.")
                                        return
                                    record[field_name] = field_value

                                with open(DB_record_path, "a") as f:
                                    f.write(str(record) + "\n")

                                messagebox.showinfo("Success", "Record added successfully!")
                                for entry in entries:
                                    entry.delete(0, tk.END)

                            def exit_window():
                                add_record_window.destroy()

                            # Create the Add Record Window
                            add_record_window = tk.Tk()
                            add_record_window.title("Add Record")
                            add_record_window.geometry("500x400")

                            tk.Label(add_record_window, text="Add Records for Fields", font=("Arial", 14)).pack(pady=10)

                            entries = []

                            # Create input fields dynamically based on field details
                            for field in field_details:
                                field_name = field['field_name']
                                tk.Label(add_record_window, text=f"{field_name} (Max {field['length']} chars):").pack(pady=5)
                                entry = tk.Entry(add_record_window, width=40)
                                entry.pack(pady=5)
                                entries.append(entry)

                            # Buttons for Save and Exit
                            button_frame = tk.Frame(add_record_window)
                            button_frame.pack(pady=20)

                            tk.Button(button_frame, text="Save and Add Another", command=save_and_continue, width=20).grid(row=0, column=0, padx=10)
                            tk.Button(button_frame, text="Exit", command=exit_window, width=10).grid(row=0, column=1, padx=10)

                            add_record_window.mainloop()

                        def Show_Records(db_folder, field_details):
                            """
                                Displays records from the database in a Treeview widget.

                                Args:
                                db_folder (str): Path to the database folder.
                                field_details (list): List of dictionaries containing field details.
                                """

                            # Open the records file
                            try:
                                with open(os.path.join(db_folder, "DB_records.txt"), "r") as records_file:
                                    records = [eval(line.strip()) for line in records_file]
                            except FileNotFoundError:
                                print("DB_records.txt file not found. No records to show.")
                                return

                            # Create the Treeview window
                            records_window = tk.Tk()
                            records_window.title("Database Records")

                            # Create the Treeview widget
                            tree = ttk.Treeview(records_window, columns=[field["field_name"] for field in field_details])

                            # Set the column headings
                            for field in field_details:
                                tree.heading(field["field_name"], text=field["field_name"])

                            # Insert records into the Treeview
                            for record in records:
                                tree.insert("", tk.END, values=list(record.values()))

                            # Display the Treeview
                            tree.pack(pady=20)

                            # Add a button to close the window
                            close_button = tk.Button(records_window, text="Close", command=records_window.destroy)
                            close_button.pack(pady=20)

                            records_window.mainloop()

                        def Update_Records(db_folder, field_details):
                            """
                            Function to update records in DB_records.txt file.

                            Args:
                                db_folder (str): Path to the database folder.
                                field_details (list): List of dictionaries containing field details.
                                """
                            records_file_path = os.path.join(db_folder, "DB_records.txt")

                            if not os.path.exists(records_file_path):
                                messagebox.showerror("Error", "DB_records.txt file not found. Cannot update records.")
                                return

                            def load_records():
                                with open(records_file_path, "r") as file:
                                    return [eval(line.strip()) for line in file]

                            def save_records(updated_records):
                                with open(records_file_path, "w") as file:
                                    for record in updated_records:
                                        file.write(str(record) + "\n")

                            records = load_records()

                            if not records:
                                messagebox.showinfo("Info", "No records found to update.")
                                return

                            def update_record(selected_index):
                                selected_record = records[selected_index]

                                def save_and_close():
                                    for field, entry in zip(field_details, entries):
                                        new_value = entry.get()
                                        if len(new_value) > field['length']:
                                            messagebox.showerror("Error", f"Value for '{field['field_name']}' exceeds max length {field['length']}.")
                                            return
                                        if new_value.strip():
                                            selected_record[field['field_name']] = new_value

                                    records[selected_index] = selected_record
                                    save_records(records)
                                    messagebox.showinfo("Success", "Record updated successfully!")
                                    update_window.destroy()

                                update_window = tk.Tk()
                                update_window.title("Update Record")
                                update_window.geometry("400x400")

                                entries = []

                                for field in field_details:
                                    tk.Label(update_window, text=f"{field['field_name']} (Current: {selected_record.get(field['field_name'], '')}):").pack(pady=5)
                                    entry = tk.Entry(update_window, width=40)
                                    entry.pack(pady=5)
                                    entries.append(entry)

                                tk.Button(update_window, text="Save", command=save_and_close, width=10).pack(pady=20)

                                update_window.mainloop()

                            def select_record_to_update():
                                selected_line = line_entry.get()

                                if selected_line.isdigit():
                                    selected_index = int(selected_line) - 1
                                    if 0 <= selected_index < len(records):
                                        update_window.destroy()
                                        update_record(selected_index)
                                    else:
                                        messagebox.showerror("Error", "Invalid line number.")
                                else:
                                    messagebox.showerror("Error", "Please enter a valid line number.")

                            update_window = tk.Tk()
                            update_window.title("Update Records")
                            update_window.geometry("500x400")

                            tk.Label(update_window, text="Available Records:", font=("Arial", 12)).pack(pady=10)

                            for i, record in enumerate(records, start=1):
                                tk.Label(update_window, text=f"{i}: {record}").pack(anchor="w", padx=20)

                            tk.Label(update_window, text="Enter line number to update:").pack(pady=10)
                            line_entry = tk.Entry(update_window, width=10)
                            line_entry.pack(pady=5)

                            tk.Button(update_window, text="Select", command=select_record_to_update, width=10).pack(pady=20)

                            update_window.mainloop()
                         
                        def Delete_Record(db_folder, field_details):
                            """
                            Function to update records in DB_records.txt file.

                            Args:
                                db_folder (str): Path to the database folder.
                                field_details (list): List of dictionaries containing field details.
                                """
                            records_file_path = os.path.join(db_folder, "DB_records.txt")

                            if not os.path.exists(records_file_path):
                                messagebox.showerror("Error", "DB_records.txt file not found. Cannot update records.")
                                return

                            def load_records():
                                with open(records_file_path, "r") as file:
                                    return [eval(line.strip()) for line in file]

                            def save_records(updated_records):
                                with open(records_file_path, "w") as file:
                                    for record in updated_records:
                                        file.write(str(record) + "\n")
                                messagebox.showinfo("Success","Record Deleted Successfully")

                            records = load_records()

                            if not records:
                                messagebox.showinfo("Info", "No records found to update.")
                                return

                            def Delete_record(selected_index):
                                del records[selected_index]
                                save_records(records)
                                
                            def select_record_to_Delete():
                                selected_line = line_entry.get()

                                if selected_line.isdigit():
                                    selected_index = int(selected_line) - 1
                                    if 0 <= selected_index < len(records):
                                        Delete_window.destroy()
                                        Delete_record(selected_index)
                                    else:
                                        messagebox.showerror("Error", "Invalid line number.")
                                else:
                                    messagebox.showerror("Error", "Please enter a valid line number.")

                            Delete_window = tk.Tk()
                            Delete_window.title("Update Records")
                            Delete_window.geometry("500x400")

                            tk.Label(Delete_window, text="Available Records:", font=("Arial", 12)).pack(pady=10)

                            for i, record in enumerate(records, start=1):
                                tk.Label(Delete_window, text=f"{i}: {record}").pack(anchor="w", padx=20)

                            tk.Label(Delete_window, text="Enter line number to Delete:").pack(pady=10)
                            line_entry = tk.Entry(Delete_window, width=10)
                            line_entry.pack(pady=5)

                            tk.Button(Delete_window, text="Select", command=select_record_to_Delete, width=10).pack(pady=20)

                            Delete_window.mainloop()
                         
                        def Search_Record(db_folder, field_details):
                            """
                            Search for specific records in the database and display them in a Treeview.
    
                            Args:
                            db_folder (str): Path to the database folder.
                            field_details (list): List of dictionaries containing field details.
                            """
                            records_file_path = os.path.join(db_folder, "DB_records.txt")
    
                            # Load records from the file
                            try:
                                with open(records_file_path, "r") as records_file:
                                    records = [eval(line.strip()) for line in records_file]
                            except FileNotFoundError:
                                messagebox.showerror("Error", "DB_records.txt file not found. Cannot search records.")
                                return

                            # Create the Search Record Window
                            search_window = tk.Tk()
                            search_window.title("Search Records")
                            search_window.geometry("800x600")
    
                            # Search frame
                            search_frame = tk.Frame(search_window)
                            search_frame.pack(pady=10)

                            tk.Label(search_frame, text="Search by Field:").pack(side=tk.LEFT, padx=5)

                            # Dropdown for field selection
                            field_var = tk.StringVar(search_window)
                            field_var.set(field_details[0]['field_name'])  # Default to first field
                            field_dropdown = ttk.Combobox(search_frame, textvariable=field_var, values=[f['field_name'] for f in field_details])
                            field_dropdown.pack(side=tk.LEFT, padx=5)

                            # Entry box for search value
                            search_entry = tk.Entry(search_frame, width=30)
                            search_entry.pack(side=tk.LEFT, padx=5)

                            # Treeview to display records
                            columns = [field['field_name'] for field in field_details]
                            tree = ttk.Treeview(search_window, columns=columns, show="headings")
                            for column in columns:
                                tree.heading(column, text=column)
                                tree.column(column, anchor=tk.W, width=150)
                            tree.pack(pady=20, fill=tk.BOTH, expand=True)

                            # Function to update the Treeview with search results
                            def update_treeview(search_field, search_value):
                                # Clear the Treeview
                                for row in tree.get_children():
                                    tree.delete(row)

                                # Filter and display matching records
                                for record in records:
                                    if search_field in record and search_value.lower() in str(record[search_field]).lower():
                                        tree.insert("", tk.END, values=[record.get(field['field_name'], "") for field in field_details])

                            # Search button functionality
                            def search_records():
                                search_field = field_var.get()
                                search_value = search_entry.get().strip()
                                if search_value:
                                    update_treeview(search_field, search_value)
                                else:
                                    messagebox.showwarning("Warning", "Please enter a value to search.")

                            # Reset button functionality
                            def reset_treeview():
                                search_entry.delete(0, tk.END)
                                update_treeview("", "")  # Reload all records

                            # Buttons for searching and resetting
                            tk.Button(search_frame, text="Search", command=search_records, width=10).pack(side=tk.LEFT, padx=5)
                            tk.Button(search_frame, text="Reset", command=reset_treeview, width=10).pack(side=tk.LEFT, padx=5)

                            # Initial load of all records
                            update_treeview("", "")

                            # Run the search window main loop
                            search_window.mainloop()


                        selected_option = selected_option_var.get()
                        if selected_option=="1":
                            Add_Record(field_details, DB_record_path)
                        elif selected_option=="2":
                            Show_Records(db_folder, field_details)
                        elif selected_option=="3":
                            Update_Records(db_folder, field_details)
                        elif selected_option=="4":
                            Delete_Record(db_folder,field_details)
                        elif selected_option=="5":
                            Search_Record(db_folder, field_details)
                        else:
                            messagebox.showwarning("Warning", "Please select an option!")

                    def exit_button_clicked():
                        features_window.destroy()

                    # Create the main window
                    features_window = tk.Tk()
                    features_window.title("Database Features")
                    features_window.geometry("350x350")

                    # Create a frame with a specific background color
                    frame = tk.Frame(features_window, bg="#FFFFC5")
                    frame.pack(padx=20, pady=20)

                    # Add a label
                    tk.Label(frame, text="Select Features From Database", bg="#FFFFC5").pack(pady=5)

                    # Create a StringVar to hold the selected option
                    selected_option_var = tk.StringVar(frame,"")

                    # Create Radiobuttons within the frame
                    options = {"Add_Record":"1", "Show_Record":"2", "Update_Record":"3", "Delete_Record":"4", "Search_Record":"5"}
                    for (text,value) in options.items():
                        radiobutton = tk.Radiobutton(frame,text=text,variable=selected_option_var,value=value,bg="#FFFFC5",font=("Ariel", 16),padx=10,pady=5)
                        radiobutton.pack(anchor="w")

                    # Create Submit and Exit buttons
                    submit_button = tk.Button(features_window, text="Submit", command=submit_button_clicked, width=8, height=2)
                    submit_button.place(x=80, y=300)

                    exit_button = tk.Button(features_window, text="Exit", command=exit_button_clicked, width=8, height=2)
                    exit_button.place(x=210, y=300)

                    # Run the main loop
                    features_window.mainloop()
                else:
                    messagebox.showerror("Error", "'DB_info.txt' OR 'DB_record.txt' doesn't Exist")


            def submit():
                entered_password = password_entry.get()
                if entered_password:
                    if os.path.exists(password_path):
                        stored_password = open(password_path, "r").read().strip()
                        if entered_password == stored_password:
                            messagebox.showinfo("Success", f"Access Confirmed. Opening Database {selected_db}")
                            password_window.after(500,lambda:[password_window.destroy(),Features_window()])
                        else:
                            messagebox.showerror("Error", "Access Denied. Incorrect Password.")
                    else:
                        messagebox.showerror("Error", "Password file doesn't exist.")
                else:
                    messagebox.showerror("Error", "Please enter a password.")

            # Submit Button for Password Window
            tk.Button(password_window, text="Submit", command=submit, width=8, height=2).pack(pady=20)
            password_window.mainloop()

        # Check if the selected option exists in the database names
        selected_db = value_inside.get()
        if selected_db not in database_names:
            messagebox.showerror("Error", f"Database '{selected_db}' does not exist.")
            return

        # Define the folder and file paths for the selected database
        db_folder = f"desktop/NED DBMS/{selected_db}"
        password_path = os.path.join(db_folder, "password.txt")
        DB_info_path = os.path.join(db_folder, "DB_info.txt")
        DB_record_path= os.path.join(db_folder,"DB_records.txt")
        
        # Check if the password file exists
        if not os.path.exists(password_path):
            messagebox.showerror("Error", "Password file is missing. Cannot open database.")
            Exit()
        else:
            messagebox.showinfo("Success", f"Database '{selected_db}' is ready to use!")
            Options_menu.after(500, lambda: [Options_menu.destroy(), Password_Window()])

    # Create the Submit button
    submit_button = tk.Button(Options_frame, text='Enter', command=print_answers, width=8, height=2)
    submit_button.place(x=120, y=120)

    # Create Exit Button
    Exit_button = tk.Button(Options_frame, text="Exit", command=Exit, width=8, height=2)
    Exit_button.place(x=20, y=120)

    # Function to update and display the selected option
    def update_selection(*args):
        print(f"Selected Option: {value_inside.get()}")

    # Bind the StringVar to the function
    value_inside.trace("w", update_selection)

    # Start the main event loop
    Options_menu.mainloop()
    
    Open_window.mainloop()

F1=tk.Frame(r1,height=350,width=700,bg="#FFFFC5")
F1.pack(side="bottom",pady=30)
B1=tk.Button(F1,text="Create New Database",command=create_database,width=25,height=2)
B1.grid(row=0,column=0,padx=20,pady=20)
B2=tk.Button(F1,text="Open Existing Databases",command=Open_database,width=25,height=2)
B2.grid(row=0,column=1,padx=20,pady=20)
B3=tk.Button(F1,text="HELP File",command=HELP,width=25,height=2)
B3.grid(row=1,column=0,padx=20,pady=20)
B4=tk.Button(F1,text="Delete Existing Database",command=Delete_database,width=25,height=2)
B4.grid(row=1,column=1,padx=20,pady=20)
B5=tk.Button(F1,text="Exit",command=Exit_main,width=25,height=2) 
B5.grid(row=3,column=1,padx=20,pady=20)
B6=tk.Button(F1,text="List Databases",command=List_Database,width=25,height=2) 
B6.grid(row=3,column=0,padx=20,pady=20)


r1.mainloop()
