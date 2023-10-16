def Labour_page(site_num=1):
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from tkcalendar import Calendar, DateEntry
    from PIL import Image, ImageTk


    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd='mysql')
    myc = con.cursor()
    myc.execute("show databases")
    out1 = myc.fetchall()
    if ("user_info",) not in out1:
        myc.execute("create database user_info")

    myc.execute("use user_info")
    myc.execute("create table if not exists users(Site int, Name varchar(30), RegNo varchar(15), DOB date, Gender varchar(10), Languages varchar(255), Address varchar(255), Designation varchar(15))")
    con.commit()

    # Function to validate the form before submission
    def validate_form():
        name = name_entry.get()
        reg_no = reg_no_entry.get()
        dob = dob_entry.get()
        gender = gender_var.get()
        languages_list = [lang for lang, checked in language_vars.items() if checked.get()]
        address = address_text.get("1.0", tk.END).strip()  # Strip leading/trailing spaces from address
        designation = designation_var.get()

        # Check if all required fields are filled
        if not (name and reg_no and dob and gender and address and designation):
            # If any required field is empty, show an error message
            success_label.config(text="")
            messagebox.showerror("Error", "All fields are required!")
            return False
        elif not (languages_list):
            # If No language is selected, show an error message
            success_label.config(text="")
            messagebox.showerror("Error", "Atleast one language is required!")
            return False
        else:
            # All fields are filled, proceed with form submission   
            return True  # Call the submit function
        

    # Function to handle button click event
    def submit():
        if validate_form():
            
            reg_no_to_insert = reg_no_entry.get()
            myc.execute("SELECT * FROM users WHERE RegNo = %s", (reg_no_to_insert,))
            existing_record = myc.fetchone()
            
            if not existing_record:
                name = name_entry.get()
                reg_no = reg_no_entry.get()
                input_date = dob_entry.get_date()
                dob = input_date.strftime("%Y%m%d")
                gender = gender_var.get()
                languages_list = [lang for lang, checked in language_vars.items() if checked.get()]

                address = address_text.get("1.0", tk.END).strip()
                designation = designation_var.get()

                languages_string = ", ".join(languages_list)

                # SQL insertion query
                insert_query = "insert into users (Site, Name, RegNo, DOB, Gender, Languages, Address, Designation) values (%s, %s, %s, %s, %s, %s, %s, %s)"
                data = (site_num, name, reg_no, dob, gender, languages_string, address, designation)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)

                print("Site no.:", site_num)
                print("Name:", name)
                print("Registration Number:", reg_no)
                print("Date of Birth:", dob)
                print("Gender:", gender)
                print("Languages Known:", languages_string)
                print("Project Selection:", designation)
                print("Address:", address)
                print("\n")
                success_label.config(text="Data entry successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} already exists!".format(reg_no_to_insert))

    def update():
        if validate_form():
            # Get registration number from user input
            reg_no_to_update = reg_no_entry.get()
            # Check if the registration number exists in the database
            myc.execute("SELECT * FROM users WHERE RegNo = %s", (reg_no_to_update,))
            existing_record = myc.fetchone()

            if existing_record:
                # Fetch new details from the user
                new_name = name_entry.get()
                new_reg_no = reg_no_entry.get()
                new_input_date = dob_entry.get_date()
                new_dob = new_input_date.strftime("%Y%m%d")
                new_gender = gender_var.get()
                new_languages_list = [lang for lang, checked in language_vars.items() if checked.get()]

                new_address = address_text.get("1.0", tk.END).strip()
                new_designation = designation_var.get()

                new_languages_string = ", ".join(new_languages_list)

                # Update the record in the database
                update_query = "UPDATE users SET Site=%s, Name = %s, DOB = %s, Gender = %s, Languages = %s, Address = %s, Designation = %s WHERE RegNo = %s"
                update_data = (site_num, new_name, new_dob, new_gender, new_languages_string, new_address, new_designation, reg_no_to_update)
                
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
                print("Date of Birth:", new_dob)
                print("Gender:", new_gender)
                print("Languages Known:", new_languages_string)
                print("Project Selection:", new_designation)
                print("Address:", new_address)
                
                success_label.config(text="Data updation successful!", fg='green') 
            else:
                success_label.config(text="")
                messagebox.showerror("Error", "Record with Registration Number {} not found!".format(reg_no_to_update))
                
    def clear():
        name_entry.delete(0, tk.END)      
        reg_no_entry.delete(0, tk.END)
        address_text.delete(1.0, tk.END)
        designation_menu.set('')
        dob_entry.set_date(datetime.date.today())
        male_button.configure(value=False)
        female_button.configure(value=False)
        other_button.configure(value=False)

    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Site {} Labour details".format(site_num))
    root.configure(bg=dark_bg)  # Dark background color

    # Load your image using the Image class from Pillow
    icon_image = Image.open("icon.png")
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)

    #Image
    user_image = Image.open("user.png")
    user_photo = ImageTk.PhotoImage(user_image)
    image_label = Label(root, image=user_photo, background=dark_bg)

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150), Image.ANTIALIAS)
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TRadiobutton', background=dark_bg, foreground=dark_fg, selectcolor=dark_bg)
    style.configure('TCheckbutton', background=dark_bg, foreground=dark_fg, selectcolor=dark_bg)  
    style.configure('TCombobox', background=dark_bg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg)  


    # Labels
    name_label = tk.Label(root, text="Name:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    reg_no_label = tk.Label(root, text="Registration Number:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    dob_label = tk.Label(root, text="Date of Birth:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    gender_label = tk.Label(root, text="Gender:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    languages_label = tk.Label(root, text="Languages Known:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    address_label = tk.Label(root, text="Address:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))
    designation_label = tk.Label(root, text="Designation:", bg=dark_bg, fg=dark_fg, font=('Arial', 10,))

    # Error Label for displaying validation messages
    success_label = tk.Label(root, text="", bg=dark_bg, fg='red', font=('Arial', 10))

    # Entry Fields
    name_entry = tk.Entry(root, font=('Arial',12))
    reg_no_entry = tk.Entry(root, font=('Arial',12))

    # Function to handle entry field focus out event
    def on_focus_out(event):
        if dob_entry.get() == "":
            dob_entry.set_date(datetime.date.today())  # Set default date if no input

    # Create the Date of Birth Entry with calendar widget
    dob_entry = DateEntry(root, width=12, background='black', foreground='white', borderwidth=2)
    dob_entry.config(font=('Arial', 12))  # Change text color and font
    dob_entry.set_date(datetime.date.today())  # Set default date to today
    dob_entry.bind('<FocusOut>', on_focus_out)  # Bind focus out event to handle default date setting


    # Gender Selection
    gender_var = tk.StringVar()
    male_button = ttk.Radiobutton(root, text="Male", variable=gender_var, value="Male")
    female_button = ttk.Radiobutton(root, text="Female", variable=gender_var, value="Female")
    other_button = ttk.Radiobutton(root, text="Other", variable=gender_var, value="Other")
    male_button.configure(style='TRadiobutton')
    female_button.configure(style='TRadiobutton')
    other_button.configure(style='TRadiobutton')


    # Languages Known Checkboxes
    languages = ["English", "Hindi", "Tamil", "Telugu", "Foreign Language"]
    language_vars = {lang: tk.BooleanVar() for lang in languages}
    language_checkboxes = [ttk.Checkbutton(root, text=lang, variable=language_vars[lang], style='TCheckbutton') for lang in language_vars]

    # Address Textbox
    address_text = tk.Text(root, height=5, width=50, wrap=tk.WORD,font=('Arial', 12))

    # Designation Selection
    options = ["Student", "Faculty", "Scholar", "HOD", "Dean"]

    designation_var = tk.StringVar()
    designation_menu=ttk.Combobox(root, textvariable=designation_var, values=options, style='TCombobox')

    # Buttons
    insert_button = ttk.Button(root, text="Submit", command=submit)
    update_button = ttk.Button(root, text="Update", command=update)
    delete_button = ttk.Button(root, text="Delete")
    view_button = ttk.Button(root, text="Clear", command=clear)
    insert_button.configure(style='TButton')  # Apply the style to the button
    update_button.configure(style='TButton')  
    delete_button.configure(style='TButton')  
    view_button.configure(style='TButton')  

    # Grid Configuration
    for i in range(10):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=0, column=2, columnspan=2, sticky="n", pady=5)  
    company_logo_label.grid(row=1, column=2, columnspan=2, sticky="n", pady=2) 

    image_label.grid(row=2, column=4, columnspan=3, rowspan=3, sticky="w")  
    name_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    name_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    reg_no_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
    reg_no_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    dob_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    dob_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    gender_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    male_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")
    female_button.grid(row=5, column=2, padx=5, pady=5, sticky="w")
    other_button.grid(row=5, column=3, padx=5, pady=5, sticky="w")
    languages_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    for i in range(len(languages)):
        language_checkboxes[i].grid(row=6, column=i+1, padx=5, pady=5, sticky="w")
    address_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
    address_text.grid(row=7, column=1, columnspan=4, padx=5, pady=5, sticky="w")
    designation_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)
    designation_menu.grid(row=8, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    insert_button.grid(row=9, column=1, pady=10)
    update_button.grid(row=9, column=2, pady=10)
    delete_button.grid(row=9, column=3, pady=10)
    view_button.grid(row=9, column=4, pady=10)
    success_label.grid(row=10, column=1, columnspan=4, pady=10)


    # Run the Tkinter main loop
    root.mainloop()

Labour_page()
