def Home_page():
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    import mysql.connector
    import datetime
    from PIL import Image, ImageTk


    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd='mysql')
    myc = con.cursor()
    myc.execute("show databases")
    out1 = myc.fetchall()
    if ("user_info",) not in out1:
        myc.execute("create database user_info")

    myc.execute("use user_info")
    myc.execute("create table if not exists users(Name varchar(30), RegNo varchar(15), DOB date, Gender varchar(10), Languages varchar(255), Address varchar(255), Designation varchar(15))")
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
        if not (name and reg_no and dob != "DDMMYYYY" and gender and address and designation):
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
            name = name_entry.get()
            reg_no = reg_no_entry.get()
            input_date = dob_entry.get()
            try:
                dob = datetime.datetime.strptime(input_date, "%d%m%Y").strftime("%Y%m%d")
                gender = gender_var.get()
                languages_list = [lang for lang, checked in language_vars.items() if checked.get()]

                address = address_text.get("1.0", tk.END).strip()
                designation = designation_var.get()

                languages_string = ", ".join(languages_list)

                # SQL insertion query
                insert_query = "insert into users (Name, RegNo, DOB, Gender, Languages, Address, Designation) values (%s, %s, %s, %s, %s, %s, %s)"
                data = (name, reg_no, dob, gender, languages_string, address, designation)

                try:
                    myc.execute(insert_query, data)
                    con.commit()
                except mysql.connector.Error as err:
                    print("Error:", err)


                print("Name:", name)
                print("Registration Number:", reg_no)
                print("Date of Birth:", dob)
                print("Gender:", gender)
                print("Languages Known:", languages_string)
                print(len(languages_string))
                print("Project Selection:", designation)
                print("Address:", address)
                print("-----------------------------------------\n")
                success_label.config(text="Data entry successful!", fg='green') 
            except ValueError as val:
                success_label.config(text="")
                messagebox.showerror("Error", "Invalid date format. Please enter the date in DDMMYYYY format!")
                        


    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("User Information Form")
    root.configure(bg=dark_bg)  # Dark background color

    # Load your image using the Image class from Pillow
    icon_image = Image.open("icon.png")
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)

    #Image
    user_image = Image.open("user.png")
    user_photo = ImageTk.PhotoImage(user_image)
    image_label = Label(root, image=user_photo, background=dark_bg)

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TRadiobutton', background=dark_bg, foreground=dark_fg, selectcolor=dark_bg)
    style.configure('TCheckbutton', background=dark_bg, foreground=dark_fg, selectcolor=dark_bg)  
    style.configure('TCombobox', background=dark_bg, foreground=dark_fg, selectcolor=dark_bg, highlightthickness=0,selectfontcolor=dark_bg)  


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
    name_entry = tk.Entry(root, font=('Arial',10))
    reg_no_entry = tk.Entry(root, font=('Arial',10))

    #DOB entry field
    def on_entry_click(event):
        if dob_entry.get() == "DDMMYYYY":
            dob_entry.delete(0, tk.END)  # Remove placeholder text when clicked
            dob_entry.config(fg='black', font=('Arial',10))  # Change text color to black

    # Function to handle entry field focus out event
    def on_focus_out(event):
        if dob_entry.get() == "":
            dob_entry.insert(0, "DDMMYYY")  # Add placeholder text if no input
            dob_entry.config(fg='grey', font=('Arial',10, 'italic'))  # Change text color to grey

    # Create the Date of Birth Entry with placeholder text
    dob_entry = tk.Entry(root, fg='grey', font=('Arial',10, 'italic'))  # Set default text color to grey
    dob_entry.insert(0, "DDMMYYYY")  # Placeholder text
    dob_entry.bind('<FocusIn>', on_entry_click)  # Bind click event
    dob_entry.bind('<FocusOut>', on_focus_out)  # Bind focus out event

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
    address_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)

    # Designation Selection
    options = ["Student", "Faculty", "Scholar", "HOD", "Dean"]

    designation_var = tk.StringVar()
    designation_menu=ttk.Combobox(root, textvariable=designation_var, values=options, style='TCombobox')

    # Buttons
    insert_button = ttk.Button(root, text="Submit", command=submit)
    update_button = ttk.Button(root, text="Update")
    delete_button = ttk.Button(root, text="Delete")
    view_button = ttk.Button(root, text="Clear")
    insert_button.configure(style='TButton')  # Apply the style to the button
    update_button.configure(style='TButton')  
    delete_button.configure(style='TButton')  
    view_button.configure(style='TButton')  

    # Grid Configuration
    for i in range(8):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    name_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    reg_no_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    reg_no_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    dob_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    dob_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    gender_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
    male_button.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    female_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")
    other_button.grid(row=3, column=3, padx=5, pady=5, sticky="w")
    languages_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    for i in range(len(languages)):
        language_checkboxes[i].grid(row=4, column=i+1, padx=5, pady=5, sticky="w")
    address_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
    address_text.grid(row=5, column=1, columnspan=4, padx=5, pady=5, sticky="w")
    designation_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    designation_menu.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    insert_button.grid(row=7, column=1, pady=10)
    update_button.grid(row=7, column=2, pady=10)
    delete_button.grid(row=7, column=3, pady=10)
    view_button.grid(row=7, column=4, pady=10)
    success_label.grid(row=8, column=1, columnspan=4, pady=10)
    image_label.grid(row=0, column=4, columnspan=3, rowspan=3, sticky="w")  


    # Run the Tkinter main loop
    root.mainloop()

Home_page()
