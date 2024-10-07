"""
This object class represents the cells of the sudoku board.
It knows its position, content and potential content.
"""


class Cell:

    def __init__(self, cell_number: int):
        self.possibilty = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.number = 0
        self.is_set = False
        self.cell_number = cell_number
        self.row = cell_number // 9
        self.collum = cell_number % 9
        self.square = (self.row // 3) * 3 + (self.collum // 3)

    # This function removes a number from the list of potentail Numbers.
    # and it checks  if there is only a single number left.

    def remove(self, number):
        if not self.is_set:
            try:
                self.possibilty.remove(number)
                if len(self.possibilty) == 1:
                    return [self.cell_number, self.possibilty[0]]
            except:
                pass
            return []

    # This function sets the content of the cell.

    def set_number(self, number: int):
        self.number = number
        self.possibilty = []
        self.is_set = True


"""
This class represents a group of cells which musst contatin all 9 numbers exactly once.
It knows which cells it conatins and what numbers are not jet set in the group.
"""


class Group:
    def __init__(self):
        self.unused_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.members = []

    def remove(self, number: int):
        try:
            self.unused_numbers.remove(number)
        except:
            pass

    # This function removes a number from the possibity pool of all it members.
    # And it gets informet when one of its members has only one possibilty left

    def member_remove(self, number: int):
        singelton_list = []
        for x in self.members:
            singelton_list.append(x.remove(number))
        return singelton_list

    # This function searches it members, for all those members where the input number is still possible.
    # If it finds more than two it holds.
    # If it finds only one it  returns the cell number and the searched number.

    def member_search(self, number: int):
        found_candidate = False
        candidate = []
        for member in self.members:
            if not member.is_set:
                if not found_candidate and member.possibilty.count(number) == 1:
                    found_candidate = True
                    candidate = [member.cell_number, number]
                elif found_candidate and member.possibilty.count(number) == 1:
                    return []
        return candidate


class Row(Group):
    pass


class Collum(Group):
    pass


class Square(Group):
    pass


"""
This class represents the sudoku board.
It knows its subgroups (rows, collums, squares) and its cells.
It also remembers if progress was made on the board.
"""


class Sudoku:
    def __init__(self):
        self.open_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.cells = []
        self.progress = False
        self.rows = [Row() for x in range(9)]
        self.collums = [Collum() for x in range(9)]
        self.squares = [Square() for x in range(9)]
        for i in range(81):
            self.cells.append(Cell(i))
            self.rows[self.cells[i].row].members.append(self.cells[i])
            self.collums[self.cells[i].collum].members.append(self.cells[i])
            self.squares[self.cells[i].square].members.append(self.cells[i])

    # This Function tells the subgroups to remove a certain nummber from there members
    def clean(self, cell: Cell, number: int):
        self.rows[cell.row].member_remove(number)
        self.collums[cell.collum].member_remove(number)
        self.squares[cell.square].member_remove(number)

    # This Function tells a cell to set its content to remove its content from all other cells it shares a subgroup with
    def set_cell(self, candidate):
        if candidate:
            self.cells[candidate[0]].set_number(candidate[1])
            self.clean(self.cells[candidate[0]], candidate[1])
            self.progress = True

    # This function gets a list of cells to set and sets them one by one
    def set_cell_list(self, candidate_list):
        for candidate in candidate_list:
            self.set_cell(candidate)

    # This function searches for a cell to be set
    def search(self):
        for number in self.open_numbers:
            for i in range(9):
                self.set_cell(self.rows[i].member_search(number))
                self.set_cell(self.collums[i].member_search(number))
                self.set_cell(self.squares[i].member_search(number))


def sudoku_print(cell_list):
    for i in range(9):
        print(cell_list[0 + i * 9].number, cell_list[1 + i * 9].number, cell_list[2 + i * 9].number, " ",
              cell_list[3 + i * 9].number, cell_list[4 + i * 9].number, cell_list[5 + i * 9].number, " ",
              cell_list[6 + i * 9].number, cell_list[7 + i * 9].number, cell_list[8 + i * 9].number)
        if i % 3 == 2:
            print()
    print("___________________________________")


def init_sudoku(sudoku: Sudoku):
    input_cell_list = list(input("enter the sudoku as a string"))
    clean_input(input_cell_list)
    for i in range(81):
        if input_cell_list[i] != 0:
            sudoku.set_cell([i, input_cell_list[i]])


def clean_input(input_list):
    if not input_list:
        exit("no sudoku provided")
    if not len(input_list) == 81:
        exit("input has not the correct length")
    for i in range(len(input_list)):
        if input_list[i] in "123456789":
            input_list[i] = int(input_list[i])
        else:
            input_list[i] = 0


def search(sudoku: Sudoku):
    while sudoku.progress:
        sudoku.progress = False
        sudoku.search()
    sudoku_print(sudoku.cells)


if __name__ == '__main__':
    sudoku_1 = Sudoku()
    while True:
        init_sudoku(sudoku_1)
        sudoku_print(sudoku_1.cells)
        search(sudoku_1)

"""
[2,1,0, 4,0,0, 0,3,6,
 8,0,0, 0,0,0, 0,0,5,
 0,0,5, 3,0,9, 8,0,0,

 6,0,4, 9,0,7, 1,0,0,
 0,0,0, 0,3,0, 0,0,0,
 0,0,7, 5,0,4, 6,0,2,

 0,0,6, 2,0,3, 5,0,0,
 5,0,0, 0,0,0, 0,0,9,
 9,3,0, 0,0,5, 0,2,7]
 
210400036800000005005309800604907100000030000007504602006203500500000009930005027

"""
"""
[0,8,0, 0,5,7, 0,0,1,
 0,1,0, 3,0,0, 5,0,7,
 0,6,5, 9,0,0, 0,0,4,
 
 5,0,0, 0,3,0, 9,2,0,
 1,0,6, 0,0,2, 4,0,0,
 3,0,0, 4,6,0, 0,7,0,
 
 0,0,0, 0,0,3, 2,6,8,
 6,3,2, 0,9,0, 0,0,0,
 0,0,4, 6,0,1, 0,5,0
"""
