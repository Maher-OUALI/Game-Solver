import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import pytesseract
from time import time
from functools import partial
import sys
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/lib')#put here the directory of the lib folder
from tools import *
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/assets')#put here the directory of the assets folder
from Constants import *
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/solvers')#put here the directory of the solvers folder
from SudokuSolver import SudokuSolver


class Sudoku(tk.Frame):
  def __init__(self,parent,controller):
    tk.Frame.__init__(self,parent) #the parent is the application frame that is on this current frame (in this case it's GameSolver)
    self.controller = controller
    label = tk.Label(self, text="Sudoku Solver", font = LARGE_FONT)
    label.pack(pady=10,padx=10)
    homeButton = ttk.Button(self,text = "What to do !", command = lambda: mb.showinfo("Game Solver","Start by choosing New Game !"))
    homeButton.pack()

  def getMenu(self,parent):
    """this function creates the menu for the Sudoku Frame"""
    self.menu = tk.Menu(parent)
    self.filemenu = tk.Menu(self.menu ,tearoff = 0)
    new_gameOption = tk.Menu(self.filemenu ,tearoff = 0)
    new_gameOption.add_command(label="Camera Input", command = lambda: self.launchGame_CameraInput())
    new_gameOption.add_command(label="Manual Input", command = lambda: self.launchGame_ManualInput())
    self.filemenu.add_cascade(label = "New Game Solver", menu= new_gameOption)
    self.filemenu.add_separator()
    self.filemenu.add_command(label="Return", command = lambda: self.controller.show_frame("StartPage","300x"+str(210*len(self.controller.games)+100)))
    self.filemenu.add_command(label="Exit", command = parent.destroy)
    self.menu.add_cascade(label="File",menu=self.filemenu)
    self.helpmenu = tk.Menu(self.menu ,tearoff = 0)
    message = "This is a Sudoku Solver, you add a new game either by typing the numbers or by importing an image"
    self.helpmenu.add_command(label="About", command = lambda: mb.showinfo("About!",message))
    self.menu.add_cascade(label="Help",menu=self.helpmenu)
    return(self.menu)
  
  def solve():
      """this function solves the wordseaerch puzzle given and returns the correspondant cell and direction of each word"""
      self.solveButton.config(state="disabled")
      self.grid=empty((9,9),dtype=str)
      try:
        for row in range(9):
          for column in range(9):
            self.grid[row,column]=int(self.numberStringVar[(row,column)].get())
      except:
        mb.showerror("Entry Error","Input must be single digit numbers")
        self.solveButton.config(state="normal")
        
      start = time()
      solver = SudokuSolver(self.grid)
      try:
        mb.showinfo("Loding","The solving process could take a long time depending on te complexity of the Sudoku grid \nPlease Wait !!!")
        self.grid = solver.solve()
        for row in range(9):
          for column in range(9):
            self.numberStringVar[(row,column)].set(str(self.grid[row,column]))
        mb.showinfo("Finished","The solving process took about "+str(time()-start)+" seconds to finish !!!")
      except:
        mb.showerror("Entry Error","There is an error in your input, please re-enter a coorect grid")
        self.solveButton.config(state="normal")
      
  def launchGame_CameraInput(self):
    """this function launchs a game solver based on camera input and OCR"""
    
    def show_frame():
      """this function updates the image canvas"""
      _, frame = self.cap.read()
      cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
      img = Image.fromarray(cv2image)
      imgtk = ImageTk.PhotoImage(image=img)
      imageLabel.imgtk = imgtk
      imageLabel.configure(image=imgtk)  
      imageLabel.after(10, show_frame)
            
    def snapshot():
      """this function put the image taken from a camera in the image canvas and sets the letters & words entries to the deteceted strings"""
      ret, frame = self.cap.read()
      cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
      img = Image.fromarray(cv2image)
      imgtk = ImageTk.PhotoImage(image=img)
      imageLabel.imgtk = imgtk
      imageLabel.configure(image=imgtk)  
      while(not(ret)):
        ret, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        imageLabel.imgtk = imgtk
        imageLabel.configure(image=imgtk)  
      cv2.imwrite("C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/assets/snapshot.jpg", frame)
      imagepath="C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/assets/snapshot.jpg"
      self.cap.release()
      solveButton.config(state="normal")
      snapshotButton.config(state="disabled")
      recognizeNumbers(imagepath)
      
    def choisirFichier():
      """this function makes the user choose the file of the picture"""
      self.cap.release()
      imagepath = filedialog.askopenfilename()
      try:
        image = Image.open(imagepath)
        image = image.resize((IMAGE_CANVAS_WIDTH, IMAGE_CANVAS_HEIGHT), Image.ANTIALIAS) #need to save the resized image
        image = ImageTk.PhotoImage(image=image)
        imageLabel.image = image
        imageLabel.configure(image=image)
      except:
        mb.showerror("File type error", "Oops! Chosen file type is wrong. \nPlease choose an image file")
      recognizeNumbers(imagepath)

    def recognizeNumbers(imagepath):
      """this function recognizes letters and words using the pytesseract OCR library"""
      image = Image.open(imagepath) 
      image = image.filter(ImageFilter.MedianFilter()) #need to be checked
      enhancer = ImageEnhance.Contrast(image)
      image = enhancer.enhance(2)
      image = image.convert('1')
      text = pytesseract.image_to_string(image)
      numbers = extractDataSudoku(text)
      
      for row in range(9):
        for column in range(9):
          self.numberStringVar[(row,column)].set(numbers[row,column])

    ####main program of the camera mode##### 
    self.controller.geometry(SUDOKU_CAMERA_GEOMETRY)
    self.filemenu.entryconfig("New Game Solver", state="disabled")
    for widget in self.winfo_children():
      widget.destroy()

    #Set the numbersEntries Frame
    numbersFrame = tk.Frame(self)
    self.numberEntries = {}
    self.numberStringVar = {}
    for row in range(9):
      for column in range(9):
        self.numberStringVar[(row,column)] = tk.StringVar()
        self.numberEntries[(row,column)] = tk.Entry(numbersFrame, width=2, textvariable=self.numberStringVar[(row,column)], font=('Helvetica',20)) #change width and height and background color to sitinguish between blocks
        if(row%3 == 2):
          pady=(3,20)
        else:
          pady=(3,3)
        if(column%3 == 2):
          padx=(3,20)
        else:
          padx=(3,3)
        self.numberEntries[(row,column)].grid(row=row , column=column, padx= padx, pady=pady)

    infoEntriesButton = ttk.Button(numbersFrame, text="?", width=3, command=lambda: mb.showinfo("Entries","Click on the Solve button to submit the Numbers written above.\nIf there is a mistake Please, Change it manually"))
    infoEntriesButton.grid(row=10, column=5, sticky=tk.E)
    self.solveButton = ttk.Button(numbersFrame, text="Solve", state="disabled", width=10, command=lambda: self.solve())
    self.solveButton.grid(row=10, column = 6,  columnspan=3, sticky=tk.W)

    #Set the image with its correspondant buttons frame 
    imageFrame = tk.Frame(self)
    imageLabel = tk.Label(imageFrame, bg="white", height=IMAGE_CANVAS_HEIGHT, width=IMAGE_CANVAS_WIDTH)
    imageLabel.grid(row=0, column=0, columnspan=6, padx=DIST_CANVAS_LETTERS, pady=3)
    infoCameraButton = ttk.Button(imageFrame, text="?", width=3, command=lambda: mb.showinfo("Snapshot","Click on the snapshot button to take a snapshot of the Sudoku. \nOr\nClick on the choose file button to import an image file\nof the Sudoku grid"))
    infoCameraButton.grid(row=1, column=2, sticky=tk.E)
    snapshotButton = ttk.Button(imageFrame, state="normal",width = 10,text="Snapshot", command=lambda: snapshot())
    snapshotButton.grid(row=1, column=3, sticky=tk.W+tk.E)
    choisirButton = ttk.Button(imageFrame, state="normal",width=13, text="Choose file", command=lambda: choisirFichier())
    choisirButton.grid(row=1, column=4, sticky=tk.W)

    #griding two frames in the main frame 
    imageFrame.grid(row=0, column=0, sticky=tk.W +tk.N)
    numbersFrame.grid(row=0, column=1, pady=(50,0),  sticky=tk.W+tk.N)

    #camera stream
    try:
      self.cap = cv2.VideoCapture(0)
      self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_CANVAS_WIDTH)
      self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_CANVAS_HEIGHT)
      show_frame()
    except:
      mb.showerror("Camera Mode", "Oops! Camera not detected. \nPlease change mode to Manual input")


    
  def launchGame_ManualInput(self):
    """this function launchs a game solver based on manual input"""

    ####main program of the manual mode#####
    self.controller.geometry(SUDOKU_MANUAL_GEOMETRY)
    self.filemenu.entryconfig("New Game Solver", state="disabled")
    for widget in self.winfo_children():
      widget.destroy()

    #Set the numbersEntries Frame
    numbersFrame = tk.Frame(self)
    self.numberEntries = {}
    self.numberStringVar = {}
    for row in range(9):
      for column in range(9):
        self.numberStringVar[(row,column)] = tk.StringVar()
        self.numberEntries[(row,column)] = tk.Entry(numbersFrame, width=2, textvariable=self.numberStringVar[(row,column)], font=('Helvetica',20)) #change width and height and background color to sitinguish between blocks
        if(row%3 == 2):
          pady=(3,20)
        else:
          pady=(3,3)
        if(column%3 == 2):
          padx=(3,20)
        else:
          padx=(3,3)
        self.numberEntries[(row,column)].grid(row=row , column=column, padx= padx, pady=pady)
        
    infoEntriesButton = ttk.Button(numbersFrame, text="?", width=3, command=lambda: mb.showinfo("Entries","Please fill the digits of the Sudocku grid.\n\nOnce finished click on the solve button."))
    infoEntriesButton.grid(row=10, column=5, sticky=tk.E)
    self.solveButton = ttk.Button(numbersFrame, text="Solve", state="disabled", width=10, command=lambda: self.solve())
    self.solveButton.grid(row=10, column = 6, columnspan=3, sticky=tk.W)
    
    #griding the main frame 
    numbersFrame.grid(row=0, column=0, padx=(20,0), pady=(20,0), sticky=tk.W+tk.N)
