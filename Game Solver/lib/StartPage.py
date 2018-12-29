import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from functools import partial
import sys
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/lib')#put here the directory of the lib folder
from tools import *



LARGE_FONT = ("Verdana",12)
NORMAL_FONT = ("Verdana",10)
SMALL_FONT = ("Verdana",8)


class StartPage(tk.Frame):
  def __init__(self,parent,controller):
    tk.Frame.__init__(self,parent)
    label = tk.Label(self,text="Choose game", font= LARGE_FONT)
    label.pack(side = tk.TOP , pady =10)
    gameButtons =[]
    for game in controller.games :
      gameButtons.append(ttk.Button(self,command = partial(self.goToGame,controller,game[0],"500x400")))
      #partial is a function that create an "instance" of a function + arguments that is when called it calls the function inside with the arguments inside
      photo = tk.PhotoImage(file="C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/assets/"+game[0]+".gif")#put here the directory of the assets folder
      gameButtons[-1].config(image=photo)
      gameButtons[-1].image = photo
      gameButtons[-1].pack( side = tk.TOP ,pady=5,padx=5)
      
  def goToGame(self,cont,gameName,geo):
    cont.show_frame(gameName,geo)
      
  def getMenu(self,parent):
    menubar = tk.Menu(parent)
    filemenu = tk.Menu(menubar ,tearoff = 0)
    message = "This is a Game Solver, choose the type of game you want to solve !"
    filemenu.add_command(label="Help", command =lambda: mb.showinfo("About!",message))    
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command= parent.destroy)
    menubar.add_cascade(label="File",menu=filemenu)
    return(menubar)
     
      
