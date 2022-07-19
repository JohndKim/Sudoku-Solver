import copy
import pygame
from sudoku import get_solved_board, visual



sudoku = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]

unsolved_sudoku = copy.deepcopy(sudoku)

solved_sudoku = get_solved_board(sudoku)

pygame.init()


width, height, row, col = 600, 600, 9, 9
bg_color = (255, 255, 255)
line_color = (0, 0, 0)
selected_color = (0, 0, 255)

answer_color = (0, 0, 0)
guess_color = (128, 128, 128)

wrong_color = (255, 0, 0)
correct_color = (0, 255, 0)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sudoku')

class Board:
    def __init__(self, sudoku, width, height, rows, cols):
        self.sudoku = sudoku
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.row_gap = height / 9
        self.col_gap = width / 9
        
        self.cells = [[Cell(width, height, i, j, self.row_gap, self.col_gap, sudoku[i][j]) for j in range(cols)] for i in range(rows)]
        self.selected_cell = None
            
    def draw_board(self):
        self.draw_grid()
        
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].draw()
     
        # draws the cells with their number
        
    def draw_grid(self):
        thickness = 1
    
        window.fill(bg_color)

        # draws the rows
        for r in range(self.rows):
            if r % 3 == 0: thickness = 2
            else: thickness = 1
            pygame.draw.line(window, line_color, (r * self.row_gap, 0), (r * self.row_gap, self.width), width=thickness)
        
        # draws the columns
        for c in range(self.cols):
            if c % 3 == 0: thickness = 2
            else: thickness = 1
            pygame.draw.line(window, line_color, (0, c * self.col_gap), (self.height, c * self.col_gap), width=thickness)
     
    
    def click_event(self, pos):
        x, y = pos
        x = int(x / self.col_gap)
        y = int(y / self.row_gap)
        
        self.cells[y][x].selected = True
        self.selected_cell = y, x
    
    def add_temp(self, key):
        y, x = self.selected_cell
        cell = self.cells[y][x]
        cell.temp = key
        
        cell.draw()
    
    def submit_value(self):
                
        y, x = self.selected_cell
        cell = self.cells[y][x]
        value = cell.temp
        
        # if correct value
        if self.check_value(x, y, value):
            cell.value = value
            self.unclick()
            
            self.selected_cell = None
            cell.draw()
        else:
            self.unclick()
            cell.temp = 0
            
            self.selected_cell = None

    def highlight_cells(self, row, col):
        for r in range(row):
            for c in range(col):
                self.cells[r][c].highlight = True
    
    def remove_highlighted_cells(self, row, col):
        for r in range(row, self.rows):
            for c in range(col, self.cols):
                # if self.cells[r][c].highlight == False: return
                self.cells[r][c].highlight = False
                
        
    
    def check_value(self, x, y, value):
        if solved_sudoku[y][x] == value: return True
        return False
        
    
    def unclick(self):
        if self.selected_cell is None: return
        y, x = self.selected_cell
        cell = self.cells[y][x]
        
        # white rect to cover previous selection
        pygame.draw.rect(window, bg_color, (x, y, self.row_gap + 2, self.col_gap + 2), 2)

        pygame.display.update()

        cell.selected = False
        cell.draw()
    
    def remove_value(self):
        y, x = self.selected_cell
        cell = self.cells[y][x]
        cell.temp = 0
        
        cell.draw()
    
    def update(self):
        for row in range(self.rows):
            for col in range(self.cols):                
                self.cells[row][col].value = self.sudoku[row][col]
                self.cells[row][col].temp = self.sudoku[row][col]
                self.cells[row][col].draw()
        
        pygame.time.wait(10)
        pygame.display.update()

    def clear(self):
        for row in range(self.rows):
            for col in range(self.cols):                
                self.cells[row][col].value = unsolved_sudoku[row][col]
                self.cells[row][col].draw()
        
        self.remove_highlighted_cells(0, 0)
        
        pygame.display.update()
        
        # for row in range(self.rows):
        #     for col in range(self.cols):
        #         if self.cells[row][col].value != 0: continue
                
        #         pygame.time.wait(10)
        #         self.cells[row][col].value = solved_sudoku[row][col]
        #         self.cells[row][col].draw()
        #         pygame.display.update()
        
        
class Cell:
    def __init__(self, width, height, row, col, row_gap, col_gap, value):
        self.temp = 0
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.row_gap = row_gap
        self.col_gap = col_gap
        self.value = value
        self.selected = False
        self.highlight = False
        
        if value == 0: self.active = True
        else: self.active = False
        
        self.font = pygame.font.SysFont('Arial', 18)
        
    def empty_text(self, x, y):
        text = self.font.render("   ", 1, (121, 121, 121), bg_color)
        # window.blit(text, (x + 5, y + 5))
        window.blit(text, (x + (self.col_gap/2 - text.get_width()/2), y + (self.row_gap/2 - text.get_height()/2)))
        
    
    def draw(self):        
        x = self.col * self.col_gap
        y = self.row * self.row_gap
        
        # if hasnt submitted a value yet OR reset value to 0
        if self.value == 0 and self.temp == 0:
            self.empty_text(x, y)
            # pygame.draw.rect(window, bg_color, (x, y, self.row_gap - 10, self.col_gap - 10), width=0)
     
        # player added temp value 
        elif self.value == 0 and self.temp != 0:
            text = self.font.render(str(self.temp), 1, guess_color, bg_color)
            window.blit(text, (x + 5, y + 5))
        
        # for all preplaced values + ones that the player has submitted
        elif self.value != 0:
            self.empty_text(x, y)
            
            text = self.font.render(str(self.value), 1, answer_color, bg_color)
            # centers text
            window.blit(text, (x + (self.col_gap/2 - text.get_width()/2), y + (self.row_gap/2 - text.get_height()/2)))

        
        else:
            text = self.font.render(str(self.value), 1, guess_color, bg_color)
            window.blit(text, (x + 5, y + 5))
        
        # if self.active and self.temp != 0 and self.value == 0:
        #     text = self.font.render(str(self.temp), 1, (121, 121, 121))
        #     window.blit(text, (x + 5, y + 5))
        # elif self.active and self.value != 0:
        #     text = self.font.render(str(self.value), 1, (121, 121, 121))
        #     window.blit(text, (x + 5, y + 5))
        #     self.active = False

        # centers text
        # window.blit(text, (x + (self.col_gap/2 - text.get_width()/2), y + (self.row_gap/2 - text.get_height()/2)))

        if self.selected and self.active:
            pygame.draw.rect(window, selected_color, (x, y, self.row_gap + 2, self.col_gap + 2), 2)
        
        if self.highlight:
            pygame.draw.rect(window, correct_color, (x, y, self.row_gap + 2, self.col_gap + 2), 2)


            
        # pygame.display.update()
    

# each cube is just an image
# user clicking on one => calculate which box (coords)
# changes box thickness
# user enters a key => change value + shown value

board = Board(sudoku, width, height, row, col)


def backtrack():
    visual(board)
    print("done")


is_playing = True

while is_playing:
    board.draw_board()
    key = None
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                backtrack()
            if event.key == pygame.K_RETURN:
                board.submit_value()
            if event.key == pygame.K_BACKSPACE:
                board.remove_value()
            if event.key == pygame.K_c:
                board.clear()
                
            if event.key == pygame.K_1:
                key = 1
            if event.key == pygame.K_2:
                key = 2
            if event.key == pygame.K_3:
                key = 3
            if event.key == pygame.K_4:
                key = 4
            if event.key == pygame.K_5:
                key = 5
            if event.key == pygame.K_6:
                key = 6
            if event.key == pygame.K_7:
                key = 7
            if event.key == pygame.K_8:
                key = 8
            if event.key == pygame.K_9:
                key = 9
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.unclick()
            pos = pygame.mouse.get_pos()
            board.click_event(pos)  
            key = None    
        
        # if cell and key are not None
        if board.selected_cell and key:
            board.add_temp(key)
            
        if event.type == pygame.QUIT:
            is_playing = False
        
    pygame.display.update()
