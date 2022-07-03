import copy
import time
import tkinter as tk
from tkinter import *

# from sudoku import Sudoku


class Sudoku:
    def __init__(self, board):
        self.board = board

    def solve(self):
        """
        Outputs the solution if board is solved
        Args:
            board (2d array): sudoku board
        """
        if (self.solve_board()): return self.board
        else: return False



    def solve_board(self):
        """
        Solves the sudoku board through backtracking

        Args:
            board (2d array): sudoku board

        Returns:
            _type_: True = solution found; False = no solution
        """
        if not self.find_empty_space(): return True

        row, col = self.find_empty_space()
        moves = self.gen_moves(row, col)

        # goes through each possible move
        for move in moves:
            # added move to board
            self.board[row][col] = move
            # checks if next square has legal moves
            if (self.solve_board()): return True, self.board
            
            # else back track
            self.board[row][col] = 0

        return False



    def find_empty_space(self):
        """finds empty sudoku space

        Args:
            board (2d array): sudoku board

        Returns:
            _type_: empty board index
        """
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0: return i, j
        return False

    def get_box_list(self, row, col):
        """
        gets the list of integers in the box

        Args:
            board (2d array): sudoku board
            row (int): row index
            col (int): column index

        Returns:
            array: box list
        """
        box_list = []
        box_length = 3

        box_row = row - row % 3
        box_col = col - col % 3

        for i in range(box_length):
            for j in range(box_length):
                box_list.append(self.board[i + box_row][j + box_col])
        
        return box_list
                

    def get_col_list(self, col):
        """
        gets the list of integers in the column

        Args:
            board (2d array): sudoku board
            col (int): column index

        Returns:
            array: column list
        """
        col_list = []
        for i in range(len(self.board)):
            col_list.append(self.board[i][col])
        return col_list


    def gen_moves(self, row, col):
        """
        generates list of possible move of a sudoku square

        Args:
            board (2d array): sudoku board
            row (int): row index
            col (int): column index

        Returns:
            array: list of possible moves
        """
        moves = []
        row_list = self.board[row]
        col_list = self.get_col_list(col)
        box_list = self.get_box_list(row, col)

        # find moves
        for i in range(1, 10):
            if i in row_list or i in col_list or i in box_list:
                continue
            moves.append(i)
        return moves

    def print_solution(self):
        """
        Prints complete sudoku 

        Args:
            board (2d array): sudoku board
        """
        length = len(self.board)
        for i in range(length):
            for j in range(length):
                print(self.board[i][j], end=" | ")
            print()
    
    def vs_solve(self):
        self.visual_solve_board()

    def visual_solve_board(self):
        """
        Solves the sudoku board through backtracking

        Args:
            board (2d array): sudoku board

        Returns:
            _type_: True = solution found; False = no solution
        """
        if not self.find_empty_space(): return True

        row, col = self.find_empty_space()


        moves = self.gen_moves(row, col)

        # thing = copy.deepcopy(self.board)
        # time.sleep(0.01)
        # update(thing)

        # goes through each possible move
        for move in moves:
            # added move to board
            update(move, row, col)
            time.sleep(0.01)
            self.board[row][col] = move

            # checks if next square has legal moves

            if (self.visual_solve_board()): return True
            
            # else back track
            update(0, row, col)
            self.board[row][col] = 0

        return False

# new_board =[[3, 1, 6, 5, 0, 8, 4, 9, 2],
#           [5, 2, 0, 0, 0, 0, 0, 0, 0],
#           [0, 8, 7, 0, 0, 0, 0, 3, 1],
#           [0, 0, 3, 0, 1, 0, 0, 8, 0],
#           [9, 0, 0, 8, 6, 3, 0, 0, 5],
#           [0, 5, 0, 0, 9, 0, 6, 0, 0],
#           [1, 3, 0, 0, 0, 0, 2, 5, 0],
#           [0, 0, 0, 0, 0, 0, 0, 7, 4],
#           [0, 0, 5, 2, 0, 6, 3, 0, 0]]


def update(move, x, y):
    squares[(x + 2 , y + 1)].delete(0, move)
    squares[(x + 2 , y + 1)].insert(0, move)



    # for row in range(2,11):
    #     for col in range(1,10):
    #         squares[(row,col)].delete(0,new_board[row-2][col-1])
    #         squares[(row, col)].insert(0, new_board[row-2][col-1])
    # solved_label.configure(text="Sudoku Solved!")




FILLED = "#b6e9fa"
UNFILLED = "#c3ecfa"

og_board =[[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]

sudoku = Sudoku(og_board)

board = copy.copy(og_board)


root = tk.Tk()

root.title('Sudoku Solver')

# window size
root.geometry("503x590")

# intro label, error label, solved label
# if you don't separate the .grid part, causes Nonetype errors
intro_label = Label(root, text="Click empty squares and enter numbers!")
intro_label.grid(row=0, column=10, columnspan=10)
err_label = Label(root, text="", fg="red")
err_label.grid(row=15, column=1, columnspan=10, pady=5)
solved_label = Label(root, text="", fg="green")
solved_label.grid(row=15, column=1, columnspan=10, pady=5)

# dictionary to store location:value (value is entry object)
squares = {}

# checks if valid number (only allows 1-9)
def validate_num(num):
    out = (num.isdigit() or num == "") and len(num) < 2
    return out

reg = root.register(validate_num)


def create3x3grid(row, column, bgcolor):
    # create a 3x3 grid
    length = 3

    for i in range(length):
        for j in range(length):
            # entry: enter/display a single line of text
            e = Entry(root, width=5, bg=bgcolor, disabledbackground=UNFILLED, justify="center", validate="key", validatecommand=(reg,"%P"))
            # adds grid + triggers validate_num whenever keystroke changes
            e.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=1, ipadx=10, ipady=16)
            # e.place(x=10, y=10, width=1000, height=1000)

            squares[(row+i+1, column+j+1)] = e
    

def create9x9grid():
    # creates 9x9 grid with 9 3x3 grids
    color = FILLED
    for row in range(1, 10, 3):
        for col in range(0, 9, 3):
            create3x3grid(row, col, color)

def clear_board():
    # configure changes a value of said object via dictionary
    err_label.configure(text="")
    solved_label.configure(text="")
    
    for row in range(2,11):
        for col in range(1, 10):
            square = squares[(row, col)]
            square.configure(bg=FILLED, disabledbackground=FILLED)
            square.delete(0, "end")

# gets the current board
def get_board():
    board = []
    err_label.configure(text="")
    solved_label.configure(text="")

    for row in range(2,11):
        rows = []
        for col in range(1, 10):
            val = squares[(row, col)].get()
            if val == "": rows.append(0)
            else: rows.append(int(val))
        board.append(rows)
    update_values()

def solve_sudoku():
    sol = sudoku.solve()
    if sol != True: 
        for row in range(2,11):
            for col in range(1,10):
                squares[(row,col)].delete(0,sol[row-2][col-1])
                squares[(row, col)].insert(0, sol[row-2][col-1])
        solved_label.configure(text="Sudoku Solved!")
    else: 
        err_label.configure(text="No solution exists for this sudoku.")


def visual_solve():
    # shows the backtracking algorithm in action

    # after each move, board is updated
    # after each back track, board is updated
    # continues until True is returned
    sudoku.vs_solve()

def check_board():
    solution = sudoku.solve()
    solved = True
    # light green
    correct = "#c0ffc9"
    # light orange
    wrong = "#ffa289"

    for row in range(2, 11):
        for col in range(1, 10):
            val = squares[(row, col)].get()
            square = squares[(row, col)]

            # correct answer
            if val != "" and solution[row-2][col-1] == int(val): square.configure(bg=correct, disabledbackground=correct)
            else: 
                square.configure(bg=wrong)
                solved = False

    if solved: solved_label.configure(text="Sudoku Solved!")
    else: err_label.configure(text="Incorrect Solution")

def update_values():
    sol = sudoku.solve()
    if sol != "no": 
        for row in range(2,11):
            for col in range(1,10):
                squares[(row, col)].delete(0,sol[row-2][col-1])
                squares[(row, col)].insert(0, sol[row-2][col-1])
        solved_label.configure(text="Sudoku Solved!")
    else: 
        err_label.configure(text="No solution exists for this sudoku.")


def fill_board(board):
    for i in range(2, 11):
        for j in range(1, 10):
            if board[i-2][j-1] == 0: continue
            square = squares[(i, j)]
            square.insert(0, board[i-2][j-1])
            square.configure(state='disabled', disabledbackground=UNFILLED)

def slow_fill():
    for row in range(2,11):
        for col in range(1,10):
            square = squares[(row, col)]
            square.config(text="1")
            # square.delete(0)
            # square.insert(0, row)

def change_text(row, col):
    square = squares[(row, col)]
    square.delete(0)
    square.insert(0, row)




solve_btn = Button(root, command=solve_sudoku, text="Solve", width=10)
solve_btn.grid(row=20, column=1, columnspan=5, pady=20)

vis_btn = Button(root, command=slow_fill, text="Visualize", width=10)
vis_btn.grid(row=20, column=2, columnspan=5, pady=20)

check_btn =Button(root, command=check_board, text="Check", width=10)
check_btn.grid(row=20, column=3, columnspan=5, pady=20)

clear_btn = Button(root, command=clear_board, text="Clear", width=10)
clear_btn.grid(row=20, column=5, columnspan=5, pady=20)

create9x9grid()

fill_board(board)










# sudoku solver



root.mainloop()
