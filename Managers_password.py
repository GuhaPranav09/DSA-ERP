
def Password_Page(pwd, site_num=0):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Local_Expenditure, Material_Purchase, Staff_Salary, view_table, Home


    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()

    myc.execute("use user_info")
    con.commit()

        # Function to validate the form before submission
    def validate_form():
        site_num=site_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        # Check if all required fields are filled
        if not (site_num and username and password):
            # If any required field is empty, show an error message
            success_label.config(text="")
            messagebox.showerror("Error", "All fields are required!")
            return False
        else:
            # All fields are filled, proceed
            return True  
        

    # Function to handle button click event
    def submit():
        if validate_form():
            site_num = site_entry.get()
            username = username_entry.get()
            myc.execute("SELECT * FROM login WHERE username = %s AND Site = %s", (username,site_num))
            existing_record = myc.fetchone()
            
            if not existing_record:
                password=password_entry.get()

                # SQL insertion query
                insert_query = "insert into login (Site, username, password) values (%s, %s, %s)"
                data = (site_num, username, password)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Manager Username:", username)
                print("Password:", password)
                
                print("\n\n\n")
                success_label.config(text="Account entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Username {} already exists in Site {}!".format(username,site_num))

    def update():
        if validate_form():
            # Get registration number from user input
            site_num = site_entry.get()
            username=username_entry.get()
            # Check if the registration number exists in the database
            myc.execute("SELECT * FROM login WHERE username = %s AND Site=%s", (username,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                # Fetch new details from the user
                password=password_entry.get()

                # Update the record in the database
                update_query = "UPDATE login SET password = %s WHERE username = %s AND Site=%s"
                update_data = (password, username, site_num)
                
                myc.execute(update_query, update_data)
                con.commit()

                try:
                    myc.execute(update_query, update_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("UPDATED DETAILS\n\n")
                print("Site no.:", site_num)
                print("Manager Username:", username)
                print("Password:", password)
                print("\n\n\n")
                success_label.config(text="Account updation successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Username {} not found in Site {}!".format(username,site_num))
                
    def clear():
        site_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)      
        password_entry.delete(0, tk.END)
        
    def delete():
        site_num = site_entry.get()
        username = username_entry.get()

        if site_num and username:

            myc.execute("SELECT * FROM login WHERE username = %s AND Site=%s", (username,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                delete_query = "DELETE FROM login WHERE username = %s AND Site=%s"
                delete_data=(username,site_num)
                
                myc.execute(delete_query, delete_data)
                con.commit()

                try:
                    myc.execute(delete_query, delete_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Data deleted\n")
                print("Site no.:", site_num)
                print("Manager Username:", username)
                print("\n\n\n")

                success_label.config(text="Account deletion successful!", fg='green')
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Username {} not found in Site {}!".format(username,site_num))
        else:
            success_label.config(text="")
            messagebox.showerror("Error", "Username and Password required!")

    def back():
        root.destroy()
        Home.Home_page(pwd)

    def view():
        view_table.D_display(pwd, site_num, "login")

    def labour():
        root.destroy()
        Labour.D_Labour_page(pwd)

    def local_exp():
        root.destroy()
        Local_Expenditure.D_Local_Expenditure_page(pwd)

    def material():
        root.destroy()
        Material_Purchase.D_Material_Purchase_page(pwd)

    def salary():
        root.destroy()
        Staff_Salary.D_Staff_Salary_page(pwd)


    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Staff Salary details")
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Manager Accounts", bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    site_label = Label(root, text="Site Number:", bg='#232323', fg='white', font=('Arial', 12))
    username_label = Label(root, text="Username:", bg='#232323', fg='white', font=('Arial', 12))
    password_label = Label(root, text="Password:", bg='#232323', fg='white', font=('Arial', 12))

    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry fields
    site_entry = tk.Entry(root, font=('Arial', 12))
    username_entry = tk.Entry(root, font=('Arial', 12))
    password_entry = tk.Entry(root, show="*", font=('Arial', 12))  # Show password as asterisks

    # Buttons
    insert_button = ttk.Button(root, text="Submit", command=submit)
    update_button = ttk.Button(root, text="Update", command=update)
    delete_button = ttk.Button(root, text="Delete", command=delete)
    clear_button = ttk.Button(root, text="Clear", command=clear)
    insert_button.configure(style='TButton')  # Apply the style to the button
    update_button.configure(style='TButton')  
    delete_button.configure(style='TButton')  
    clear_button.configure(style='TButton')  
    view_button = ttk.Button(root, text="View table", command=view)
    back_button = ttk.Button(root, text="Log out", command=back, style='TButton')

    # Grid Configuration
    for i in range(9):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=2, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=2, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=2, sticky="n", pady=2) 

    site_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    site_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    username_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    username_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    password_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    password_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
    insert_button.grid(row=8, column=1, pady=10)
    update_button.grid(row=8, column=2, pady=10)
    delete_button.grid(row=8, column=3, pady=10)
    clear_button.grid(row=8, column=4, pady=10)
    view_button.grid(row=9, column=2, pady=10)
    back_button.grid(row=9, column=3, pady=10)
    success_label.grid(row=10, column=1, columnspan=4, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=0, columnspan=7, sticky="news")

    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure", command=local_exp)
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase",command=material)
    accounts_button = ttk.Button(nav_bar_frame, text="Managers")
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary", command=salary)
    home_button.configure(style='TButton')  # Apply the style to the button
    manager_button.configure(style='TButton')  
    accounts_button.configure(style='TButton')  
    director_button.configure(style='TButton')  
    exit_button.configure(style='TButton')

    # Grid placement for navigation bar buttonexit
    home_button.grid(row=0, column=0, padx=[100,10], pady=10)
    manager_button.grid(row=0, column=1, padx=10, pady=10)
    accounts_button.grid(row=0, column=2, padx=10, pady=10)
    director_button.grid(row=0, column=3, padx=10, pady=10)
    exit_button.grid(row=0, column=4, padx=[10,100], pady=10)


    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    Password_Page("mysql")