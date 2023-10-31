def Staff_Salary_page(pwd, site_num=1):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Local_Expenditure, Material_Purchase
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()

    myc.execute("use user_info")
    myc.execute("create table if not exists salary(Site int, Name varchar(30), RegNo varchar(15), Salary int)")
    con.commit()

     # Function to validate the form before submission
    def validate_form():
        name = name_entry.get()
        reg_no = reg_no_entry.get()
        salary=salary_entry.get()

        # Check if all required fields are filled
        if not (name and reg_no and salary):
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
            
            reg_no_to_insert = reg_no_entry.get()
            myc.execute("SELECT * FROM salary WHERE RegNo = %s AND Site = %s", (reg_no_to_insert,site_num))
            existing_record = myc.fetchone()
            
            if not existing_record:
                name = name_entry.get()
                reg_no = reg_no_entry.get()
                salary=salary_entry.get()

                # SQL insertion query
                insert_query = "insert into salary (Site, Name, RegNo, Salary) values (%s, %s, %s, %s)"
                data = (site_num, name, reg_no, salary)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Name:", name)
                print("Registration Number:", reg_no)
                print("Salary:Rs", salary)
                print("\n\n\n")
                success_label.config(text="Data entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} already exists!".format(reg_no_to_insert))

    def update():
        if validate_form():
            # Get registration number from user input
            reg_no_to_update = reg_no_entry.get()
            # Check if the registration number exists in the database
            myc.execute("SELECT * FROM salary WHERE RegNo = %s AND Site=%s", (reg_no_to_update,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                # Fetch new details from the user
                new_name = name_entry.get()
                new_reg_no = reg_no_entry.get()
                new_salary = salary_entry.get()

                # Update the record in the database
                update_query = "UPDATE salary SET Name = %s, Salary = %s WHERE RegNo = %s AND Site=%s"
                update_data = (new_name, new_salary, reg_no_to_update, site_num)
                
                myc.execute(update_query, update_data)
                con.commit()

                try:
                    myc.execute(update_query, update_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("UPDATED DETAILS\n\n")
                print("Site no.:", site_num)
                print("Name:", new_name)
                print("Registration Number:", new_reg_no)
                print("Salary:Rs", new_salary)
                print("\n\n\n")
                success_label.config(text="Data updation successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} not found!".format(reg_no_to_update))
                
    def clear():
        name_entry.delete(0, tk.END)      
        reg_no_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)
        
    def delete():
        name = name_entry.get()
        reg_no_to_delete = reg_no_entry.get()

        if name and reg_no_to_delete:

            myc.execute("SELECT * FROM salary WHERE RegNo = %s AND Site=%s", (reg_no_to_delete,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                delete_query = "DELETE FROM salary WHERE RegNo = %s AND Site=%s"
                delete_data=(reg_no_to_delete,site_num)
                
                myc.execute(delete_query, delete_data)
                con.commit()

                try:
                    myc.execute(delete_query, delete_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Data deleted\n")
                print("Registration Number:", reg_no_to_delete)
                print("\n\n\n")

                success_label.config(text="Data deletion successful!", fg='green')
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} not found!".format(reg_no_to_delete))
        else:
            success_label.config(text="")
            messagebox.showerror("Error", "Name and Registration number required!")

    def labour():
        root.destroy()
        Labour.Labour_page(pwd, site_num)

    def local_exp():
        root.destroy()
        Local_Expenditure.Local_Expenditure_page(pwd, site_num)

    def material():
        root.destroy()
        Material_Purchase.Material_Purchase_page(pwd, site_num)

    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Site {} Staff Salary details".format(site_num))
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Site {} Staff Salary".format(site_num), bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    name_label = tk.Label(root, text="Name:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    reg_no_label = tk.Label(root, text="Registration number:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    salary_label = tk.Label(root, text="Salary:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    
    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry Fields
    name_entry = tk.Entry(root, font=('Arial',12))
    reg_no_entry = tk.Entry(root, font=('Arial',12))
    salary_entry = tk.Entry(root, font=('Arial',12))
    

    # Buttons
    insert_button = ttk.Button(root, text="Submit", command=submit)
    update_button = ttk.Button(root, text="Update", command=update)
    delete_button = ttk.Button(root, text="Delete", command=delete)
    clear_button = ttk.Button(root, text="Clear", command=clear)
    insert_button.configure(style='TButton')  # Apply the style to the button
    update_button.configure(style='TButton')  
    delete_button.configure(style='TButton')  
    clear_button.configure(style='TButton')  

    # Grid Configuration
    for i in range(8):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=2, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=2, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=2, sticky="n", pady=2) 

    name_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    name_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    reg_no_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    reg_no_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    salary_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    salary_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
      
   
    insert_button.grid(row=7, column=1, pady=10)
    update_button.grid(row=7, column=2, pady=10)
    delete_button.grid(row=7, column=3, pady=10)
    clear_button.grid(row=7, column=4, pady=10)
    success_label.grid(row=8, column=1, columnspan=4, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")

    

    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure", command=local_exp)
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase",command=material)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary")
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

def D_Staff_Salary_page(pwd):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Local_Expenditure, Material_Purchase
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()

    myc.execute("use user_info")
    myc.execute("create table if not exists salary(Site int, Name varchar(30), RegNo varchar(15), Salary int)")
    con.commit()

     # Function to validate the form before submission
    def validate_form():
        site_num=site_entry.get()
        name = name_entry.get()
        reg_no = reg_no_entry.get()
        salary=salary_entry.get()

        # Check if all required fields are filled
        if not (site_num and name and reg_no and salary):
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
            reg_no_to_insert = reg_no_entry.get()
            myc.execute("SELECT * FROM salary WHERE RegNo = %s AND Site = %s", (reg_no_to_insert,site_num))
            existing_record = myc.fetchone()
            
            if not existing_record:
                name = name_entry.get()
                reg_no = reg_no_entry.get()
                salary=salary_entry.get()

                # SQL insertion query
                insert_query = "insert into salary (Site, Name, RegNo, Salary) values (%s, %s, %s, %s)"
                data = (site_num, name, reg_no, salary)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Name:", name)
                print("Registration Number:", reg_no)
                print("Salary:Rs", salary)
                print("\n\n\n")
                success_label.config(text="Data entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} already exists in Site {}!".format(reg_no_to_insert,site_num))

    def update():
        if validate_form():
            # Get registration number from user input
            site_num = site_entry.get()
            reg_no_to_update = reg_no_entry.get()
            # Check if the registration number exists in the database
            myc.execute("SELECT * FROM salary WHERE RegNo = %s AND Site=%s", (reg_no_to_update,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                # Fetch new details from the user
                new_name = name_entry.get()
                new_reg_no = reg_no_entry.get()
                new_salary = salary_entry.get()

                # Update the record in the database
                update_query = "UPDATE salary SET Name = %s, Salary = %s WHERE RegNo = %s AND Site=%s"
                update_data = (new_name, new_salary, reg_no_to_update, site_num)
                
                myc.execute(update_query, update_data)
                con.commit()

                try:
                    myc.execute(update_query, update_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("UPDATED DETAILS\n\n")
                print("Site no.:", site_num)
                print("Name:", new_name)
                print("Registration Number:", new_reg_no)
                print("Salary:Rs", new_salary)
                print("\n\n\n")
                success_label.config(text="Data updation successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} not found in Site {}!".format(reg_no_to_update,site_num))
                
    def clear():
        site_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)      
        reg_no_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)
        
    def delete():
        site_num = site_entry.get()
        name = name_entry.get()
        reg_no_to_delete = reg_no_entry.get()

        if site_num and name and reg_no_to_delete:

            myc.execute("SELECT * FROM salary WHERE RegNo = %s AND Site=%s", (reg_no_to_delete,site_num))
            existing_record = myc.fetchone()

            if existing_record:
                delete_query = "DELETE FROM salary WHERE RegNo = %s AND Site=%s"
                delete_data=(reg_no_to_delete,site_num)
                
                myc.execute(delete_query, delete_data)
                con.commit()

                try:
                    myc.execute(delete_query, delete_data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Data deleted\n")
                print("Site no.:", site_num)
                print("Registration Number:", reg_no_to_delete)
                print("\n\n\n")

                success_label.config(text="Data deletion successful!", fg='green')
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} not found in Site {}!".format(reg_no_to_delete,site_num))
        else:
            success_label.config(text="")
            messagebox.showerror("Error", "Site no., Name and Registration number required!")

    def labour():
        root.destroy()
        Labour.D_Labour_page(pwd)

    def local_exp():
        root.destroy()
        Local_Expenditure.D_Local_Expenditure_page(pwd)

    def material():
        root.destroy()
        Material_Purchase.D_Material_Purchase_page(pwd)

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
    page_name_label=Label(root, text="Staff Salary", bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    site_label = tk.Label(root, text="Site no.:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    name_label = tk.Label(root, text="Name:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    reg_no_label = tk.Label(root, text="Registration number:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    salary_label = tk.Label(root, text="Salary:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    
    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry Fields
    site_entry = tk.Entry(root, font=('Arial',12))
    name_entry = tk.Entry(root, font=('Arial',12))
    reg_no_entry = tk.Entry(root, font=('Arial',12))
    salary_entry = tk.Entry(root, font=('Arial',12))
    

    # Buttons
    insert_button = ttk.Button(root, text="Submit", command=submit)
    update_button = ttk.Button(root, text="Update", command=update)
    delete_button = ttk.Button(root, text="Delete", command=delete)
    clear_button = ttk.Button(root, text="Clear", command=clear)
    insert_button.configure(style='TButton')  # Apply the style to the button
    update_button.configure(style='TButton')  
    delete_button.configure(style='TButton')  
    clear_button.configure(style='TButton')  

    # Grid Configuration
    for i in range(9):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=2, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=2, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=2, sticky="n", pady=2) 

    site_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    site_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    name_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    name_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    reg_no_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    reg_no_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    salary_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
    salary_entry.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky="w")
      
   
    insert_button.grid(row=8, column=1, pady=10)
    update_button.grid(row=8, column=2, pady=10)
    delete_button.grid(row=8, column=3, pady=10)
    clear_button.grid(row=8, column=4, pady=10)
    success_label.grid(row=9, column=1, columnspan=4, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")

    

    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure", command=local_exp)
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase",command=material)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary")
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


if __name__ == '__main__':
    Staff_Salary_page()