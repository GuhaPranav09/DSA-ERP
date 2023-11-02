def Update_Password(pwd, site_num=1):
    import tkinter as tk
    from tkinter import ttk, Label, Entry, Button, messagebox
    import mysql.connector
    import Labour, Material_Purchase, Staff_Salary

    # Function to update password
    def update_password():
        site = site_entry.get()
        username = username_entry.get()
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()

        if not (site and username and old_password and new_password):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Connect to the MySQL database
        con = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="user_info")
        myc = con.cursor()

        # Check if the given site, username, and old password match
        myc.execute("SELECT * FROM login WHERE Site=%s AND Username=%s AND Password=%s", (site, username, old_password))
        existing_record = myc.fetchone()

        if existing_record:
            # Update the password in the database
            myc.execute("UPDATE login SET Password=%s WHERE Site=%s AND Username=%s", (new_password, site, username))
            con.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
        else:
            messagebox.showerror("Error", "Site, Username, and Old Password do not match!")

        con.close()

    # Create the main window
    root = tk.Tk()
    root.title("Password Update")
    root.geometry("600x400")
    root.configure(bg='#232323')  # Dark background color

    # Empty rows and columns for centering
    for i in range(4):
        root.grid_rowconfigure(i, weight=1)
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)

    # Heading
    heading = Label(root, text="Update Password", bg='#232323', fg='white', font=('Arial', 20))
    heading.grid(row=1, column=1, columnspan=2, pady=10)

    # Labels
    site_label = Label(root, text="Site Number:", bg='#232323', fg='white', font=('Arial', 12))
    username_label = Label(root, text="Username:", bg='#232323', fg='white', font=('Arial', 12))
    old_password_label = Label(root, text="Old Password:", bg='#232323', fg='white', font=('Arial', 12))
    new_password_label = Label(root, text="New Password:", bg='#232323', fg='white', font=('Arial', 12))

    # Entry fields
    site_entry = Entry(root, font=('Arial', 12))
    username_entry = Entry(root, font=('Arial', 12))
    old_password_entry = Entry(root, show="*", font=('Arial', 12))  # Show password as asterisks
    new_password_entry = Entry(root, show="*", font=('Arial', 12))

    # Update button
    update_button = Button(root, text="Update", command=update_password, font=('Arial', 12))

    # Grid layout for labels and entry fields
    site_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")
    site_entry.grid(row=2, column=2, padx=10, pady=5)
    username_label.grid(row=3, column=1, padx=10, pady=5, sticky="e")
    username_entry.grid(row=3, column=2, padx=10, pady=5)
    old_password_label.grid(row=4, column=1, padx=10, pady=5, sticky="e")
    old_password_entry.grid(row=4, column=2, padx=10, pady=5)
    new_password_label.grid(row=5, column=1, padx=10, pady=5, sticky="e")
    new_password_entry.grid(row=5, column=2, padx=10, pady=5)

    # Update button
    update_button.grid(row=6, column=1, columnspan=2, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")

    def labour():
        root.destroy()
        Labour.Labour_page(pwd, site_num)

    def material():
        root.destroy()
        Material_Purchase.Material_Purchase_page(pwd, site_num)

    def salary():
        root.destroy()
        Staff_Salary.Staff_Salary_page(pwd, site_num)

    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure")
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase", command=material)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary",command=salary)
    home_button.configure(style='TButton')  # Apply the style to the button
    manager_button.configure(style='TButton')  
    director_button.configure(style='TButton')  
    exit_button.configure(style='TButton')

    # Grid placement for navigation bar buttonexit
    home_button.grid(row=0, column=1, padx=10, pady=10)
    manager_button.grid(row=0, column=2, padx=10, pady=10)
    director_button.grid(row=0, column=3, padx=10, pady=10)
    exit_button.grid(row=0, column=4, padx=[10,100], pady=10)

    # Run the tkinter main loop
    root.mainloop()

    

    

Update_Password("Techno$pider2099")