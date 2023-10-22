import tkinter as tk
from tkinter import ttk

class CustomButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_color = self['style'].lookup(self['style'], 'background')
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self.configure(style='TButton', background='green')

    def on_leave(self, event):
        self.configure(style='TButton', background=self.default_color)

# Create a root window
root = tk.Tk()

# Create a custom button with the CustomButton class
custom_button = CustomButton(root, text="Custom Button")
custom_button.pack(padx=20, pady=20)

# Run the Tkinter main loop
root.mainloop()
