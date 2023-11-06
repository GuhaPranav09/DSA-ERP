def display(pwd, site_number, table_name):
    import tkinter as tk
    from tkinter import ttk
    import mysql.connector
    def get_column_info():
        con = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="user_info")
        myc = con.cursor()
        myc.execute(f"SHOW COLUMNS FROM {table_name}")
        column_info = myc.fetchall()
        con.close()
        return column_info

    def populate_treeview():
        for record in tree.get_children():
            tree.delete(record)

        con = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="user_info")
        myc = con.cursor()
        myc.execute(f"SELECT * FROM {table_name} WHERE Site={site_number}")
        data = myc.fetchall()

        for row in data:
            tree.insert("", "end", values=row)

        con.close()

    dark_bg='#232323'
    root = tk.Tk()
    root.title(f"{table_name} Table for Site {site_number}")
    root.configure(bg=dark_bg)  # Dark background color

    # Set window size
    root.geometry("1400x600")  

    column_info = get_column_info()
    columns = [column[0] for column in column_info]

    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)  # Set the Treeview's height
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=200)  # Increased column width

    tree.pack()

    populate_button = tk.Button(root, text="Populate Table", command=populate_treeview)
    populate_button.pack()

    root.mainloop()

def D_display(pwd, site_num, table_name):
    import tkinter as tk
    from tkinter import ttk
    import mysql.connector
    def get_column_info():
        con = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="user_info")
        myc = con.cursor()
        myc.execute(f"SHOW COLUMNS FROM {table_name}")
        column_info = myc.fetchall()
        con.close()
        return column_info

    def populate_treeview():
        for record in tree.get_children():
            tree.delete(record)

        con = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="user_info")
        myc = con.cursor()
        myc.execute(f"SELECT * FROM {table_name}")
        data = myc.fetchall()

        for row in data:
            tree.insert("", "end", values=row)

        con.close()

    dark_bg='#232323'
    root = tk.Tk()
    root.title(f"{table_name} Table")
    root.configure(bg=dark_bg)  # Dark background color

    # Set window size
    root.geometry("1400x600")  

    column_info = get_column_info()
    columns = [column[0] for column in column_info]

    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)  # Set the Treeview's height
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=200)  # Increased column width

    tree.pack()

    populate_button = tk.Button(root, text="Populate Table", command=populate_treeview)
    populate_button.pack()

    root.mainloop()

