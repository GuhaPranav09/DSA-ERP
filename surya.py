import tkinter as tk
from tkinter import ttk
import mysql.connector

# Establish a MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='#######',
    database='MainSite'
)
print("Connected to MySQL:", conn.is_connected())
cursor = conn.cursor()

def submit():
    
    reg_number = reg_number_entry.get()
    reg_name = reg_name_entry.get()

    # Convert the input date (DDMMYY) to the YYYYMMDD format
    input_date = dob_entry.get()
    try:
        dob = datetime.datetime.strptime(input_date, "%d%m%y").strftime("%Y%m%d")
    except ValueError:
        print("Invalid date format. Please enter the date in DDMMYY format.")
        return

    gender = gender_var.get()
    languages = [lang for lang, val in lang_vars.items() if val.get()]
    address = address_text.get("1.0", tk.END)
    designation = designation_combobox.get()

    # Insert data into Site1 table
    insert_query = "INSERT INTO Site1 (registration_number, name, dob, gender, languages, address, designation) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (reg_number, reg_name, dob, gender, ", ".join(languages), address, designation)

    try:
        cursor.execute(insert_query, data)
        conn.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

    # Print the gathered information
    print("Data inserted into MySQL database:")
    print("Registration Number:\t", reg_number)
    print("Name:\t\t\t", reg_name)
    print("Date of Birth:\t\t", dob)
    print("Gender:\t\t\t", gender)
    print("Languages known:\t", ", ".join(languages))
    print("Address:\n", address)
    print("Designation:\t\t", designation)
    print()


# Create the main application window
root = tk.Tk()
root.title("User Registration Form")
root.configure(bg='#272727')  # Set background color for the window

# Style settings for a dark theme
style = ttk.Style()
style.configure('TLabel', foreground='white', background='#272727', font=('Arial', 12, 'bold'))
style.configure('TButton', foreground='black', background='#2B35AF', font=('Arial', 12, 'bold'))
style.configure('TRadiobutton', background='#272727', font=('Arial', 12), foreground='white')
style.configure('TCheckbutton', background='#272727', font=('Arial', 12), foreground='white')
style.configure('TEntry', font=('Arial', 12))

# Labels
reg_number_label = ttk.Label(root, text="Registration Number:")
reg_number_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
reg_name_label = ttk.Label(root, text="Registration Name:")
reg_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
dob_label = ttk.Label(root, text="Date of Birth:")
dob_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
gender_label = ttk.Label(root, text="Gender:")
gender_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
lang_label = ttk.Label(root, text="Languages known:")
lang_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
address_label = ttk.Label(root, text="Address:")
address_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)
designation_label = ttk.Label(root, text="Designation:")
designation_label.grid(row=10, column=0, padx=10, pady=5, sticky=tk.W)

# Entry widgets with bluish-grey tone
reg_number_entry = ttk.Entry(root, font=('Arial', 12))
reg_number_entry.grid(row=0, column=1, padx=10, pady=5, ipady=2)  # Adjusted padding
reg_name_entry = ttk.Entry(root, font=('Arial', 12))
reg_name_entry.grid(row=1, column=1, padx=10, pady=5, ipady=2)  # Adjusted padding
dob_entry = ttk.Entry(root, font=('Arial', 12))
dob_entry.grid(row=2, column=1, padx=10, pady=5, ipady=2)  # Adjusted padding

# Gender radio buttons
gender_var = tk.StringVar(value="Male")  # Default value
male_radio = ttk.Radiobutton(root, text="Male", variable=gender_var, value="Male")
male_radio.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
female_radio = ttk.Radiobutton(root, text="Female", variable=gender_var, value="Female")
female_radio.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E)

# Languages checkboxes
languages = ["English", "Hindi", "Malayalam", "Tamil"]
lang_vars = {lang: tk.BooleanVar() for lang in languages}
checkboxes = [ttk.Checkbutton(root, text=lang, variable=lang_vars[lang]) for lang in languages]
for idx, checkbox in enumerate(checkboxes):
    checkbox.grid(row=idx + 4, column=1, padx=10, pady=2, sticky=tk.W)

# Address text box
address_text = tk.Text(root, width=40, height=5, bg='#4a4a4a', fg='white')
address_text.grid(row=8, column=1, padx=10, pady=5, rowspan=2)

# Designation dropdown
designation_combobox = ttk.Combobox(root, values=["Student", "Teacher", "Researcher", "Faculty", "HOD"])
designation_combobox.grid(row=10, column=1, padx=10, pady=5)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=submit, style='TButton')
submit_button.grid(row=11, column=0, columnspan=2, pady=10, ipadx=20)  # Adjusted padding and width

# Run the main event loop
root.mainloop()