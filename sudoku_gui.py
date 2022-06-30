import tkinter as tk
from tkinter import *

from sudoku import solve

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

# dictionary to store location:value
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
            e = Entry(root, width=5, bg=bgcolor, disabledbackground=bgcolor, justify="center", validate="key", validatecommand=(reg,"%P"))
            # adds grid + triggers validate_num whenever keystroke changes
            e.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=1, ipadx=10, ipady=16)
            squares[(row+i+1, column+j+1)] = e
    

def create9x9grid():
    # creates 9x9 grid with 9 3x3 grids
    color = "#c3ecfa"
    for row in range(1, 10, 3):
        for col in range(0, 9, 3):
            create3x3grid(row, col, color)
            # creates alternating color pattern
            if color == "#c3ecfa": 
                color = "#a9e7fc"
            else: 
                color = "#c3ecfa"

def clear_values():
    # configure changes a value of said object via dictionary
    err_label.configure(text="")
    solved_label.configure(text="")
    
    for row in range(2,11):
        for col in range(1, 10):
            square = squares[(row, col)]
            square.delete(0, "end")

def get_values():
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
    update_values(board)

def solve_board(board):
    return solve(board)

def update_values(board):
    sol = solve(board)
    if sol != "no": 
        for row in range(2,11):
            for col in range(1,10):
                squares[(row,col)].delete(0,sol[row-2][col-1])
                squares[(row, col)].insert(0, sol[row-2][col-1])
        solved_label.configure(text="Sudoku Solved!")
    else: 
        err_label.configure(text="No solution exists for this sudoku.")


def fill_board(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0: continue
            square = squares[(i+2, j+1)]
            square.insert(0, board[i][j])
            square.configure(state='disabled')
board =[[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]

solution_board = solve_board(board)

def fill(board):
    print(solve(board))
solve_btn = Button(root, command=get_values, text="Solve", width=10)
solve_btn.grid(row=20, column=1, columnspan=5, pady=20)

clear_btn = Button(root, command=clear_values, text="Clear", width=10)
clear_btn.grid(row=20, column=5, columnspan=5, pady=20)

create9x9grid()

fill_board(board)
root.mainloop()
