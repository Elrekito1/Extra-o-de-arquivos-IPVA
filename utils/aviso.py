import sys
import tkinter as tk
from tkinter import filedialog

def aviso(msg: str):
    
    root = tk.Tk()
    root.title("AVISO!")
    root.geometry("600x100")
    root.configure(bg='gray15')  
    root.iconbitmap('img/logo.ico')

    label_style = {'bg': 'gray15', 'fg': 'white'}  
    button_style = {'bg': 'gray30', 'fg': 'white', 'activebackground': 'gray50', 'activeforeground': 'white', 'borderwidth': 0}

    label = tk.Label(root, text=msg, **label_style)
    label.pack(pady=10, padx=20)
    
    button = tk.Button(root, text="Ok", command=sys.exit, **button_style)
    button.pack(pady=10, padx=20, ipadx=20, ipady=5) 
    
    root.mainloop()
