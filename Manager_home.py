def Manager_Home_Page(pwd,site_num,username):    
    import tkinter as tk
    from tkinter import ttk,Label, messagebox
    from PIL import Image, ImageTk
    import Labour, Local_Expenditure, Material_Purchase, Staff_Salary, View_Report, Home
   

    def back():
        root.destroy()
        Home.Home_page(pwd)
    
    def labour():
        root.destroy()
        Labour.Labour_page(pwd, site_num)

    def local_exp():
        root.destroy()
        Local_Expenditure.Local_Expenditure_page(pwd, site_num)

    def material():
        root.destroy()
        Material_Purchase.Material_Purchase_page(pwd, site_num)
    
    def salary():
        root.destroy()
        Staff_Salary.Staff_Salary_page(pwd, site_num)

    def report():
        root.destroy()
        View_Report.D_Report_page(pwd)


    # Colors
    dark_bg='#232323'
    dark_fg='white'

    # Create main window
    root = tk.Tk()
    root.title("Site {}".format(site_num))
    root.configure(bg=dark_bg)  # Dark background color

    # Load your company logo
    company_logo_image = Image.open("company_logo.png").resize((150,150))
    company_logo_photo = ImageTk.PhotoImage(company_logo_image)
    company_logo_label = Label(root, image=company_logo_photo, background=dark_bg)

    # Company Name Label
    company_name_label = Label(root, text="Company Name", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    page_name_label=Label(root, text="Site {}".format(site_num), bg=dark_bg, fg='white', font=('Arial', 16, 'bold'))
    welcome_label = Label(root, text="Welcome", bg=dark_bg, fg='white', font=('Arial', 20, 'bold'))
    message_label = Label(root, text="Site {} Manager {}".format(site_num,username), bg=dark_bg, fg='white', font=('Arial', 30, 'bold'))

    # Set Dark Theme Colors
    style = ttk.Style()
    style.configure('TButton', background=dark_bg, foreground=dark_bg, highlightBackground='#404040', highlightColor='#404040',font=('Arial', 10, 'bold'))

    # Grid Configuration
    for i in range(4):
        root.grid_rowconfigure(i, weight=1)

    # Grid Placement
    company_name_label.grid(row=1, column=3, columnspan=3, sticky="n", pady=5)  
    page_name_label.grid(row=2, column=3, columnspan=3, sticky="n", pady=5)
    company_logo_label.grid(row=3, column=3, columnspan=3, sticky="n", pady=5) 
    welcome_label.grid(row=4, column=3, columnspan=3, sticky="n", pady=[75,5])
    message_label.grid(row=5,column=1, columnspan=7, sticky="n",pady=[5,75])

    back_button = ttk.Button(root, text="Log out", command=back, style='TButton')
    back_button.grid(row=6, column=4, pady=[5, 30])

    # Navigation bar frame
    nav_bar_frame2 = tk.Frame(root, bg="#777777")
    nav_bar_frame2.grid(row=0, column=0, columnspan=8, sticky="news")
    nav_bar_frame = tk.Frame(root, bg="#777777")
    nav_bar_frame.grid(row=0, column=1, columnspan=7, sticky="news")


    # Buttons in the navigation bar
    home_button = ttk.Button(nav_bar_frame, text="Local Expenditure", command=local_exp)
    manager_button = ttk.Button(nav_bar_frame, text="Material Purchase",command=material)
    director_button = ttk.Button(nav_bar_frame, text="Labour", command=labour)
    exit_button = ttk.Button(nav_bar_frame, text="Staff-Salary", command=salary)
    report_button = ttk.Button(nav_bar_frame, text="Report", command=report)
    report_button.configure(style='TButton')
    home_button.configure(style='TButton')  # Apply the style to the button
    manager_button.configure(style='TButton')  
    director_button.configure(style='TButton')  
    exit_button.configure(style='TButton')

    # Grid placement for navigation bar buttonexit
    home_button.grid(row=0, column=1, padx=[100,10], pady=10)
    manager_button.grid(row=0, column=2, padx=10, pady=10)
    report_button.grid(row=0, column=3, padx=10,pady=10)
    director_button.grid(row=0, column=4, padx=10, pady=10)
    exit_button.grid(row=0, column=5, padx=[10,100], pady=10)


    # Run the Tkinter main loop
    root.mainloop()

    

if __name__ == "__main__":
    Manager_Home_Page("mysql",1,"GP")