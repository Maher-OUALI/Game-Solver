import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as mb
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import pytesseract
from functools import partial
from numpy import empty
from time import sleep
from random import choice
import sys
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/lib')#put here the directory of the lib folder
from tools import *
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/assets')#put here the directory of the assets folder
from Constants import *
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/solvers')#put here the directory of the solvers folder
from WordSearchPuzzleSolver import WSPSolver

# and need to delete the frame after we exit and release capture when we click on exit or return 

directionStep = {"South":(1,0),"North":(-1,0),"West":(0,-1),"East":(0,1),"North-East":(-1,1),"North-West":(-1,-1),"South-East":(1,1),"South-West":(1,-1)}

class WordsearchPuzzle(tk.Frame):
  def __init__(self,parent,controller):
    tk.Frame.__init__(self,parent) #the parent is the application frame that is on this current frame (in this case it's GameSolver)
    self.controller = controller
    self.parent = parent
    label = tk.Label(self, text="Wordsearch Puzzle Solver", font=LARGE_FONT)
    label.pack(pady=10, padx=10)
    homeButton = ttk.Button(self, text="What to do !", command=lambda: mb.showinfo("Game Solver","Start by choosing New Game !"))
    homeButton.pack()

  def getMenu(self,parent):
    """this function creates the menu for the Wordsearch Puzzle Frame"""
    self.menu = tk.Menu(parent)
    self.filemenu = tk.Menu(self.menu, tearoff=0)
    new_gameOption = tk.Menu(self.filemenu, tearoff=0)
    new_gameOption.add_command(label="Camera Input", command=lambda: self.chooseParam("camera"))
    new_gameOption.add_command(label="Manual Input", command=lambda: self.chooseParam("manual"))
    self.filemenu.add_cascade(label = "New Game Solver", menu=new_gameOption)
    self.filemenu.add_separator()
    self.filemenu.add_command(label="Return", command=lambda: self.controller.show_frame("StartPage","300x"+str(210*len(self.controller.games)+100)))
    self.filemenu.add_command(label="Exit", command = parent.destroy)
    self.menu.add_cascade(label="File", menu=self.filemenu)
    self.helpmenu = tk.Menu(self.menu, tearoff=0)
    message = "This is a Wordsearch Puzzle Solver, you add a new game either by typing the numbers or by importing an image"
    self.helpmenu.add_command(label="About", command = lambda: mb.showinfo("About!",message))
    self.menu.add_cascade(label="Help", menu=self.helpmenu)
    return(self.menu)

  def chooseParam(self,mode):
      """this function takes param given by the user and then launches the appropriate mode"""
      try:
        paramConfiguration = ParamWSP(self.controller)
        self.nbRows,self.nbColumns,self.nbWords = paramConfiguration.result
        if(mode == "camera"):
          self.launchGame_CameraInput()
        elif(mode == "manual"):
          self.launchGame_ManualInput()
      except:
        pass

  def solve(self,text_display=None):
      """this function solves the wordseaerch puzzle given and returns the correspondant cell and direction of each word"""
      #use showinfo to indicate the starting cell and direction 
      self.solveButton.config(state="disabled")
      self.lettersMatrix=empty((self.nbRows,self.nbColumns),dtype=str)
      self.words=list()
      for row in range(self.nbRows):
        for column in range(self.nbColumns):
          self.lettersMatrix[row,column]=str(self.letterStringVar[(row,column)].get()).upper()
      for word in range(self.nbWords):
        self.words.append(str(self.wordStringVar[word].get()).upper())

      solver = WSPSolver(self.lettersMatrix)
      for word in self.words:
        try:
          pos,direction = solver.findWord(word)
          color = choice(COLORS)
          self.wordEntries[self.words.index(word)].config(bg=color)
          for i in range(len(word)):
            self.letterEntries[(pos[0]+i*directionStep[direction][0],pos[1]+i*directionStep[direction][1])].config(bg=color)
          sleep(0.2) #sleep for 200 ms
          if(text_display == None):
            mb.showinfo("Solution","To find word "+word+" go to cell ("+str(pos[0]+1)+","+str(pos[1]+1)+") and take the "+direction+" direction.")
          else:
            text_display.insert(tk.END,"To find word "+word+" go to cell ("+str(pos[0]+1)+","+str(pos[1]+1)+") and take the "+direction+" direction. \n")
        except:
          mb.showerror("Entry Error","There is an error in your input, please re-enter letters & words")
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
      self.solveButton.config(state="normal")
      snapshotButton.config(state="disabled")
      choisirButton.config(state="disabled")
      recognizeLettersWords(imagepath)
      
    def chooseFile():
      """this function makes the user choose the file of the picture"""
      self.cap.release()
      imagepath = filedialog.askopenfilename()
      try:
        image = Image.open(imagepath)
        image = image.resize((IMAGE_CANVAS_WIDTH, IMAGE_CANVAS_HEIGHT), Image.ANTIALIAS) #need to save the resized image
        image = ImageTk.PhotoImage(image=image)
        imageLabel.image = image
        imageLabel.configure(image=image)
        self.solveButton.config(state="normal")
        snapshotButton.config(state="disabled")
        choisirButton.config(state="disabled")
      except:
        mb.showerror("File type error", "Oops! Chosen file type is wrong. \nPlease choose an image file")
        snapshotButton.config(state="disabled")
        choisirButton.config(state="normal")
      recognizeLettersWords(imagepath)
    
    def recognizeLettersWords(imagepath): #need to be modified with the use of image processing
      """this function recognizes letters and words using the pytesseract OCR library"""
      image = Image.open(imagepath) 
      text = pytesseract.image_to_string(image)
      print(text) ####
      letters,words = extractDataWSP(text,self.nbRows,self.nbColumns,self.nbWords)
      print(letters,words) #####
      try:
        for row in range(self.nbRows):
          for column in range(self.nbColumns):
            self.letterStringVar[(row,column)].set(letters[row][column])
      except:
         pass
      try:
        for word in range(self.nbWords):
          self.wordStringVar[word].set(words[word])
      except:
         pass

        
    ####main program of the camera mode#####
    self.controller.geometry(WSP_CAMERA_GEOMETRY)
    self.filemenu.entryconfig("New Game Solver", state="disabled")
    for widget in self.winfo_children():
      widget.destroy()

    #Set the image with its correspondant buttons frame 
    imageFrame = tk.Frame(self)
    imageLabel = tk.Label(imageFrame, bg="white", height=IMAGE_CANVAS_HEIGHT, width=IMAGE_CANVAS_WIDTH)
    imageLabel.grid(row=0, column=0, columnspan=6, padx=DIST_CANVAS_LETTERS, pady=3)
    infoCameraButton = ttk.Button(imageFrame, text="?", width=3, command=lambda: mb.showinfo("Snapshot","Click on the snapshot button to take a snapshot of the wordsearch puzzle. \nOr\nClick on the choose file button to import an image file\nof the wordsearch puzzle"))
    infoCameraButton.grid(row=1, column=2, sticky=tk.E)
    snapshotButton = ttk.Button(imageFrame, state="normal",width = 10,text="Snapshot", command=lambda: snapshot())
    snapshotButton.grid(row=1, column=3, sticky=tk.W+tk.E)
    choisirButton = ttk.Button(imageFrame, state="normal",width=13, text="Choose file", command=lambda: chooseFile())
    choisirButton.grid(row=1, column=4, sticky=tk.W)
    
    #Set the letterEntries Frame
    lettersFrame = tk.Frame(self)
    self.letterEntries = {}
    self.letterStringVar = {}
    for row in range(self.nbRows):
      for column in range(self.nbColumns):
        self.letterStringVar[(row,column)] = tk.StringVar()
        self.letterEntries[(row,column)] = tk.Entry(lettersFrame, width=1, textvariable=self.letterStringVar[(row,column)], font=('Helvetica',12))
        self.letterEntries[(row,column)].grid(row=row , column=column, padx=MIN_DIST_LET_LET_X[self.nbColumns], pady=MIN_DIST_LET_LET_Y[self.nbRows]) #580 total length 

    #Set the text view of the solving process Frame
    textDisplayFrame = tk.Frame(self)
    scroll = tk.Scrollbar(textDisplayFrame)
    scroll.pack(side="right", fill=tk.Y)
    textDisplay = tk.Text(textDisplayFrame, wrap=tk.CHAR, fg="blue", yscrollcommand=scroll.set, width=85, height=8)
    textDisplay.pack(side="left", padx=10, pady=10)
    scroll.config(command=textDisplay.yview)
    
    #Set the wordEntries  and verification button Frame
    wordsFrame = tk.Frame(self)
    self.wordEntries = {}
    self.wordStringVar = {}
    for word in range(self.nbWords):
      self.wordStringVar[word]= tk.StringVar()
      self.wordEntries[word]= tk.Entry(wordsFrame, textvariable=self.wordStringVar[word], width=10, fg="blue")
      self.wordEntries[word].grid(row=(word//8), column=(word%8), padx=3, pady=3)
    infoEntriesButton = ttk.Button(wordsFrame, text="?", width=3, command=lambda: mb.showinfo("Entries","Click on the Solve button to submit the Letters & Words written above.\nIf there is a mistake Please, Change it manually"))
    infoEntriesButton.grid(row=6, column=5, sticky=tk.E)
    self.solveButton = ttk.Button(wordsFrame, text="Solve", state="disabled", width=10, command=lambda: self.solve(textDisplay))
    self.solveButton.grid(row=6, column = 6, sticky=tk.W)
   
    #griding four frames in the main frame 
    imageFrame.grid(row=0, column=0, sticky=tk.W +tk.N)
    lettersFrame.grid(row=0, column=1, sticky=tk.W+tk.N)
    textDisplayFrame.grid(row=1, column=0, sticky=tk.W+tk.N)
    wordsFrame.grid(row=1, column=1, sticky=tk.W+tk.N, padx=10)

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
    self.controller.geometry(WSP_MANUAL_GEOMETRY)
    self.filemenu.entryconfig("New Game Solver", state="disabled")
    for widget in self.winfo_children():
      widget.destroy()

    #Set the letterEntries Frame
    lettersFrame = tk.Frame(self)
    self.letterEntries = {}
    self.letterStringVar = {}
    for row in range(self.nbRows):
      for column in range(self.nbColumns):
        self.letterStringVar[(row,column)] = tk.StringVar()
        self.letterEntries[(row,column)] = tk.Entry(lettersFrame, width=1, textvariable=self.letterStringVar[(row,column)], font=('Helvetica',12))
        self.letterEntries[(row,column)].grid(row=row , column=column, padx=MIN_DIST_LET_LET_X[self.nbColumns], pady=MIN_DIST_LET_LET_Y[self.nbRows]) #580 total length 
    
    #Set the wordEntries  and verification button Frame
    wordsFrame = tk.Frame(self)
    self.wordEntries = {}
    self.wordStringVar = {}
    for word in range(self.nbWords):
      self.wordStringVar[word]= tk.StringVar()
      self.wordEntries[word]= tk.Entry(wordsFrame, textvariable=self.wordStringVar[word], width=10, fg="blue")
      self.wordEntries[word].grid(row=(word//8), column=(word%8), padx=3, pady=3)
    infoEntriesButton = ttk.Button(wordsFrame, text="?", width=3, command=lambda: mb.showinfo("Entries","Please fill the letters and words of the wordsearch Puzzle.\n\nOnce finished click on the solve button."))
    infoEntriesButton.grid(row=6, column=5, sticky=tk.E)
    self.solveButton = ttk.Button(wordsFrame, text="Solve", state="normal", width=10, command=lambda: self.solve())
    self.solveButton.grid(row=6, column = 6, sticky=tk.W)

    #griding four frames in the main frame 
    lettersFrame.grid(row=0, column=0, sticky=tk.W+tk.N, pady=10)
    wordsFrame.grid(row=1, column=0, sticky=tk.W+tk.N, padx=10)


  


