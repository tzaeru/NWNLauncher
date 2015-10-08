from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
    
root = Tk()
root.title("Feet to Meters")
#root.geometry("170x200+30+30") 

ttk.Style().configure("TButton", padding=6, relief="flat",
   background="#595b59")

mainframe = ttk.Frame(root, padding="0 0 0 0")
#mainframe.geometry("170x200+30+30")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#mainframe.columnconfigure(0, weight=1)
#mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

background_image=PhotoImage(file="images/potm_title.png").zoom(x = 1, y = 1)
background_label = Label(mainframe, image=background_image, borderwidth=0)
background_label.grid(row=0,column=0, rowspan=6, columnspan=6)

progress = ttk.Progressbar(mainframe)
progress.grid(row=4,column=0)

stacy = ttk.Button(mainframe, text = 'yoyo')
stacy.grid(row=5,column=0)
#stacy.place(x=0, y=0, relwidth=1, relheight=1)

#background_label.grid_configure()
#for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()