def report_page(pwd, site_num):
    import tkinter as tk
    from tkinter import ttk, messagebox
    import mysql.connector
    from datetime import datetime

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

    
    root = tk.Tk()
    root.title("Generate Report")
    root.geometry("400x500")
    root.configure(bg='#232323')  # Dark background color

    # Labels
    label_category = tk.Label(root, text="Select category:", bg='#232323', fg='white', font=('Arial', 12))
    label_category.pack(pady=10)

    # Dropdown menu for category
    categories = ["Expenditure", "Purchase"]
    category_var = tk.StringVar()
    dropdown_category = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly")
    dropdown_category.pack(pady=10)

    # Label and Dropdown menu for year
    label_year = tk.Label(root, text="Select year:", bg='#232323', fg='white', font=('Arial', 12))
    label_year.pack(pady=10)

    years = get_years()
    years.insert(0,"All Years")
    year_var = tk.StringVar()
    dropdown_year = ttk.Combobox(root, textvariable=year_var, values=years, state="readonly")
    dropdown_year.pack(pady=10)

    # Label and Dropdown menu for month
    label_month = tk.Label(root, text="Select month:", bg='#232323', fg='white', font=('Arial', 12))
    label_month.pack(pady=10)

    months = ["Overall", "01 (January)", "02 (February)", "03 (March)", "04 (April)", "05 (May)", "06 (June)", "07 (July)",
            "08 (August)", "09 (September)", "10 (October)", "11 (November)", "12 (December)"]
    month_var = tk.StringVar()
    dropdown_month = ttk.Combobox(root, textvariable=month_var, values=months, state="readonly")
    dropdown_month.pack(pady=10)

    # View Report button
    
    btn_view_report = tk.Button(root, text="View Report", command=lambda: view_report(category_var.get(), year_var.get(), month_var.get()), font=('Arial', 12))
    btn_view_report.pack(pady=20)

    root.mainloop()


def D_report_page(pwd, site_num=0):
    import tkinter as tk
    from tkinter import ttk, messagebox
    import mysql.connector
    from datetime import datetime

    def get_years():
        current_year = datetime.now().year
        return [str(year) for year in range(2015, current_year + 1)]

    def view_report(category, selected_year, selected_month, site_num):
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
                messagebox.showinfo("Report", f"Total {category} amount for Site {site_num} {msg_month} {selected_year}: {result} Rs")
            else:
                messagebox.showinfo("Report", f"No {category} data available for Site {site_num} {msg_month} {selected_year}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")

    
    root = tk.Tk()
    root.title("Generate Report")
    root.geometry("400x400")
    root.configure(bg='#232323')  # Dark background color

    # Labels
    label_category = tk.Label(root, text="Select category:", bg='#232323', fg='white', font=('Arial', 12))
    label_category.pack(pady=10)

    # Dropdown menu for category
    categories = ["Expenditure", "Purchase"]
    category_var = tk.StringVar()
    dropdown_category = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly")
    dropdown_category.pack(pady=10)

    # Label and Dropdown menu for month
    label_site = tk.Label(root, text="Select Site:", bg='#232323', fg='white', font=('Arial', 12))
    label_site.pack(pady=10)
    site_entry = tk.Entry(root, font=('Arial',12))
    site_entry.pack(pady=10)

    # Label and Dropdown menu for year
    label_year = tk.Label(root, text="Select year:", bg='#232323', fg='white', font=('Arial', 12))
    label_year.pack(pady=10)

    years = get_years()
    years.insert(0,"All Years")
    year_var = tk.StringVar()
    dropdown_year = ttk.Combobox(root, textvariable=year_var, values=years, state="readonly")
    dropdown_year.pack(pady=10)

    # Label and Dropdown menu for month
    label_month = tk.Label(root, text="Select month:", bg='#232323', fg='white', font=('Arial', 12))
    label_month.pack(pady=10)

    months = ["Overall", "01 (January)", "02 (February)", "03 (March)", "04 (April)", "05 (May)", "06 (June)", "07 (July)",
            "08 (August)", "09 (September)", "10 (October)", "11 (November)", "12 (December)"]
    month_var = tk.StringVar()
    dropdown_month = ttk.Combobox(root, textvariable=month_var, values=months, state="readonly")
    dropdown_month.pack(pady=10)

    # View Report button
    
    btn_view_report = tk.Button(root, text="View Report", command=lambda: view_report(category_var.get(), year_var.get(), month_var.get(), site_entry.get()), font=('Arial', 12))
    btn_view_report.pack(pady=20)

    root.mainloop()



if __name__ == "__main__":
    D_report_page("mysql")
