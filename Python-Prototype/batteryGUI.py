from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
import getBattery

# root window
root = tk.Tk()
root.geometry('300x120')
root.title('Progressbar Demo')


def update_percent_label():
    return f"Battery Percentage: {pb['value']}%"




def updateData():
        pb['value'] = getBattery.GetBattery()
        value_label['text'] = update_percent_label()
        root.after(2000, updateData)



# progressbar
pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=280
)
# place the progressbar
pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

# label
value_label = ttk.Label(root, text=update_percent_label())
value_label.grid(column=0, row=1, columnspan=2)


updateData()

root.mainloop()