def Local_Expenditure_page(pwd, site_num=1):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Material_Purchase, Staff_Salary, view_table, Home
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()

    myc.execute("use user_info")
    myc.execute("create table if not exists expenditure(Site int, Amount int, Activity TEXT, DOB date)")
    con.commit()

    # Function to validate the form before submission
    def validate_form():
        amount = amount_entry.get()
        activity = activity_entry.get()
        dob = dob_entry.get_date()

        # Check if all required fields are filled
        if not (amount and dob and activity):
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
            amount = amount_entry.get()
            activity = activity_entry.get()
            dob = dob_entry.get_date().strftime("%Y%m%d")

            myc.execute("SELECT * FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s", (dob, activity, site_num))
            existing_record = myc.fetchone()
            
            if not existing_record:

                # SQL insertion query
                insert_query = "insert into expenditure (Site, DOB, Activity, Amount) values (%s, %s, %s, %s)"
                data = (site_num,dob,activity, amount)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Time Stamp:", dob)
                print("Activity:", activity)
                print("Amount:Rs", amount)
                print("\n\n\n")
                success_label.config(text="Data entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record already exists!")
            

    def update():
        if validate_form():
            dob = dob_entry.get_date().strftime("%Y%m%d")
            activity=activity_entry.get()

            myc.execute("SELECT * FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s", (dob,material,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                # Fetch new details from the user
                dob = dob_entry.get_date().strftime("%Y%m%d")
                activity=activity_entry.get()
                amount=amount_entry.get()
                

                # Update the record in the database
                update_query = "UPDATE expenditure SET Amount=%s WHERE Activity = %s AND DOB=%s AND Site=%s"
                update_data = (amount, activity, dob, site_num)
                
                myc.execute(update_query, update_data)
                con.commit()

                try:
                    myc.execute(update_query, update_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("UPDATED DETAILS\n\n")
                print("Site no.:", site_num)
                print("Date:", dob)
                print("Activity:", activity)
                print("Amount:Rs", amount)
                print("\n\n\n")
                success_label.config(text="Data updation successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record doesn't exist!")
           
                
    def clear():
        amount_entry.delete(0, tk.END)      
        activity_entry.delete(0, tk.END)
        dob_entry.set_date(datetime.date.today())

    def delete():
        activity = activity_entry.get()
        dob = dob_entry.get_date().strftime("%Y%m%d")

        # Check if all required fields are filled
        if dob and activity:

            myc.execute("SELECT * FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s", (dob, activity, site_num))
            existing_record = myc.fetchone()

            if existing_record:
                delete_query = "DELETE FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s"
                delete_data=(dob,activity,site_num)
                
                myc.execute(delete_query, delete_data)
                con.commit()

                try:
                    myc.execute(delete_query, delete_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Data deleted\n")
                print("Site no.:", site_num)
                print("Time Stamp:", dob)
                print("Activity:", activity)
                print("\n\n\n")
                success_label.config(text="Data deletion successful!", fg='green')
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record doesn't exist!")
        else:
            success_label.config(text="")
            messagebox.showerror("Error", "Time Stamp and Activity required!")

    def back():
        root.destroy()
        Home.Home_page(pwd)

    def view():
        view_table.display(pwd, site_num, "expenditure")

    def labour():
        root.destroy()
        Labour.Labour_page(pwd, site_num)

    def material():
        root.destroy()
        Material_Purchase.Material_Purchase_page(pwd, site_num)

    def salary():
        root.destroy()
        Staff_Salary.Staff_Salary_page(pwd, site_num)
    
    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Site {} Local Expenditure details".format(site_num))
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Site {} Local Expenditure".format(site_num), bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    activity_label = tk.Label(root, text="Activity:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    amount_label = tk.Label(root, text="Amount:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    dob_label = tk.Label(root, text="Timestamp:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))

    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry Fields
    activity_entry = tk.Entry(root, font=('Arial',12))
    amount_entry = tk.Entry(root, font=('Arial',12))

    # Function to handle entry field focus out event
    def on_focus_out(event):
        if dob_entry.get() == "":
            dob_entry.set_date(datetime.date.today())  # Set default date if no input

    # Create the Date of Birth Entry with calendar widget
    dob_entry = DateEntry(root, width=12, background='black', foreground='white', borderwidth=2)
    dob_entry.config(font=('Arial', 12))  # Change text color and font
    dob_entry.set_date(datetime.date.today())  # Set default date to today
    dob_entry.bind('<FocusOut>', on_focus_out)  # Bind focus out event to handle default date setting


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
    for i in range(8):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=2, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=2, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=2, sticky="n", pady=2) 

    dob_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    dob_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    activity_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    activity_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    amount_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    amount_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
   
    insert_button.grid(row=7, column=1, pady=10)
    update_button.grid(row=7, column=2, pady=10)
    delete_button.grid(row=7, column=3, pady=10)
    clear_button.grid(row=7, column=4, pady=10)
    view_button.grid(row=8, column=2, pady=10)
    back_button.grid(row=8, column=3, pady=10)
    success_label.grid(row=9, column=1, columnspan=4, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")

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


    # Run the Tkinter main loop
    root.mainloop()

def D_Local_Expenditure_page(pwd, site_num=0):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Material_Purchase, Staff_Salary, Managers_password, view_table, Home
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()

    myc.execute("use user_info")
    myc.execute("create table if not exists expenditure(Site int, Amount int, Activity TEXT, DOB date)")
    con.commit()

    # Function to validate the form before submission
    def validate_form():
        site_num=site_entry.get()
        amount = amount_entry.get()
        activity = activity_entry.get()
        dob = dob_entry.get_date()

        # Check if all required fields are filled
        if not (site_num and amount and dob and activity):
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
            site_num=site_entry.get()
            amount = amount_entry.get()
            activity = activity_entry.get()
            dob = dob_entry.get_date().strftime("%Y%m%d")

            myc.execute("SELECT * FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s", (dob, activity, site_num))
            existing_record = myc.fetchone()
            
            if not existing_record:

                # SQL insertion query
                insert_query = "insert into expenditure (Site, DOB, Activity, Amount) values (%s, %s, %s, %s)"
                data = (site_num,dob,activity, amount)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Time Stamp:", dob)
                print("Activity:", activity)
                print("Amount:Rs", amount)
                print("\n\n\n")
                success_label.config(text="Data entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record already exists in Site {}!".format(site_num))
            

    def update():
        if validate_form():
            site_num=site_entry.get()
            dob = dob_entry.get_date().strftime("%Y%m%d")
            activity=activity_entry.get()

            myc.execute("SELECT * FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s", (dob,material,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                # Fetch new details from the user
                dob = dob_entry.get_date().strftime("%Y%m%d")
                activity=activity_entry.get()
                amount=amount_entry.get()
                

                # Update the record in the database
                update_query = "UPDATE expenditure SET Amount=%s WHERE Activity = %s AND DOB=%s AND Site=%s"
                update_data = (amount, activity, dob, site_num)
                
                myc.execute(update_query, update_data)
                con.commit()

                try:
                    myc.execute(update_query, update_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("UPDATED DETAILS\n\n")
                print("Site no.:", site_num)
                print("Date:", dob)
                print("Activity:", activity)
                print("Amount:Rs", amount)
                print("\n\n\n")
                success_label.config(text="Data updation successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record doesn't exist!")
           
                
    def clear():
        site_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)      
        activity_entry.delete(0, tk.END)
        dob_entry.set_date(datetime.date.today())

    def delete():
        site_num = site_entry.get()
        activity = activity_entry.get()
        dob = dob_entry.get_date().strftime("%Y%m%d")

        # Check if all required fields are filled
        if site_num and dob and activity:

            myc.execute("SELECT * FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s", (dob, activity, site_num))
            existing_record = myc.fetchone()

            if existing_record:
                delete_query = "DELETE FROM expenditure WHERE DOB = %s AND Activity=%s AND Site=%s"
                delete_data=(dob,activity,site_num)
                
                myc.execute(delete_query, delete_data)
                con.commit()

                try:
                    myc.execute(delete_query, delete_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Data deleted\n")
                print("Site no.:", site_num)
                print("Time Stamp:", dob)
                print("Activity:", activity)
                print("\n\n\n")
                success_label.config(text="Data deletion successful!", fg='green')
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record doesn't exist in Site {}!".format(site_num))
        else:
            success_label.config(text="")
            messagebox.showerror("Error", "Site no., Time Stamp and Activity required!")

    def back():
        root.destroy()
        Home.Home_page(pwd)

    def view():
        view_table.D_display(pwd, site_num, "expenditure")

    def labour():
        root.destroy()
        Labour.D_Labour_page(pwd)

    def material():
        root.destroy()
        Material_Purchase.D_Material_Purchase_page(pwd)

    def salary():
        root.destroy()
        Staff_Salary.D_Staff_Salary_page(pwd)
    
    def managers():
        root.destroy()
        Managers_password.Password_Page(pwd)

    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Local Expenditure details")
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Local Expenditure", bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    site_label = tk.Label(root, text="Site no.:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    activity_label = tk.Label(root, text="Activity:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    amount_label = tk.Label(root, text="Amount:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    dob_label = tk.Label(root, text="Timestamp:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))

    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry Fields
    site_entry = tk.Entry(root, font=('Arial',12))
    activity_entry = tk.Entry(root, font=('Arial',12))
    amount_entry = tk.Entry(root, font=('Arial',12))

    # Function to handle entry field focus out event
    def on_focus_out(event):
        if dob_entry.get() == "":
            dob_entry.set_date(datetime.date.today())  # Set default date if no input

    # Create the Date of Birth Entry with calendar widget
    dob_entry = DateEntry(root, width=12, background='black', foreground='white', borderwidth=2)
    dob_entry.config(font=('Arial', 12))  # Change text color and font
    dob_entry.set_date(datetime.date.today())  # Set default date to today
    dob_entry.bind('<FocusOut>', on_focus_out)  # Bind focus out event to handle default date setting


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
    dob_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    dob_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    activity_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    activity_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    amount_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
    amount_entry.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
   
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
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure")
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase",command=material)
    accounts_button = ttk.Button(nav_bar_frame, text="Managers", command=managers)
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

if __name__ == '__main__':
    D_Local_Expenditure_page("mysql")
