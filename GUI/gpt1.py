import tkinter as tk
from tkinter import messagebox

class Parameters:
    def __init__(self, param1, param2, param3, param4, param5):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.param5 = param5


def submit():
    my_params = Parameters(entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get())
    messagebox.showinfo("Parameters", "Parameters stored in the class successfully")


root = tk.Tk()

label1 = tk.Label(root, text='Parameter 1:')
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text='Parameter 2:')
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

label3 = tk.Label(root, text='Parameter 3:')
label3.pack()
entry3 = tk.Entry(root)
entry3.pack()

label4 = tk.Label(root, text='Parameter 4:')
label4.pack()
entry4 = tk.Entry(root)
entry4.pack()

label5 = tk.Label(root, text='Parameter 5:')
label5.pack()
entry5 = tk.Entry(root)
entry5.pack()

submit_button = tk.Button(root, text='Submit', command=submit)
submit_button.pack()

root.mainloop()