from tkinter import *
from tkinter import ttk, messagebox
import imdb
import urllib.request
from datetime import datetime
from time import strftime


class ImdbMovie:
    def __init__(self, root):
        self.root = root
        self.root.title("IMDB Movie Ratings")
        self.root.geometry("700x400")
        self.root.config(bg="black")
        self.imdb_ob = imdb.IMDb()
        self.main_function()

    def main_function(self):
        self.search_txt = StringVar()

        self.frame = Frame(root, bd=1, highlightbackground="light blue", relief=GROOVE)
        self.frame.place(x=0, y=0, width=400, height=600)
        Label(self.frame).place(x=0, y=0)

        self.imdb_frame = Frame(root, bg="light blue")
        self.imdb_frame.place(x=400, y=0, width=300, height=600)

        Label(self.imdb_frame, bg="light blue", text="Movie Search").place(x=10, y=0)

        self.search_E = Entry(self.imdb_frame, width=46, textvariable=self.search_txt)
        self.search_E.place(x=10, y=25)

        ttk.Button(self.imdb_frame, text="search", command=self.search_movie).place(x=214, y=50)
        ttk.Button(self.imdb_frame, text="Movie details", command=self.description).place(x=100, y=50, width=100)

        self.list_frame = Frame(self.imdb_frame, bg="black")
        self.list_frame.place(x=10, y=80, width=278, height=290)
        scrolly = Scrollbar(self.list_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx = Scrollbar(self.list_frame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)
        self.listbox = Listbox(self.list_frame, font=("arial", 10), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrolly.config(command=self.listbox.yview)
        scrollx.config(command=self.listbox.xview)
        self.listbox.pack(expand=TRUE, fill=BOTH)
        self.listbox.selection_set(first=0)

        self.frame1 = Frame(self.imdb_frame, bg="gray")
        self.frame1.place(x=0, y=380, width=300, height=20)
        self.internet = Label(self.frame1, fg="black", bg="gray" )
        self.internet.place(x=10, y=0)
        self.connection()

    def search_movie(self):
        try:
            movie = self.imdb_ob.search_movie(self.search_txt.get())
            self.listbox.delete(0, END)
            for i in range(len(movie)):
                id = movie[i].movieID
                self.listbox.insert(END, movie[i]['title'] + " -- " + id)
            self.listbox.bind('<<ListboxSelect>>', self.active)
        except:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def active(self, e=None):
        self.search_txt.set(self.listbox.get(ANCHOR))

    def description(self):
        try:
            code = self.search_txt.get().split('--')
            print(code)
            if len(code)==1:
                mo = self.imdb_ob.search_movie(code[0])
                id = mo[0].movieID
                self.movie = self.imdb_ob.get_movie(id)
            else:
                self.movie = self.imdb_ob.get_movie(code[1])
            title = self.movie['title']
            director = self.movie['director'][0]
            year = self.movie['year']
            genres = self.movie['genres']
            ratings = self.movie['rating']
            casts = self.movie['cast']

            Label(self.frame, text="Title : ", font=("Times new roman", 13, 'bold')).place(x=10, y=10)
            Label(self.frame, text=title, font=("Times new roman", 13)).place(x=60, y=10)

            Label(self.frame, text="Release Year : ", font=("Times new roman", 13, 'bold')).place(x=10, y=50)
            Label(self.frame, text=str(year), font=("Times new roman", 13)).place(x=120, y=50)

            Label(self.frame, text="Director : ", font=("Times new roman", 13, 'bold')).place(x=10, y=90)
            Label(self.frame, text=str(director), font=("Times new roman", 13)).place(x=90, y=90)

            Label(self.frame, text="Genres : ", font=("Times new roman", 13, 'bold')).place(x=10, y=130)
            Label(self.frame, text=", ".join(genres), font=("Times new roman", 13)).place(x=80, y=130)

            Label(self.frame, text="Ratings : ", font=("Times new roman", 13, 'bold')).place(x=10, y=170)
            Label(self.frame, text=str(ratings), font=("Times new roman", 13)).place(x=85, y=170)

            Label(self.frame, text="Top Casting : ", font=("Times new roman", 13, 'bold')).place(x=10, y=210)
            y = 210
            for i in range(5):
                Label(self.frame, text=str(casts[i]), font=("Times new roman", 13)).place(x=150, y=y)
                y += 40

        except:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def connection(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host)
            internet = 'Internet connected'
        except:
            internet = 'No internet'
        self.internet.config(text=internet) 

root = Tk()
ob = ImdbMovie(root)
mainloop()