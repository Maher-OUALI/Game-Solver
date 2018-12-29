#program taken from https://stackoverflow.com/questions/1697334/algorithm-for-solving-sudoku using the backpropagation algorithm

class SudokuSolver():
    def __init__(self,grid=None):
        self.grid = grid

    def solve(self,i=0,j=0):
        i,j = self.findNextCellToFill(i, j)
        if i == -1:
                return self.grid
        for e in range(1,10):
                if self.isValid(i,j,e):
                        self.grid[i][j] = e
                        if self.solve(i, j):
                                return self.grid
                        # Undo the current cell for backtracking
                        self.grid[i][j] = 0
                            
    def isValid(self, i, j, e):
        rowOk = all([e != self.grid[i][x] for x in range(9)])
        if rowOk:
            columnOk = all([e != self.grid[x][j] for x in range(9)])
            if columnOk:
                    # finding the top left x,y co-ordinates of the section containing the i,j cell
                    secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
                    for x in range(secTopX, secTopX+3):
                            for y in range(secTopY, secTopY+3):
                                    if self.grid[x][y] == e:
                                            return False
                    return True
        return False
        
    def findNextCellToFill(self, i, j):
        for x in range(i,9):
            for y in range(j,9):
                    if self.grid[x][y] == 0:
                            return x,y
        for x in range(0,9):
            for y in range(0,9):
                    if self.grid[x][y] == 0:
                            return x,y
        return -1,-1

##solver = SudokuSolver( [[5,1,7,6,0,0,0,3,4],[2,8,9,0,0,4,0,0,0],[3,4,6,2,0,5,0,9,0],[6,0,2,0,0,0,0,1,0],[0,3,8,0,0,6,0,4,7],[0,0,0,0,0,0,0,0,0],[0,9,0,0,0,0,0,7,8],[7,0,3,4,0,0,5,6,0],[0,0,0,0,0,0,0,0,0]])
##print(solver.solve())

