def Report_page(pwd, site_num=1):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    from datetime import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Material_Purchase, Staff_Salary, Local_Expenditure, Home
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()

    myc.execute("use user_info")
    con.commit()

    
    def back():
        root.destroy()
        Home.Home_page(pwd)

    def labour():
        root.destroy()
        Labour.Labour_page(pwd, site_num)

    def material():
        root.destroy()
        Material_Purchase.Material_Purchase_page(pwd, site_num)

    def salary():
        root.destroy()
        Staff_Salary.Staff_Salary_page(pwd, site_num)
    
    def expenditure():
        root.destroy()
        Local_Expenditure.Local_Expenditure_page(pwd,site_num)

    def get_years():
        current_year = datetime.now().year
        return [str(year) for year in range(2015, current_year + 1)]

    def view_report(category, selected_year, selected_month):
        if not (category and selected_year and selected_month):
            messagebox.showerror("Error", "Please select an option for each field.")
            return
        elif selected_year=="All Years" and selected_month!="Overall":
            messagebox.showerror("Error", "Please select a year for the month.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="user_info")
            myc = con.cursor()

            if category == "Expenditure":
                table_name = "expenditure"
                column_name = "Amount"
            elif category == "Purchase":
                table_name = "purchase"
                column_name = "Price"
            else:
                raise ValueError("Invalid category selected")

            if selected_year == "All Years":
                year_condition = "1"  # Always true
            else:
                year_condition = f"YEAR(DOB) = {selected_year}"

            if selected_month == "Overall":
                month_condition = ""
            else:
                month_condition = f"AND MONTH(DOB) = {selected_month.split(' ')[0]}"  # Extract the month number

            query = f"SELECT SUM({column_name}) FROM {table_name} WHERE {year_condition} {month_condition} AND Site = {site_num}"

            myc.execute(query)
            result = myc.fetchone()[0]

            con.close()

            msg_month=selected_month
            if msg_month!='Overall':
                msg_month=msg_month[4:-1]
            if result is not None:
                messagebox.showinfo("Report", f"Total {category} amount for {msg_month} {selected_year}: {result}")
            else:
                messagebox.showinfo("Report", f"No {category} data available for {msg_month} {selected_year}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")

        
        
    
    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Site {} Generate Report".format(site_num))
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Site {} Generate Report".format(site_num), bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    label_category = tk.Label(root, text="Select category:", bg='#232323', fg='white', font=('Arial', 12))

    # Dropdown menu for category
    categories = ["Expenditure", "Purchase"]
    category_var = tk.StringVar()
    dropdown_category = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly")

    # Label and Dropdown menu for year
    label_year = tk.Label(root, text="Select year:", bg='#232323', fg='white', font=('Arial', 12))
    
    years = get_years()
    years.insert(0,"All Years")
    year_var = tk.StringVar()
    dropdown_year = ttk.Combobox(root, textvariable=year_var, values=years, state="readonly")
    

    # Label and Dropdown menu for month
    label_month = tk.Label(root, text="Select month:", bg='#232323', fg='white', font=('Arial', 12))
    

    months = ["Overall", "01 (January)", "02 (February)", "03 (March)", "04 (April)", "05 (May)", "06 (June)", "07 (July)",
            "08 (August)", "09 (September)", "10 (October)", "11 (November)", "12 (December)"]
    month_var = tk.StringVar()
    dropdown_month = ttk.Combobox(root, textvariable=month_var, values=months, state="readonly")
    


    # Buttons
    view_button = ttk.Button(root, text="View Report", command=lambda: view_report(category_var.get(), year_var.get(), month_var.get()),style='TButton')
    back_button = ttk.Button(root, text="Log out", command=back, style='TButton')

    # Grid Configuration
    for i in range(8):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=4, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=4, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=4, sticky="n", pady=2) 

    label_category.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    dropdown_category.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    label_year.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    dropdown_year.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    label_month.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    dropdown_month.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
    view_button.grid(row=7, column=3, columnspan=2, pady=10)
    back_button.grid(row=8, column=3, columnspan=2, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")

    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure",command=expenditure)
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase", command=material)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary",command=salary)
    report_button = ttk.Button(nav_bar_frame, text="Report")
    home_button.configure(style='TButton')  # Apply the style to the button
    manager_button.configure(style='TButton')  
    director_button.configure(style='TButton')  
    exit_button.configure(style='TButton')
    report_button.configure(style='TButton')

    # Grid placement for navigation bar buttonexit
    home_button.grid(row=0, column=1, padx=10, pady=10)
    manager_button.grid(row=0, column=2, padx=10, pady=10)
    report_button.grid(row=0, column=3, padx=10, pady=10)
    director_button.grid(row=0, column=4, padx=10, pady=10)
    exit_button.grid(row=0, column=5, padx=[10,100], pady=10)


    # Run the Tkinter main loop
    root.mainloop()

def D_Report_page(pwd, site_num=0):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    from datetime import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk
    import Labour, Material_Purchase, Staff_Salary, Local_Expenditure, Home, Managers_password
   

    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()

    myc.execute("use user_info")
    con.commit()

    
    def back():
        root.destroy()
        Home.Home_page(pwd)

    def labour():
        root.destroy()
        Labour.D_Labour_page(pwd)

    def material():
        root.destroy()
        Material_Purchase.D_Material_Purchase_page(pwd)

    def salary():
        root.destroy()
        Staff_Salary.D_Staff_Salary_page(pwd)
    
    def expenditure():
        root.destroy()
        Local_Expenditure.D_Local_Expenditure_page(pwd)
    
    def managers():
        root.destroy()
        Managers_password.Password_Page(pwd)

    def get_years():
        current_year = datetime.now().year
        return [str(year) for year in range(2015, current_year + 1)]

    def view_report(category, selected_year, selected_month, site_num):
        if not (category and selected_year and selected_month and site_num):
            messagebox.showerror("Error", "Please select an option for each field.")
            return
        elif selected_year=="All Years" and selected_month!="Overall":
            messagebox.showerror("Error", "Please select a year for the month.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="user_info")
            myc = con.cursor()

            if category == "Expenditure":
                table_name = "expenditure"
                column_name = "Amount"
            elif category == "Purchase":
                table_name = "purchase"
                column_name = "Price"
            else:
                raise ValueError("Invalid category selected")

            if selected_year == "All Years":
                year_condition = "1"  # Always true
            else:
                year_condition = f"YEAR(DOB) = {selected_year}"

            if selected_month == "Overall":
                month_condition = ""
            else:
                month_condition = f"AND MONTH(DOB) = {selected_month.split(' ')[0]}"  # Extract the month number

            query = f"SELECT SUM({column_name}) FROM {table_name} WHERE {year_condition} {month_condition} AND Site = {site_num}"

            myc.execute(query)
            result = myc.fetchone()[0]

            con.close()

            msg_month=selected_month
            if msg_month!='Overall':
                msg_month=msg_month[4:-1]
            if result is not None:
                messagebox.showinfo("Report", f"Total {category} amount for Site {site_num} {msg_month} {selected_year}: {result} Rs")
            else:
                messagebox.showinfo("Report", f"No {category} data available for Site {site_num} {msg_month} {selected_year}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")

        
        
    
    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Generate Report".format(site_num))
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Generate Report".format(site_num), bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg) 

    # Labels
    label_category = tk.Label(root, text="Select category:", bg='#232323', fg='white', font=('Arial', 12))

    # Dropdown menu for category
    categories = ["Expenditure", "Purchase"]
    category_var = tk.StringVar()
    dropdown_category = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly")

    #Label and Dropdown menu for site
    label_site = tk.Label(root, text="Select Site:", bg='#232323', fg='white', font=('Arial', 12))
    site_entry = tk.Entry(root, font=('Arial',12))

    # Label and Dropdown menu for year
    label_year = tk.Label(root, text="Select year:", bg='#232323', fg='white', font=('Arial', 12))
    
    years = get_years()
    years.insert(0,"All Years")
    year_var = tk.StringVar()
    dropdown_year = ttk.Combobox(root, textvariable=year_var, values=years, state="readonly")
    

    # Label and Dropdown menu for month
    label_month = tk.Label(root, text="Select month:", bg='#232323', fg='white', font=('Arial', 12))
    

    months = ["Overall", "01 (January)", "02 (February)", "03 (March)", "04 (April)", "05 (May)", "06 (June)", "07 (July)",
            "08 (August)", "09 (September)", "10 (October)", "11 (November)", "12 (December)"]
    month_var = tk.StringVar()
    dropdown_month = ttk.Combobox(root, textvariable=month_var, values=months, state="readonly")
    


    # Buttons
    view_button = ttk.Button(root, text="View Report", command=lambda: view_report(category_var.get(), year_var.get(), month_var.get(), site_entry.get()),style='TButton')
    back_button = ttk.Button(root, text="Log out", command=back, style='TButton')

    # Grid Configuration
    for i in range(8):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=2, columnspan=4, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=2, columnspan=4, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=2, columnspan=4, sticky="n", pady=2) 

    label_site.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    site_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    label_category.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    dropdown_category.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    label_year.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    dropdown_year.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    label_month.grid(row=7, column=0, sticky="w", padx=5, pady=5)
    dropdown_month.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
    view_button.grid(row=8, column=3, columnspan=2, pady=10)
    back_button.grid(row=9, column=3, columnspan=2, pady=10)

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")

    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure",command=expenditure)
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase", command=material)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary",command=salary)
    report_button = ttk.Button(nav_bar_frame, text="Report")
    accounts_button = ttk.Button(nav_bar_frame, text="Managers", command=managers)
    home_button.configure(style='TButton')  # Apply the style to the button
    manager_button.configure(style='TButton')  
    director_button.configure(style='TButton')  
    exit_button.configure(style='TButton')
    report_button.configure(style='TButton')
    accounts_button.configure(style='TButton')

    # Grid placement for navigation bar buttonexit
    home_button.grid(row=0, column=1, padx=10, pady=10)
    manager_button.grid(row=0, column=2, padx=10, pady=10)
    report_button.grid(row=0, column=3, padx=10, pady=10)
    accounts_button.grid(row=0, column=4, padx=10, pady=10)
    director_button.grid(row=0, column=5, padx=10, pady=10)
    exit_button.grid(row=0, column=6, padx=[10,100], pady=10)


    # Run the Tkinter main loop
    root.mainloop()


if __name__ == '__main__':
    D_Report_page("mysql")
