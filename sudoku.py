# sudoku solver
import copy
import time

import pygame


class Sudoku:
    def __init__(self, board):
        self.board = board
        self.original_board = copy.deepcopy(board)

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

    def visual_solve(self, cells):
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
            cells[row * 9 + col].change_key(move)
            pygame.display.update()
            pygame.time.delay(20)
            # time.sleep(0.05)
            # checks if next square has legal moves
            if (self.visual_solve(cells)): return True
            
            # else back track
            self.board[row][col] = 0
            cells[row * 9 + col].change_key(0)
            pygame.display.update()


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






if __name__ == "__main__":
    board =[[0 for x in range(9)]for y in range(9)]

    board =[[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    sudoku = Sudoku(board)
    print(sudoku.solve())
    print(sudoku.original_board)
