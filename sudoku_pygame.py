import copy
import math

import pygame

from sudoku import Sudoku

# make square
# make a 3x3 square
# fill into 9x9 square

# initialize modules
pygame.init()

class Board:
    def __init__(self, width, height, rows, columns, sudoku):
        # gui window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sudoku')

        # baord variables
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns
        self.row_gap = round(self.width / self.rows)
        self.col_gap = round(self.height / self.columns)
        self.sudoku = sudoku
        self.cells = []
        self.original_cells = []

    # creates outlined board
    def create_board(self, rgb):
        # creates border
        pygame.draw.rect(self.window, (rgb), [0, 0, self.width, self.height], 2)

        # creates rows
        self.draw_row(rgb, self.row_gap, 3)
        
        # creates columns
        self.draw_col(rgb, self.col_gap, 3)


        # pygame.display.update()

    def draw_row(self, rgb, row_gap, thick_row):
        for row in range(self.rows):
            y = math.ceil(row_gap * row)
            if row % thick_row == 0: pygame.draw.line(self.window, rgb, (0, y), (self.width, y), 2)
            else: pygame.draw.line(self.window, rgb, (0, y), (self.width, y), 1)

    def draw_col(self, rgb, col_gap, thick_col):
        for col in range(self.columns):
            x = col_gap * col
            if col % thick_col == 0: pygame.draw.line(self.window, rgb, (x, 0), (x, self.height), 2)
            else: pygame.draw.line(self.window, rgb, (x, 0), (x, self.height), 1)

    def add_cells(self):
        x = self.row_gap
        y = self.col_gap

        for row in range(self.rows):
            for col in range(self.columns):
                # 9x9 input boxes
                key = self.sudoku.board[row][col]
                box = cell(x * col, y * row, x, y, row, col, key)
                self.cells.append(box)
        return self.cells

    def fill_board(self, board):
        index = 0
        for row in range(self.rows):
            for col in range(self.columns):
                self.cells[index].change_key(board[row][col])
                index += 1
        # return cells

    def check_board(self):
        sol = self.sudoku.solve()
        index = 0
        for row in range(self.rows):
            for col in range(self.columns):
                cell = self.cells[index]
                if sol[row][col] == cell.key: cell.color = COLOR_CORRECT
                else: cell.color = COLOR_WRONG
                cell.thickness = 2
                index += 1

    def reset_colors_thickness(self):
        for i in range(len(self.cells)):
            self.cells[i].color = COLOR_INACTIVE
            self.cells[i].thickness = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # self.fill_board(self.sudoku.solve())
                self.sudoku.visual_solve(self.cells)
            if event.key == pygame.K_d:
                self.fill_board(self.sudoku.original_board)
                self.reset_colors_thickness()
            if event.key == pygame.K_c:
                self.check_board()
                # check answer

        

# class Cell:
#     def __init__(self, width, height):



width = 600
height = 600
rows = 9
cols = 9
window = pygame.display.set_mode((width, height))


COLOR_READ_ONLY = pygame.Color('gray')
COLOR_INACTIVE = pygame.Color('black')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_CORRECT = pygame.Color('green')
COLOR_WRONG = pygame.Color('red')

FONT = pygame.font.Font(None, 32)
FONT_READ_ONLY = pygame.font.Font(None, 32)
# FONT_READ_ONLY.bold



# [left, top, width, height]
# pygame.draw.rect(window, (0, 0, 0), [0, 0, width, height], 1)
# pygame.display.update()

# cell = pygame.Rect(200,200,140,32)

# event.key : key
KEYS = {
    49: 1,
    50: 2,
    51: 3,
    52: 4,
    53: 5,
    54: 6,
    55: 7,
    56: 8,
    57: 9
}



sudoku_filled = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]

sudoku = Sudoku(sudoku_filled)


class cell:
    def __init__(self, x, y, width, height, row, col, key, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.row = row
        self.col = col
        self.width = width
        self.height = height

        self.color = COLOR_INACTIVE


        self.active = False
        self.thickness = 1
        self.key = key
        
        # fillable cells
        if key == 0: 
            self.read_only = False
            self.text = text
            self.text_surface = FONT.render(text, True, self.color)

            # self.color = COLOR_INACTIVE
        # already filled cells (read only)
        else: 
            self.read_only = True
            self.text = str(self.key)
            self.text_surface = FONT_READ_ONLY.render(text, True, self.color)

            # self.color = COLOR_READ_ONLY
        
    def select_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.read_only:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.thickness = 2 if self.active else 1

    def handle_event(self, event):
        self.select_event(event)


        if event.type == pygame.KEYDOWN and self.active:
            if event.key in KEYS and self.key == 0: 
                self.key = KEYS[event.key]
                self.text += event.unicode

            if event.key == pygame.K_RETURN:
                self.text = str(self.key)
                sudoku.board[self.row][self.col] = self.key
                print(sudoku.board)

            if event.key == pygame.K_BACKSPACE:
                # removes num from sudoku
                if self.key != 0 and self.text == str(self.key):
                    self.key = 0
                    sudoku.board[self.row][self.col] = self.key
                    self.text = ''
                self.text = self.text[:-1]
                    
        
        # Re-render the text.
        if self.read_only: self.text_surface = FONT_READ_ONLY.render(self.text, True, self.color)
        else: self.text_surface = FONT.render(self.text, True, self.color)
        # self.text_surface.get_rect(center=(self.width / 2, self.height / 2))
        

    def draw(self, window):
        # Blit the text.
        # window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        # window.blit(self.text_surface, self.rect,  self.rect.center=(width/2, height/2))
        window.blit(self.text_surface, (self.rect.x + 4 + round(self.width/3), self.rect.y + 2 + round(self.height/3)))

        # Blit the rect.
        pygame.draw.rect(window, self.color, self.rect, self.thickness)
    
    def change_key(self, key):
        self.key = key
        if key == 0: self.text = ""
        else: self.text = str(key)
        self.draw(window)
        



def main(): 
    board = Board(width, height, rows, cols, sudoku)

    window.fill((255, 255, 255))

    running = True
    clock = pygame.time.Clock()
    input_boxes = board.add_cells()

    while running:

        for event in pygame.event.get():
            # let each input box handle an event

            board.handle_event(event)

            for box in input_boxes:
                box.handle_event(event)

            # quit event
            if event.type == pygame.QUIT:
                running = False
        
        window.fill((255, 255, 255))
        board.create_board((0, 0, 0))
        for box in input_boxes:
            box.draw(window)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
