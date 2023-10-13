def Login_page():
    import tkinter as tk
    from tkinter import ttk, Label, messagebox
    import mysql.connector
    from PIL import Image, ImageTk
    import Labour

    # Function to handle login button click event
    def login():
        # Connect to the MySQL database
        con = mysql.connector.connect(host='localhost', user='root', passwd='mysql', database='user_info')
        myc = con.cursor()

        # Retrieve username and password from the entry fields
        username = username_entry.get()
        password = password_entry.get()

        # Check if the login details match the records in the database
        myc.execute("SELECT * FROM login WHERE username=%s AND password=%s", (username, password))
        result = myc.fetchone()

        # If login details match, close the login window and open the user information window
        if result:
            login_window.destroy()  # Close the login window
            Labour.Labour_page()  # Open the user information window
        else:
            messagebox.showerror("Error", "Invalid login credentials. Please try again.")
        

    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create login window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg=dark_bg)  # Dark background color
    login_window.geometry("400x300")  # Set window size

    # Load your image using the Image class from Pillow
    icon_image = Image.open("icon.png")
    icon_photo = ImageTk.PhotoImage(icon_image)
    login_window.iconphoto(True, icon_photo)

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))
    style.configure('TLabel', background=dark_bg, foreground=dark_fg, font=('Arial', 12))

    # Login Label
    login_label = Label(login_window, text="Manager Login", bg=dark_bg, fg=dark_fg, font=('Arial', 20, 'bold'))

    # Username Label and Entry
    username_label = ttk.Label(login_window, text="Username:", style='TLabel')
    username_entry = ttk.Entry(login_window, font=('Arial', 12))

    # Password Label and Entry
    password_label = ttk.Label(login_window, text="Password:", style='TLabel')
    password_entry = ttk.Entry(login_window, show='*', font=('Arial', 12))

    # Login Button
    login_button = ttk.Button(login_window, text="Login", command=login, style='TButton')
    # Bind the Enter key to the login button's command
    login_window.bind('<Return>', lambda event=None: login_button.invoke())

    # Center all elements
    login_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")
    username_label.grid(row=1, column=0, pady=10, sticky="e")
    username_entry.grid(row=1, column=1, pady=10, sticky="w")
    password_label.grid(row=2, column=0, pady=10, sticky="e")
    password_entry.grid(row=2, column=1, pady=10, sticky="w")
    login_button.grid(row=3, column=0, columnspan=2, pady=20)

    # Configure grid row and column weights to center everything
    login_window.grid_rowconfigure(0, weight=1)
    login_window.grid_rowconfigure(3, weight=1)
    login_window.grid_columnconfigure(0, weight=1)
    login_window.grid_columnconfigure(1, weight=1)

    # Run the Tkinter main loop for login window
    login_window.mainloop()

Login_page()