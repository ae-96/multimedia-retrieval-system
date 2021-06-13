from tkinter import *
from tkinter import font as tkFont
import tkinter.messagebox
from PIL import ImageTk, Image
import cv2
import matplotlib.pyplot as plt
from  tkinter import  filedialog
import PIL.Image, PIL.ImageTk
import os
from db import *

class gui:
    def __init__(self):

        self.folder_path=""
        self.master=Tk()
        self.master.title("Content Based MultiMedia Retrieval System ")
        self.master.geometry("1100x600")
        self.root = Frame(self.master)
        self.root.pack()
        self.File_Path=""
        self.search_or_insert = Label(self.root, text="Select Operation", font="Helvetica 40 ")
        self.search_or_insert.pack(pady=50)

        self.clicked2 = StringVar()
        self.clicked2.set("Retrieve")

        self.dropp = OptionMenu(self.root, self.clicked2, "Retrieve", "DataBase Insertion","Clear DataBase")
        helv20 = tkFont.Font(family='Helvetica', size=34)
        self.dropp.config(font=helv20)
        menu = self.root.nametowidget(self.dropp.menuname)
        menu.config(font=helv20)  # Set the dropdown menu's font
        self.dropp.pack(pady=10)

        self.ok = Button(self.root, text="OK", command=self.OK2, font="Helvetica 26 ", width=4)
        self.ok.pack(pady=60)





        self.master.mainloop()

    def OK2(self):
        self.dropp.destroy()
        self.search_or_insert.destroy()
        self.ok.destroy()
        if self.clicked2.get()=="Retrieve":
            self.conn = start_db()

            self.clicked = StringVar()
            self.clicked.set("Image")
            self.mode = Label(self.root, text="Please Select MultiMedia Type ", font="Helvetica 37 ")
            self.mode.pack(pady=50)
            self.drop = OptionMenu(self.root, self.clicked, "Image", "Video")
            helv20 = tkFont.Font(family='Helvetica', size=34)
            self.drop.config(font=helv20)
            menu = self.root.nametowidget(self.drop.menuname)
            menu.config(font=helv20)  # Set the dropdown menu's font
            self.drop.pack(pady=40)

            self.ok = Button(self.root, text="OK", command=self.OK, font="Helvetica 26 ", width=4)
            self.ok.pack(pady=40)
            self.Reset = Button(self.root, text="Reset", command=self.reset, font="Helvetica 18 ", width=5)
            self.Reset.pack(side="bottom",pady=20)
        elif self.clicked2.get()=="DataBase Insertion":
            self.conn = start_db()

            self.Reset = Button(self.root, text="Reset", command=self.reset, font="Helvetica 18 ", width=5)
            self.Reset.pack(side="bottom", pady=20)
            self.browse_data = Button(self.root, text="Browse", command=self.browse_d, font="Helvetica 28 ",
                                 width=10)
            self.browse_Data_label = Label(self.root, text="Please Browse MultiMedia Folder", font="Helvetica 30 ")

            self.browse_Data_label.pack(pady=30)
            self.browse_data.pack(pady=30)

            self.ok = Button(self.root, text="OK", command=self.add, font="Helvetica 26 ", width=4)
            self.ok.pack(pady=40)
        else:
            self.Reset = Button(self.root, text="Reset", command=self.reset, font="Helvetica 18 ", width=5)
            self.Reset.pack(side="bottom", pady=20)

            self.Clear=Button(self.root, text="Clear DataBase", command=self.clear, font="Helvetica 28 ",
                                 width=15)
            self.Clear.pack(pady=30)




    def clear(self):
        for i in os.listdir(os. getcwd()):
            if i== "mm.db":
                path = os. getcwd()+"\\"+i
                if self.conn:
                    self.conn.close()
                os.remove(path)
        self.reset()




    def add(self):
        if self.folder_path == "":
            tkinter.messagebox.showinfo("error", "Please Select a non Empty Path")
            self.browse_d()
        self.reset()


    def browse_d(self):
        self.folder_path = self.filedialog("folder")
        self.content_list_images=[]
        self.content_list_videos=[]

        if self.folder_path == "":
            tkinter.messagebox.showinfo("error", "Please Select a non Empty Path")
            self.browse_d()
        for i in os.listdir(self.folder_path):
            if i[-3:]!="mp4":
                self.content_list_images.append(self.folder_path+"/"+i)
            else:
                self.content_list_videos.append(self.folder_path + "/" + i)

        for i in self.content_list_images:
            insert_image(self.conn, i)
        for i in self.content_list_videos:
            inser_video(self.conn, i)


    def reset(self):
        self.master.destroy()
        self.folder_path = ""
        self.master = Tk()
        self.master.title("Content Based MultiMedia Retrieval System ")
        self.master.geometry("1100x600")
        self.root = Frame(self.master)
        self.root.pack()
        self.File_Path = ""
        self.search_or_insert = Label(self.root, text="Select Operation", font="Helvetica 40 ")
        self.search_or_insert.pack(pady=50)

        self.clicked2 = StringVar()
        self.clicked2.set("Retrieve")

        self.dropp = OptionMenu(self.root, self.clicked2, "Retrieve", "DataBase Insertion", "Clear DataBase")
        helv20 = tkFont.Font(family='Helvetica', size=34)
        self.dropp.config(font=helv20)
        menu = self.root.nametowidget(self.dropp.menuname)
        menu.config(font=helv20)  # Set the dropdown menu's font
        self.dropp.pack(pady=10)

        self.ok = Button(self.root, text="OK", command=self.OK2, font="Helvetica 26 ", width=4)
        self.ok.pack(pady=60)

        self.master.mainloop()


    def OK(self):
        self.selected=self.clicked.get()
        self.mode.destroy()
        self.ok.destroy()
        self.drop.destroy()
        if self.selected == "Image":
            self.label = Label(self.root, text="Please Select The Search Algorithm", font="Helvetica 30 ")
            self.label.pack(pady=25)

            self.clicked1 = StringVar()
            self.clicked1.set("Mean Color Algorithm")

            self.alg = OptionMenu(self.root, self.clicked1, "Mean Color Algorithm", "Histogram Algorithm", "Color Layout Algorithm")
            helv20 = tkFont.Font(family='Helvetica', size=24)
            self.alg.config(font=helv20)
            menu = self.root.nametowidget(self.alg.menuname)
            menu.config(font=helv20)  # Set the dropdown menu's font
            self.alg.pack(pady=10)
            self.browse = Button(self.root, text=" Browse Image", command=self.browsee, font="Helvetica 24 ",
                                 width=12)
            self.browse_label = Label(self.root, text="Please Browse Query Image", font="Helvetica 30 ")




        else:
            self.label = Label(self.root, text="Available Algorithm", font="Helvetica 30 ")
            self.label.pack()

            self.clicked1 = StringVar()
            self.clicked1.set("CBVR")

            self.alg = OptionMenu(self.root, self.clicked1,"CBVR")
            helv20 = tkFont.Font(family='Helvetica', size=24)
            self.alg.config(font=helv20)
            menu = self.root.nametowidget(self.alg.menuname)
            menu.config(font=helv20)  # Set the dropdown menu's font
            self.alg.pack(pady=10)
            self.browse = Button(self.root, text=" Browse Video", command=self.browsee, font="Helvetica 24 ",
                                 width=15)
            self.browse_label = Label(self.root, text="Please Browse Query Video", font="Helvetica 30 ")


        self.browse_label.pack(pady=20)
        self.browse.pack(pady=10)



        self.ok1 = Button(self.root, text="OK", command=self.OK1, font="Helvetica 22 ", width=4)
        self.ok1.pack(pady=10)

    def filedialog(self,folder=""):
        if folder=="folder":
            self.filename = filedialog.askdirectory(title="Select MultiMedia Folder")
            return self.filename
        else:
            self.filename=filedialog.askopenfilename(title="Select A File",filetype=(("ALL","*.*"),("Img","*.jpg"),("Img","*.PNG"),("Vid","*.mp4")))
            return self.filename

    def OK1(self):
        type = self.clicked1.get()
        self.list_images = []
        if self.File_Path == "":
            tkinter.messagebox.showinfo("error","Please Select a non Empty Path")
            self.browsee()
        self.selected_algorithm = self.clicked1.get()
        self.root.destroy()
        self.root=Frame(self.master)
        self.root.pack()
        self.Reset = Button(self.root, text="Reset", command=self.reset, font="Helvetica 18 ", width=5)
        self.Reset.pack(side="bottom")

        self.label = Label(self.root, text="Results", font="Helvetica 30 ")
        self.label.pack()
        if type=="Mean Color Algorithm":
            type="mean"
        elif type=="Histogram Algorithm":
            type="hist"
        else :
            type="layout"

        if self.selected == "Video":
            string=""
            self.list_images = search_video(self.conn, self.filename)
            canvas = Canvas(self.root, width=1500, height=1500)

            for i in self.list_images:
                string+=i+"\n"
            canvas.create_text(string)


        if self.selected == "Image":
            self.list_images = search_image(self.conn, self.filename, type)
            canvas = Canvas(self.root,width=1500,height=1500)

            canvas.pack(side="bottom")

            index_x=20
            index_y=0
            images_list=[]
            k=1
            for i in self.list_images:


                image = PhotoImage(file=i)
                image=image.subsample(9, 9)
                images_list.append(image)

            for i in images_list:
                canvas.create_image(index_x,index_y,anchor = NW, image =i)
                index_x+=200
                if ((k % 7 )==0) :
                    index_x = 20
                    index_y+=240
                k+=1
            canvas.create_image(index_x, index_y, anchor=NW, image=images_list[0])


            self.master.mainloop()



    def browsee(self):
        self.File_Path = self.filedialog()

        if self.File_Path == "":
            tkinter.messagebox.showinfo("error","Please Select a non Empty Path")
            self.browsee()





