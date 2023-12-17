def Home_page(pwd): 
    import tkinter as tk
    from tkinter import ttk, Label
    from PIL import Image, ImageTk
    import Login
    import mysql.connector

    
    #SQL STARTUP STUFF
    con = mysql.connector.connect(host='localhost', user='root', passwd=pwd)
    myc = con.cursor()
    myc.execute("show databases")
    out1 = myc.fetchall()
    if ("user_info",) not in out1:
        myc.execute("create database user_info")

    myc.execute("use user_info")
    myc.execute("create table if not exists login(Site int, username varchar (50), password varchar (50))")

    
    def open_manager_page():
        root.destroy()
        Login.Manager_login_page(pwd)

    def open_director_page():
        root.destroy()
        Login.Director_login_page(pwd)

    # Colors
    dark_bg = '#232323'
    dark_fg = 'white'

    # Create main window
    root = tk.Tk()
    root.title("Company Portal")
    root.configure(bg=dark_bg)  # Dark background color
    root.geometry("400x300")

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150, 150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040',
                    highlightColor='#404040', font=('Arial', 10, 'bold'))

    # Buttons
    manager_button = ttk.Button(root, text="Manager", command=open_manager_page)
    director_button = ttk.Button(root, text="Director", command=open_director_page)
    manager_button.configure(style='TButton')
    director_button.configure(style='TButton')

    # Configure grid layout
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Grid Placement
    company_name_label.grid(row=0, column=0, columnspan=2, pady=(10, 10))
    company_logo_label.grid(row=1, column=0, columnspan=2, pady=5)
    manager_button.grid(row=2, column=0, columnspan=2)
    director_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="n")

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == '__main__':
    from tkinter import simpledialog
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    pwd = simpledialog.askstring("Database Setup", "Enter MySQL Password:\t\t\t", show="*")
    root.destroy()
    Home_page(pwd)
