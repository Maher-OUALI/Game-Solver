import tkinter as tk
from tkinter import ttk
from functools import partial
from lib.WordsearchPuzzle import *
from lib.Sudoku import *
from lib.StartPage import *


class GameSolver(tk.Tk):
  def __init__(self,*args,**kwargs):
    #initialize a Tkinter Object to be able to create a GUI
    tk.Tk.__init__(self,*args,**kwargs)
    self.title("Game Solver")
    
    container = tk.Frame(self)

    container.pack(side="top", fill="both", expand = True)
    container.grid_rowconfigure(0,weight =1)
    container.grid_columnconfigure(0,weight=1)
    
    self.games = (("Sudoku",Sudoku),("WordsearchPuzzle",WordsearchPuzzle))
    self.frames ={} # a dictionnary containing all possible frames
    
    #initialise startPage
    frame = StartPage(container, self)
    self.frames["StartPage"] = frame
    frame.grid(row=0, column=0,sticky="nsew")

    #initialise gamePages
    for Game in self.games:
      frame = Game[1](container, self)
      self.frames[Game[0]] = frame
      frame.grid(row=0, column=0,sticky="nsew")

    #show startPage  
    self.show_frame("StartPage","300x"+str(210*len(self.games)+100))
    
  def show_frame(self,cont,geo):
    #rectify app geometry so it fits the new frame 
    self.geometry(geo)
    #load the correct frame
    frame = self.frames[cont]
    #raise the frame
    frame.tkraise()
    #get the menubar correspondant to the correct frame
    menubar = frame.getMenu(self)
    #configure it to the app
    self.config(menu=menubar)


    
    
#main()
if __name__ == "__main__":
  app = GameSolver()
  app.resizable(width=False, height=False)
  app.mainloop()
