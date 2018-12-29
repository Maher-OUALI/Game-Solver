import numpy as np

#all possible directions to find a word
directions = {"S":"South","N":"North","W":"West","E":"East","NE":"North-East","NW":"North-West","SE":"South-East","SW":"South-West"}

class WSPSolver():
    def __init__(self,lettersMatrix):
        self.letters = lettersMatrix #matrix containing all letters
        self.row,self.column=lettersMatrix.shape
        
        self.letters_coord = {chr(i):set({}) for i in range(ord('A'), ord('Z')+1)}
        self.create_letters_coord()#raise exception if bad construction

    def create_letters_coord(self):
        for i in range(self.row):
            for j in range(self.column):
                self.letters_coord[self.letters[i,j]]=self.letters_coord[self.letters[i,j]].union({(i,j)})

    def findWord(self, word):
        wordfound = False
        for direction in list(directions.keys()):
            if self.check_direction(direction,word):
                wordfound = True
                break
        
        if(wordfound):
            return(self.position,self.direction)
        else:
            return(None)
        
    def check_direction(self, direction, word):
        check_direction_last_result = {}
        var_ligne = int(direction == "N")+int(direction == "NE")+int(direction == "NW")-(int(direction == "S")+int(direction == "SW")+int(direction == "SE"))
        var_colonne = int(direction == "W")+int(direction == "SW")+int(direction == "NW")-(int(direction == "E")+int(direction == "NE")+int(direction == "SE"))
        check_direction_last_result = self.letters_coord[word.upper()[0]]
        k=1
        for i in word.upper()[1::]:
            temp_set = {(list(self.letters_coord[i])[j][0]+k*var_ligne,list(self.letters_coord[i])[j][1]+k*var_colonne) for j in range(len(self.letters_coord[i]))}
            check_direction_last_result = check_direction_last_result & temp_set
            k+=1
        if(len(check_direction_last_result)!= 0):
            self.direction=directions[direction]
            self.position=check_direction_last_result.pop()
            return(True)
        else:
            return(False)


####Test Example######
##L=np.array([['W', 'K', 'D', 'R', 'E', 'K', 'C', 'E', 'P', 'D', 'O', 'O', 'W', 'H'],
## ['O', 'W', 'N', 'R', 'S', 'W', 'A', 'N', 'N', 'F', 'O', 'J', 'A', 'Y'],
## ['R', 'A', 'O', 'U', 'I', 'G', 'M', 'I', 'N', 'G', 'I', 'V', 'M', 'T'],
## ['C', 'H', 'E', 'R', 'L', 'B', 'T', 'B', 'N', 'O', 'U', 'N', 'U', 'I'],
## ['P', 'T', 'G', 'E', 'R', 'R', 'K', 'I', 'U', 'L', 'C', 'R', 'C', 'M'],
## ['E', 'E', 'I', 'O', 'A', 'A', 'M', 'C', 'T', 'D', 'K', 'L' ,'O', 'H'],
## ['L', 'E', 'P', 'M' ,'S', 'A', 'P', 'U', 'A', 'E', 'G', 'C', 'A', 'U'],
## ['I', 'K' ,'O', 'W', 'L', 'T', 'R', 'S', 'Y', 'L', 'K', 'I', 'M', 'F'],
## ['C' ,'A', 'L', 'F', 'H', 'E', 'R', 'O', 'N', 'I', 'B', 'E', 'E', 'O'],
## ['A', 'R', 'L', 'C', 'A', 'R', 'D', 'I', 'N', 'A', 'T', 'V', 'D', 'N'],
## ['N', 'A', 'U', 'K', 'C', 'U', 'D', 'G' ,'C' ,'E' ,'S', 'O', 'O', 'G'],
## ['A', 'P', 'G', 'R', 'R' ,'O' ,'B', 'I', 'N', 'H', 'D', 'D', 'G', 'B'],
## ['R', 'M' ,'A', 'G', 'P', 'I', 'E', 'N', 'E', 'K', 'C', 'I', 'H', 'C'],
## ['Y', 'N', 'E', 'W', 'R', 'E', 'N', 'T' ,'O', 'R', 'R', 'A', 'P', 'I'],
## ['E', 'R', 'S', 'D', 'D', 'R', 'A', 'V', 'E', 'N', 'A' ,'N' ,'Y', 'M']])
##
##words =['BLACKBIRD','EAGLE','MARTIN','ROBIN']
##solver = WSPSolver(L)
##for w in words:
##    print(solver.findWord(w),'\n')
                    

