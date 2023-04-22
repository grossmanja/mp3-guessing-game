import tkinter as tk
from tkinter import N,S,E,W
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 *  value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

# N = tk.N
# W = tk.W
# E = tk.E
# S = tk.S


root = tk.Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(row=0, column=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = tk.StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(row=1, column=2, sticky=(W,E))

meters = tk.StringVar()
ttk.Label(mainframe, textvariable=meters).grid(row=2, column=2, sticky=(W,E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(row=3, column=2, sticky=W)

ttk.Label(mainframe, text="feet").grid(row=1, column=3, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(row=2, column=1, sticky=E)
ttk.Label(mainframe, text="meters").grid(row=2, column=3, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()