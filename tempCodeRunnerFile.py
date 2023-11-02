import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import mysql.connector

# Function to add a new manager and clear input fields
def add_manager():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not (site and username and password):
        messagebox.showerror("Error", "All fields are required!")
        return

    # Connect to the MySQL database
    con = mysql.connector.connect(host="localhost", user="root", passwd="Techno$pider2099", database="user_info")
    myc = con.cursor()

    # Check if the manager already exists
    myc.execute("SELECT * FROM login WHERE Site=%s AND Username=%s", (site, username))
    existing_record = myc.fetchone()

    if existing_record:
        messagebox.showerror("Error", "Manager already exists!")
    else:
        # Insert the new manager record into the database
        myc.execute("INSERT INTO login (Site, Username, Password) VALUES (%s, %s, %s)", (site, username, password))
        con.commit()
        messagebox.showinfo("Success", "Manager added successfully!")

        # Clear input fields
        site_entry.delete(0, "end")
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")

    con.close()

# Create the main window
root = tk.Tk()
root.title("Add Manager")
root.geometry("400x250")
root.configure(bg='#232323')  # Dark background color

# Empty rows and columns for centering
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
for i in range(2):
    root.grid_columnconfigure(i, weight=1)

# Heading
heading = Label(root, text="Add Manager", bg='#232323', fg='white', font=('Arial', 20))
heading.grid(row=1, column=0, columnspan=2, pady=10)

# Labels
site_label = Label(root, text="Site Number:", bg='#232323', fg='white', font=('Arial', 12))
username_label = Label(root, text="Username:", bg='#232323', fg='white', font=('Arial', 12))
password_label = Label(root, text="Password:", bg='#232323', fg='white', font=('Arial', 12))

# Entry fields
site_entry = Entry(root, font=('Arial', 12))
username_entry = Entry(root, font=('Arial', 12))
password_entry = Entry(root, show="*", font=('Arial', 12))  # Show password as asterisks

# Add button
add_button = Button(root, text="Add", command=add_manager, font=('Arial', 12))

# Grid layout for labels and entry fields
site_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
site_entry.grid(row=2, column=1, padx=10, pady=5)
username_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
username_entry.grid(row=3, column=1, padx=10,  pady=5)
password_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
password_entry.grid(row=4, column=1, padx=10, pady=5)

# Add button
add_button.grid(row=5, column=0, columnspan=2, pady=10)

# Run the tkinter main loop
root.mainloop()
