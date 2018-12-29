import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from tkinter import ttk
from PIL import Image,ImageTk
import cv2
import sys
sys.path.insert(0,'C:/Users/Asus/Desktop/GitHub Projects/projets à terminer/Game Solver (à terminer)/assets')#put here the directory of the assets folder
from Constants import *

class ParamWSP(sd.Dialog):

    def body(self, master):

        tk.Label(master, text="Number of Rows").grid(row=0)
        tk.Label(master, text="Number of Columns").grid(row=1)
        tk.Label(master, text="Number of Words").grid(row=2)

        self.row = tk.Entry(master)
        self.column = tk.Entry(master)
        self.words = tk.Entry(master)

        self.row.grid(row=0, column=1)
        self.column.grid(row=1, column=1)
        self.words.grid(row=2, column=1)
        return self.row # initial focus

    def apply(self):
        rows = self.row.get()
        columns = self.column.get()
        words = self.words.get()
        try:
            if(int(rows)<=20 and int(rows)>=5 and int(columns)<=20 and int(columns)>=5 and int(words)<=40 and int(words)>=1):
                self.result = (int(rows),int(columns),int(words))
            else:
                mb.showwarning("Warning",
                "Parameters must be integer values \nNbr of Rows and nbr of Columns must be between 5 and 20 \nNbr of Words must be less than 40 \nPlease try again!"
            )
        except:
            mb.showwarning("Warning",
                "Parameters must be integer values \nNbr of Rows and nbr of Columns must be between 5 and 20 \nNbr of Words must be less than 40 \nPlease try again!"
            )

def extractDataWSP(text,rows,columns,words):
    try:
        text = text.split('\n')
        elements = list()
        for element in text:
            elements += element.split(' ')
        matrixLetters = list()
        listWords = list()
        listLetters = list()
        element,row,word,column = 0,0,0,0
        while(row<rows or word<words ):    
            if(len(elements[element]) == 1 and elements[element].isalpha()):
                if(row<rows):
                    listLetters.append(elements[element].upper())
                    column = (column+1)%columns
                    if(column == 0):
                        matrixLetters.append(listLetters)
                        listLetters = list()
                        row += 1
            elif(len(elements[element])>1 and elements[element].isalpha()):
                if(word<words):
                    listWords.append(elements[element].upper())
                    word+=1    
            element += 1
        return(matrixLetters,listWords)
    except:
        mb.showwarning("Warning",
                "Character didn't go well.\nRe-capture a better quality image.\nOr\nComplete missing input manually"
            )
        matrixLetters.append(listLetters)
        return(matrixLetters,listWords)

def extractDataSudoku(text):
    try:
        text = text.split('\n')
        elements = list()
        for element in text:
            elements += element.split(' ')
        matrixNumbers = list()
        element = 0
        listNumbers = list()
        while(row<9 or word<9 ):    
            if(len(elements[element]) == 1 and elements[element].isnumeric()):
                if(row<9):
                    listLetters.append(elements[element])
                    column = (column+1)%9
                    if(column == 0):
                        matrixNumbers.append(listNumbers)
                        listNumbers = list()
                        row += 1
            element += 1
        return(matrixNumbers)
    except:
        mb.showwarning("Warning",
                "Character didn't go well.\nRe-capture a better quality image.\nOr\nComplete missing input manually"
            )
        matrixLetters.append(listNumbers)
        return(matrixNumbers)
##test =" A  G j h  f \n r T  E  g   \n ERFTg  HgtF HHGf \n gyTI "
##print(extractData(test,2,5,4))
            
            

