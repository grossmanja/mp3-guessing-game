import tkinter as tk
from tkinter import N,S,E,W
from tkinter import ttk
from tkinter.messagebox import showinfo
import time

global numOfLimitIncreases
numOfLimitIncreases = 0
limitList = [1,2,4,7,11,16]
print(numOfLimitIncreases)

def updateProgressLabel():
    return "Current Progress: " + str(progressValue.get()) + "%"

# def incrementNumOfLimitIncreases():


# def getNumOfLimitIncreases():
#     return 

def progress():
    print("start")
    pb.start(16)
    print(limitValue.get() * 1000)
    root.after(limitValue.get() * 1000, stop)

def stop():
    print("stop")
    pb.stop()

def increase():
    progressValue.set(0)
    # print(numOfLimitIncreases)
    global numOfLimitIncreases
    numOfLimitIncreases += 1
    limitValue.set(limitList[numOfLimitIncreases])
    # value_label['text'] = updateProgressLabel()

root = tk.Tk()
root.title("General Guessing Game GUI")
root.geometry("500x500")

progressValue = tk.DoubleVar()
limitValue = tk.IntVar(value=limitList[0])

pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=450, variable=progressValue)

# place the progressbar
pb.grid(column=0, row=0, columnspan=3, padx=10, pady=20)

# label
value_label = ttk.Label(root, text=updateProgressLabel())
value_label.grid(column=0, row=1, columnspan=2)

# start button
start_button = ttk.Button(
    root,
    text='Progress',
    command=progress
)
start_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.E)

pause_button = ttk.Button(
    root,
    text="Pause",
    command=stop 
)
pause_button.grid(column=1, row=3, padx=10, pady=10, sticky=tk.E)

limit_increase_button = ttk.Button(
    root,
    text='Increase',
    command=increase
)
limit_increase_button.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)

# for child in root.winfo_children():
#     child.grid_configure(padx=10, pady=10)

root.mainloop()