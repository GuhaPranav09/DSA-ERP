def Material_Purchase_page(site_num=1):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Local_Expenditure, Staff_Salary
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd='mysql')
    myc = con.cursor()

    myc.execute("use user_info")
    myc.execute("create table if not exists purchase(Site int, Material int, Quantity int, Price int, DOB date)")
    con.commit()

    # Function to validate the form before submission
    def validate_form():
        material=material_entry.get()
        quantity=quantity_entry.get()
        price=price_entry.get()
        dob = dob_entry.get_date()

        # Check if all required fields are filled
        if not (material and dob and quantity and price):
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
            material=material_entry.get()
            quantity=quantity_entry.get()
            price=price_entry.get()
            dob = dob_entry.get_date().strftime("%Y%m%d")

            myc.execute("SELECT * FROM purchase WHERE DOB = %s AND Material=%s AND Site=%s", (dob, material, site_num))
            existing_record = myc.fetchone()
            
            if not existing_record:

                # SQL insertion query
                insert_query = "insert into purchase (Site, DOB, Material, Quantity, Price) values (%s, %s, %s, %s, %s)"
                data = (site_num,dob,material,quantity,price)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Time Stamp:", dob)
                print("Material:", material)
                print("Quantity:", quantity)
                print("Price:Rs", price)
                print("\n\n\n")
                success_label.config(text="Data entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record already exists!")
            

    def update():
        if validate_form():
           
           pass
                
    def clear():
        material_entry.delete(0, tk.END)      
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        dob_entry.set_date(datetime.date.today())

    def delete():
        material=material_entry.get()
        dob = dob_entry.get_date().strftime("%Y%m%d")

        # Check if all required fields are filled
        if dob and material:

            myc.execute("SELECT * FROM purchase WHERE DOB = %s AND Material=%s AND Site=%s", (dob, material, site_num))
            existing_record = myc.fetchone()

            if existing_record:
                delete_query = "DELETE FROM purchase WHERE DOB = %s AND Material=%s AND Site=%s"
                delete_data=(dob,material,site_num)
                
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
                print("Material:", material)
                print("\n\n\n")
                success_label.config(text="Data deletion successful!", fg='green')
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record doesnt exist!")
        else:
            success_label.config(text="")
            messagebox.showerror("Error", "Site no., Time Stamp and Material required!")

    def labour():
        root.destroy()
        Labour.Labour_page(site_num)

    def local_exp():
        root.destroy()
        Local_Expenditure.Local_Expenditure_page(site_num)
    
    def salary():
        root.destroy()
        Staff_Salary.Staff_Salary_page(site_num)

    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Site {} Material Purchase details".format(site_num))
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150), Image.ANTIALIAS)
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Site {} Material Purchase".format(site_num), bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    material_label = tk.Label(root, text="Material:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    quantity_label = tk.Label(root, text="Quantity:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    price_label = tk.Label(root, text="Price:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    dob_label = tk.Label(root, text="Timestamp:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))

    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry Fields
    material_entry = tk.Entry(root, font=('Arial',12))
    quantity_entry = tk.Entry(root, font=('Arial',12))
    price_entry = tk.Entry(root, font=('Arial',12))
    
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

    # Grid Configuration
    for i in range(9):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=2, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=2, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=2, sticky="n", pady=2) 

    dob_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    dob_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    material_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    material_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    quantity_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    quantity_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    price_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
    price_entry.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
   
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
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase",)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary", command=salary)
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

def D_Material_Purchase_page():
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Local_Expenditure, Staff_Salary
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd='mysql')
    myc = con.cursor()

    myc.execute("use user_info")
    myc.execute("create table if not exists purchase(Site int, Material int, Quantity int, Price int, DOB date)")
    con.commit()

    # Function to validate the form before submission
    def validate_form():
        site_num=site_entry.get()
        material=material_entry.get()
        quantity=quantity_entry.get()
        price=price_entry.get()
        dob = dob_entry.get_date()

        # Check if all required fields are filled
        if not (site_num and material and dob and quantity and price):
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
            material=material_entry.get()
            quantity=quantity_entry.get()
            price=price_entry.get()
            dob = dob_entry.get_date().strftime("%Y%m%d")

            myc.execute("SELECT * FROM purchase WHERE DOB = %s AND Material=%s AND Site=%s", (dob, material, site_num))
            existing_record = myc.fetchone()
            
            if not existing_record:

                # SQL insertion query
                insert_query = "insert into purchase (Site, DOB, Material, Quantity, Price) values (%s, %s, %s, %s, %s)"
                data = (site_num,dob,material,quantity,price)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Time Stamp:", dob)
                print("Material:", material)
                print("Quantity:", quantity)
                print("Price:Rs", price)
                print("\n\n\n")
                success_label.config(text="Data entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record already exists in Site{}!".format(site_num))
            
            

    def update():
        if validate_form():
           
           pass
                
    def clear():
        site_entry.delete(0, tk.END)
        material_entry.delete(0, tk.END)      
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        dob_entry.set_date(datetime.date.today())

    def delete():
        site_num=site_entry.get()
        material=material_entry.get()
        dob = dob_entry.get_date().strftime("%Y%m%d")

        # Check if all required fields are filled
        if dob and material:

            myc.execute("SELECT * FROM purchase WHERE DOB = %s AND Material=%s AND Site=%s", (dob, material, site_num))
            existing_record = myc.fetchone()

            if existing_record:
                delete_query = "DELETE FROM purchase WHERE DOB = %s AND Material=%s AND Site=%s"
                delete_data=(dob,material,site_num)
                
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
                print("Material:", material)
                print("\n\n\n")
                success_label.config(text="Data deletion successful!", fg='green')
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record doesnt exist in Site {}".format(site_num))
        else:
            success_label.config(text="")
            messagebox.showerror("Error", "Site no., Time Stamp and Material required!")

    def labour():
        root.destroy()
        Labour.D_Labour_page()

    def local_exp():
        root.destroy()
        Local_Expenditure.D_Local_Expenditure_page()
    
    def salary():
        root.destroy()
        Staff_Salary.D_Staff_Salary_page()

    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Material Purchase details")
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150), Image.ANTIALIAS)
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Material Purchase", bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    site_label = tk.Label(root, text="Site no.:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    material_label = tk.Label(root, text="Material:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    quantity_label = tk.Label(root, text="Quantity:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    price_label = tk.Label(root, text="Price:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    dob_label = tk.Label(root, text="Timestamp:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))

    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry Fields
    site_entry = tk.Entry(root, font=('Arial',12))
    material_entry = tk.Entry(root, font=('Arial',12))
    quantity_entry = tk.Entry(root, font=('Arial',12))
    price_entry = tk.Entry(root, font=('Arial',12))
    
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

    # Grid Configuration
    for i in range(10):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=2, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=2, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=2, sticky="n", pady=2) 

    site_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    site_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    dob_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    dob_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    material_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    material_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    quantity_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
    quantity_entry.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    price_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)
    price_entry.grid(row=8, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
   
    insert_button.grid(row=9, column=1, pady=10)
    update_button.grid(row=9, column=2, pady=10)
    delete_button.grid(row=9, column=3, pady=10)
    clear_button.grid(row=9, column=4, pady=10)
    success_label.grid(row=10, column=1, columnspan=4, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")

    

    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure", command=local_exp)
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase",)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary", command=salary)
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
    Material_Purchase_page()
