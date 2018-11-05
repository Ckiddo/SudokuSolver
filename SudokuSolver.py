import copy


def sudoku_cells():
    '''
    this function will return:
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), ..., (8, 5), (8, 6), (8, 7), (8, 8)]
    '''
    lis = []
    for i in range(9):
        for j in range(9):
            lis.append((i,j))
    return lis
    pass

def sudoku_arcs():
    '''
    this function will return:
    set([((0, 0), (0, 0)),((0, 0), (0, 1)),...])
    '''
    ans = set()
    for i in range(9):
            for j in range(9):
                for k in range(9):
                    ans.add(((i,k),(i,j)))
                    ans.add(((k,j),(i,j)))
                mdx = (i)//3 * 3 + 1
                mdy = (j)//3 * 3 + 1
                for k in [-1,0,1]:
                    for l in [-1,0,1]:
                        ans.add(((mdx+k,mdy+l),(i,j)))
    return ans

    pass

def read_board(path):
    '''
    path: the file path
    this function will return a list like:
    [
    [set([1,2,3,4,5,6,7,8,9]),...,],
    [set([1]),...],
    ...
    [set([9]),...]
    ]
    '''
    fil = open(path,"r")
    text = fil.read()
    fil.close()
    count = 0
    cellBoard = []
    alist = []
    for letter in text:      
        if letter == '*':
            count = count +  1
            alist.append(set([1,2,3,4,5,6,7,8,9]))
        elif letter in "123456789":
            count = count +1
            alist.append(set([int(letter)]))
        if count >= 9:
            cellBoard.append(alist)
            count = 0
            alist = []
    return cellBoard

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    my_cell = []
    def __init__(self, board):
        '''
        deep copy the board to my_cell,
        my_cell record all the imformation about this sudoku
        '''
        self.my_cell = copy.deepcopy(board)
        pass

    def get_values(self, cell):
        '''
        get values by cell
        '''
        return self.my_cell[cell[0]][cell[1]]
        pass

    def remove_inconsistent_values(self, cell1, cell2):
        '''
            self.get_values(cell2) has only 1 element, means this cell is decided.
            self.get_values(cell1) has at least 2 elements, means can be moved.
        '''
        if (len(self.get_values(cell2)) == 1) and (len(self.get_values(cell1)) > 1):
            re = False
            if self.get_values(cell2).issubset(self.get_values(cell1)):
                re = True
            # if len(self.get_values(cell1) - self.get_values(cell2)) == 0:
            #     print "hi:" ,cell1 ,cell2
            self.my_cell[cell1[0]][cell1[1]] = self.get_values(cell1) - self.get_values(cell2)

            return re
        else:
            return False
        pass

    def infer_ac3(self):
        '''
        use the function remove_inconsistent_values constantly
        '''
        successChanged = False
        while True:
            successChanged = False
            for tupe in self.ARCS:
                if self.remove_inconsistent_values(tupe[0],tupe[1]):
                    successChanged = True
            if successChanged == False:
                break

        pass

    def infer_improved(self):
        '''
        if len(self.get_values((i,j))) > 1:
            and only one number appear in a row or column or 9 cells
            this number can be safely placed
        '''
        self.infer_ac3()
        for ck in range(100):
            successChanged = False
            count = 0
            for i in range(9):
                for j in range(9):
                    if len(self.get_values((i,j))) == 1:
                        continue
                    for number in self.get_values((i,j)):
                        lineshowen = False
                        listshowen = False
                        bigCellshowen = False
                        for k in range(9):
                            if number in self.get_values((i,k)) and k != j:
                                lineshowen = True
                            if number in self.get_values((k,j)) and i != k:
                                listshowen = True
                        mdx = (i)//3 * 3 + 1
                        mdy = (j)//3 * 3 + 1
                        for k in [-1,0,1]:
                            for l in [-1,0,1]:
                                if number in self.get_values((mdx + k,mdy + l)) and (i != mdx + k or j != mdy + l):
                                    bigCellshowen = True
                        if (lineshowen == False or listshowen == False or bigCellshowen == False) and (not(lineshowen == False and listshowen == False and bigCellshowen == False)):
                            self.my_cell[i][j] = set([number])
                            self.infer_ac3()
                            successChanged = True
            if successChanged == False:
                break

    def infer_with_guessing(self):
        '''
        using search function
        '''
        self.my_cell = self.search(self.my_cell)

    def search(self,cellmap):
        '''
            use DFS, depth first search algorithm.
        '''
        searchList = []
        searchList.append(cellmap)
        while len(searchList) > 0:
            newcellmap = searchList.pop()
            newSudoku = Sudoku(newcellmap)
            newSudoku.infer_improved()
            if self.solved(newSudoku.my_cell):
                return newSudoku.my_cell
            else:
                multiChosen = self.firstmultiChosen(newSudoku.my_cell)
                if multiChosen == None:
                    continue
                else:
                    numbers = newSudoku.get_values(multiChosen)
                    for number in numbers:
                        # print number
                        newnewSudoku = Sudoku(newSudoku.my_cell)
                        newnewSudoku.my_cell[multiChosen[0]][multiChosen[1]] = set([number])
                        searchList.append(newnewSudoku.my_cell)

    def showCells(self,cellmap):
        '''
        print sudoku elegantly
        '''
        for i in range(9):
            for j in range(9):
                if len(cellmap[i][j]) > 1:
                    print cellmap[i][j],
                else:
                    for s in cellmap[i][j]:
                        print s,
            print ""


    def firstmultiChosen(self,cellmap):
        '''
        return the coordinate of a cell which has lots of number can be placed
        '''
        for i in range(9):
            for j in range(9):
                if len(cellmap[i][j]) > 1:
                    return (i,j)
        return None

    def solved(self,cellmap):
        '''
        if this sudoku finished or solved, return true
        '''
        for tupe in self.ARCS:
            cell1 = cellmap[tupe[0][0]][tupe[0][1]]
            cell2 = cellmap[tupe[1][0]][tupe[1][1]]
            # cell1 = self.get_values((tupe[0]))
            # cell2 = self.get_values((tupe[1]))
            if tupe[0] == tupe[1]:
                continue
            if len(cell1) != 1 or len(cell2) != 1 :
                # print "wrong:in",cell1,cell2,(tupe[0]),(tupe[1])
                return False
            elif cell1 == cell2:
                # print "wrong:in",cell1,cell2,(tupe[0]),(tupe[1])
                return False
        return True


if __name__ == '__main__':
    fileName = "hard.txt"
    board = read_board(fileName)
    sudoku = Sudoku(board)
    sudoku.infer_with_guessing()
    print "ans:"
    sudoku.showCells(sudoku.my_cell)


