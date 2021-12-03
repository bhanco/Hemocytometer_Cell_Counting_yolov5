import tkinter as tk
from tkinter import filedialog
from tkinter import *
import cell_count_functions
import os
from datetime import datetime
datetime.now().strftime("%Y-%m-%d hour %H minute %M")

root = tk.Tk()

def browse_botton():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    button2['state'] = 'normal'

def run_button():
    cell_count_functions.run_count(folder_path.get())
    curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #very confused here, toggling the run_count line above changes the results of __file__ to the yolov5-master
    os.chdir(script_dir)
    counts_txt = open(os.path.join(script_dir,"counts",curr_time + ".txt"), 'a')
    late_dir = cell_count_functions.get_latest_file(os.path.join(script_dir,'yolov5-master','runs','detect'), 'last_run_cells*')
    label_dir = os.path.join(late_dir, 'labels')
    cell_label_files = os.listdir(label_dir)
    cell_label_files.sort()
    for fi in cell_label_files:
        f = open(os.path.join(label_dir,fi),'r')
        count = len(f.readlines())
        line = fi[:-4] + ': ' + str(count) + ' cells\n'
        counts_txt.write(line)
    button3['state'] = 'normal'


def counts_button():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.startfile(r"" + cell_count_functions.get_latest_file(os.path.join(script_dir, "counts"),"*"))



root.title('Hemocytometer cell counting with yolov5')

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

#text instructions
instructions = tk.Label(root, text= "Select folder with hemocytometer images to count, then click the Run button")
instructions.grid(columnspan=3, column = 0, row = 0)
#
button1 = Button(text="Select folder", command=browse_botton, bg="#20bebe", fg="white")
button1.grid(row=1, column=0)

button2 = Button(root, text="Run", bg="#20bebe", command=run_button, fg="white", state='disabled')
button2.grid(row=2, column=0)

button3 = Button(text="Show Counts", command=counts_button, bg="#20bebe", fg="white", state='disabled')
button3.grid(row=3, column=0)

folder_path = StringVar()
lbl1 = Label(master=root, textvariable=folder_path)
lbl1.grid(row=1, column=1)



#browse button
#orig_folder = filedialog.askdirectory(initialdir='.', title="Slect folder with pictures to count")
#print(orig_folder)


root.mainloop()
