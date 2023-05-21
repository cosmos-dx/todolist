import sqlite3
import os
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

class todo (Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.td = self.master
        if not (os.path.isfile('todo.db')):
            self.cnn = sqlite3.connect('todo.db')
            self.crr = self.cnn.cursor()
            self.crtbl(self.crr)
        else:
            self.cnn = sqlite3.connect('todo.db')
            self.crr = self.cnn.cursor()
        self.sw = self.td.winfo_screenwidth()          #### screen width
        self.sh = self.td.winfo_screenheight()         #### screen height
        self.w = 700
        self.h = 400                
        self.xpos =(self.sw/2) - (self.w/2)            #### calculation for centre
        self.ypos =(self.sh/2) - (self.h/2)
        self.td.geometry('%dx%d+%d+%d' % (self.w, self.h, self.xpos, self.ypos))
        
        self.entbx = StringVar()
        
        self.canvas = Canvas(self.master, bg = "#ffffff", height = 400,
                        width = 700, bd = 0, highlightthickness = 0,
                        relief = "ridge")
        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(0,0,0+250,0+400,
                                     fill = "#50A0FF", outline = "")
        self.canvas.create_text(110, 36.0, text = "To-Do List",
                           fill = "#ffffff",
                           font = ("Roboto-Bold", int(32.0)))
        
        self.canvas.create_text( 110, 73.0, text = "Created by - Ananya Baranwal",
            fill = "#ffffff",
            font = ("Roboto-Bold", int(10.0)))
        self.image = Image.open('image/img3.png')
        self.image1 = ImageTk.PhotoImage(self.image)
        Label(self.canvas, image=self.image1 , bg="#50A0FF").place(x=15, y=200)
        

        self.canvas.create_text( 310.0, 28.0, text = "Add Task",
            fill = "#000000",
            font = ("Roboto-Medium", int(14.0)))
        

        self.canvas.create_text( 305, 50.5, text = "Create a task",
        fill = "#000000",
        font = ("None", int(8.0)))

    
        self.entry0 = Entry( bd = 0, bg = "#e5e5e5",
        highlightthickness = 0,
        textvariable= self.entbx)

        self.entry0.place( x = 274.0, y = 65, width = 217.0,
        height = 24)

        self.entry0_img = PhotoImage(file = f"image/img_textBox0.png")
        entry0_bg = self.canvas.create_image( 382.5, 78.0,
        image = self.entry0_img)

    
        self.img0 = PhotoImage(file = f"image/img0.png")
        b0 = Button(image = self.img0, borderwidth = 0,
            highlightthickness = 0,
            command = self.add_task, relief = "flat")
        b0.place( x = 510, y = 64, width = 31,
            height = 28)

        self.task_list()
        self.img_delete = PhotoImage(file = f"image/img_delete.png")
        b1 = Button(image=self.img_delete, borderwidth = 0, highlightthickness = 0,
            relief = "flat", 
            command=self.delete_task,
            bg='#65daff', fg='#fff',
            font= ("Roboto-Medium", int(12.0)))

        b1.place( x = 567, y = 120,)
        self.canvas.create_text( 310.0, 130.0, text = "Task List",
        fill = "#000000",
        font = ("Roboto-Medium", int(14.0)))
        
        

    def task_list(self):
        records = self.crr.execute("SELECT * FROM todo")
        show = ""

        scrollbar = Scrollbar(self.canvas, width=15)
        scrollbar.place(x = 645, y=155,  relheight=0.5)
        self.list1 = Listbox(self.canvas,  bg = "#fff", font = ("None", 13), relief='flat', 
                        width=40, selectmode=SINGLE, 
                        yscrollcommand=scrollbar.set, )
        self.list1.place(x=272, y=155)
        scrollbar.config(command=self.list1.yview)
        id1 = 0
        for task, date, time in records:
            id1 += 1 
            show = str(id1)+"    "+task+"       "+date+"  "+time +"\n"
            self.list1.insert(END, show)

        
    def crtbl (self, crr):
        qry = (''' CREATE TABLE IF NOT EXISTS todo(
                   task TEXT,
                   date DATE,
                   time TIME TEXT)''')
        self.crr.execute(qry)

    def add_task(self):
        self.date_time = datetime.now()
        dt_string = self.date_time.strftime("%d/%m/%Y %H:%M")
        if len(self.entbx.get()) != 0:
            self.crr.execute("INSERT INTO todo VALUES(:task, :date, :time)",{
                'task':str(self.entbx.get()).strip(),
                'date': str(dt_string[:10]),
                'time': str(dt_string[10:])})
            self.cnn.commit()
            self.entry0.delete(0, 'end')
            self.task_list()
        else:
            messagebox.showerror('Add Task', 'Write your task name')

    def delete_task(self):
        try: 
            val = int(self.list1.curselection()[0])
            data_list = (self.list1.get(val)).split("    ")
            self.crr.execute("DELETE FROM todo WHERE task='%s'"% str(data_list[1]))
            self.cnn.commit()
            self.task_list()
        except:
            messagebox.showerror('Select Task', 'Select Task Which You Have To Delete')

    
def main():
    root = Tk()
    todo(root)
    root.title("To Do List")
    root.resizable(False, False)
    root.mainloop()
    
if __name__ == "__main__":
    main()
