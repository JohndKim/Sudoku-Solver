import copy
import pygame
from sudoku import get_solution, visual, gen_sudoku


pygame.init()


WIDTH, HEIGHT, ROW, COL = 600, 600, 9, 9

BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (0, 0, 255)

ANSWER_COLOR = (0, 0, 0)
GUESS_COLOR = (128, 128, 128)

WRONG_COLOR = (255, 0, 0)
CORRECT_COLOR = (0, 255, 0)


class Sudoku:
    """A class representing a sudoku game"""
    def __init__(self, window):
        """Initializes the sudoku game with a randomly generated sudoku, the unsolved copy, the solution, and the board

        Args:
            window (pygame window): gui window
        """
        self.sudoku = gen_sudoku()
        self.unsolved_sudoku = copy.deepcopy(self.sudoku)
        self.solved_sudoku = get_solution(self.sudoku)
        self.board = Board(window, WIDTH, HEIGHT, ROW, COL, self.sudoku)
        
    def click_event(self, pos):
        """The event that occurs during any clicks;
        finds the cell location clicked, selects it, and stores the selected location

        Args:
            pos (tuple): x, y position on the gui
        """
        x, y = pos
        x = int(x / self.board.col_gap)
        y = int(y / self.board.row_gap)
        
        self.board.cells[y][x].selected = True
        self.board.selected_cell = y, x
    
    def add_temp(self, key):
        """Adds a temporary value to a cell

        Args:
            key (int): temporary value to add
        """
        y, x = self.board.selected_cell
        cell = self.board.cells[y][x]
        cell.temp = key        
        cell.draw()
    
    def fill_sol(self):
        """Fills the board with the solution + updates board"""
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                self.sudoku[row][col] = self.solved_sudoku[row][col]
                self.board.cells[row][col].value = self.solved_sudoku[row][col]
                self.board.cells[row][col].temp = self.solved_sudoku[row][col]
                self.board.cells[row][col].draw()
    
    def check_sol(self):
        """Checks current board to see which cells are correct and incorrect"""
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.cells[row][col]
                if cell.value != self.solved_sudoku[row][col]: cell.correct = False
                else: cell.correct = True
     
    def submit_value(self):
        """After a temp value is added, pressing 'enter' will submit the value
        This value will be checked with the solution;
        Correct = accepted
        Incorrect = empty cell
        """
        y, x = self.board.selected_cell
        cell = self.board.cells[y][x]
        value = cell.temp
        
        # if correct value
        if self.check_value(x, y, value):
            cell.value = value
            self.unclick()
            
            self.board.selected_cell = None
            cell.draw()
        else:
            self.unclick()
            cell.temp = 0
            
            self.board.selected_cell = None


    def check_value(self, x, y, value):
        """Checks the value in the cell with solution and returns if it is correct"""
        if self.solved_sudoku[y][x] == value: return True
        return False
        
    
    def unclick(self):
        """Unclicks the cell (deselects) and removes the selected cell's location"""
        if self.board.selected_cell is None: return
        y, x = self.board.selected_cell
        cell = self.board.cells[y][x]
        cell.selected = False
        cell.draw()
    
    def remove_value(self):
        """Pressing 'backspace' will remove the current temp value from the cell"""
        y, x = self.board.selected_cell
        cell = self.board.cells[y][x]
        cell.temp = 0
        
        cell.draw()
        
    def update(self):
        """Updates the entire board and ensures that the cells are correctly shown"""
        for row in range(self.board.rows):
            for col in range(self.board.cols):                
                self.board.cells[row][col].value = self.sudoku[row][col]
                self.board.cells[row][col].temp = self.sudoku[row][col]
                self.board.cells[row][col].draw()
        
        pygame.time.wait(10)
        pygame.display.update()

    def clear(self):
        """Clears the board and resets it to its initial state"""
        for row in range(self.board.rows):
            for col in range(self.board.cols):        
                self.sudoku[row][col] = self.unsolved_sudoku[row][col]        
                self.board.cells[row][col].value = self.unsolved_sudoku[row][col]
                self.board.cells[row][col].temp = self.unsolved_sudoku[row][col]
                self.board.cells[row][col].correct = None
                self.board.cells[row][col].draw()
        
        self.board.remove_highlighted_cells(0, 0)
        
        pygame.display.update()
    
    def new_board(self):
        """Generates a new sudoku game"""
        sudoku = gen_sudoku()
        
        self.sudoku = sudoku
        self.unsolved_sudoku = copy.deepcopy(sudoku)
        self.solved_sudoku = get_solution(self.sudoku)
        
        self.clear()
        


class Board:
    """A class representing the board of a sudoku game
    """
    def __init__(self, window, width, height, rows, cols, sudoku):
        """Initializes the window, width, height, rows, cols, and sudoku board

        Args:
            window (pygame window): gui window
            width (int): width of window
            height (int): height of window
            rows (int): number of rows
            cols (int): number of columns
            sudoku (2d array): sudoku board values
        """
        self.window = window
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.row_gap = height / 9
        self.col_gap = width / 9
        
        self.cells = [[Cell(window, width, height, i, j, self.row_gap, self.col_gap, sudoku[i][j]) for j in range(cols)] for i in range(rows)]
        self.selected_cell = None
            
    def draw_board(self):
        """Draws the board on the gui"""
        self.draw_grid()
        
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].draw()
             
    def draw_grid(self):
        """Draws the grid lines on the gui
        """
        thickness = 1
    
        self.window.fill(BG_COLOR)

        # draws the rows
        for r in range(self.rows):
            if r % 3 == 0: thickness = 2
            else: thickness = 1
            pygame.draw.line(self.window, LINE_COLOR, (r * self.row_gap, 0), (r * self.row_gap, self.width), width=thickness)
        
        # draws the columns
        for c in range(self.cols):
            if c % 3 == 0: thickness = 2
            else: thickness = 1
            pygame.draw.line(self.window, LINE_COLOR, (0, c * self.col_gap), (self.height, c * self.col_gap), width=thickness)


    def highlight_cells(self, row, col):
        """Highlights the cells from 0,0 to row, col

        Args:
            row (int): row 
            col (int): column
        """
        for r in range(row):
            for c in range(col):
                self.cells[r][c].highlight = True
        pygame.display.update()
    
    def remove_highlighted_cells(self, row, col):
        """Removes all highlighted cells from the current row, col to the end

        Args:
            row (int): row
            col (int): column
        """
        for r in range(row, self.rows):
            for c in range(col, self.cols):
                self.cells[r][c].highlight = False
    
        
class Cell:
    """Class representing a single cell in a sudoku board"""
    def __init__(self, window, width, height, row, col, row_gap, col_gap, value):
        """Initializes the gui window, width, height, row, col, row_gap, col_gap, and value

        Args:
            window (pygame window): gui window
            width (int): width of window
            height (int): height of window
            row (int): row coord
            col (int): column coord
            row_gap (int): length of row gap
            col_gap (int): length of column gap
            value (int): the current value of the cell
        """
        self.window = window
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
        self.correct = None
        
        if value == 0: self.active = True
        else: self.active = False
        
        self.font = pygame.font.SysFont('Arial', 18)
        
    def empty_text(self, x, y):
        """Adds an empty text to the cell to cover its previous value

        Args:
            x (int): x coord
            y (int): y coord
        """
        text = self.font.render("   ", 1, (121, 121, 121), BG_COLOR)
        # window.blit(text, (x + 5, y + 5))
        self.window.blit(text, (x + (self.col_gap/2 - text.get_width()/2), y + (self.row_gap/2 - text.get_height()/2)))
        
    
    def draw(self):  
        """Draws the cell"""      
        x = self.col * self.col_gap
        y = self.row * self.row_gap
        
        # FOR THE NUMBER IN THE CELL
        
        # if hasnt submitted a value yet OR reset value to 0
        if self.value == 0 and self.temp == 0:
            self.empty_text(x, y)
            # pygame.draw.rect(window, bg_color, (x, y, self.row_gap - 10, self.col_gap - 10), width=0)
     
        # player added temp value 
        elif self.value == 0 and self.temp != 0:
            text = self.font.render(str(self.temp), 1, GUESS_COLOR, BG_COLOR)
            self.window.blit(text, (x + 5, y + 5))
        
        # for all preplaced values + ones that the player has submitted
        elif self.value != 0:
            self.empty_text(x, y)
            
            text = self.font.render(str(self.value), 1, ANSWER_COLOR, BG_COLOR)
            # centers text
            self.window.blit(text, (x + (self.col_gap/2 - text.get_width()/2), y + (self.row_gap/2 - text.get_height()/2)))

        else:
            text = self.font.render(str(self.value), 1, GUESS_COLOR, BG_COLOR)
            self.window.blit(text, (x + 5, y + 5))
     
        # FOR THE CELL'S BORDER
     
        if self.selected and self.active:
            pygame.draw.rect(self.window, SELECTED_COLOR, (x, y, self.row_gap + 2, self.col_gap + 2), 2)

        if self.highlight or self.correct:
            pygame.draw.rect(self.window, CORRECT_COLOR, (x, y, self.row_gap + 2, self.col_gap + 2), 2)
        elif self.correct == False:
            pygame.draw.rect(self.window, WRONG_COLOR, (x, y, self.row_gap + 2, self.col_gap + 2), 2)
            

def backtrack(sudoku):
    """Solves the sudoku + visualizes it via a backtracking algorithm

    Args:
        sudoku (Sudoku): a sudoku object
    """
    visual(sudoku)


def main():
    """Main function that runs the game"""
    # window that displays the game
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sudoku')

    # sudoku game object
    sudoku_game = Sudoku(window)

    is_playing = True

    # game loop
    while is_playing:
        sudoku_game.board.draw_board()
        key = None
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # various controls
                if event.key == pygame.K_SPACE:
                    backtrack(sudoku_game)
                if event.key == pygame.K_RETURN:
                    sudoku_game.submit_value()
                if event.key == pygame.K_BACKSPACE:
                    sudoku_game.remove_value()
                if event.key == pygame.K_c:
                    sudoku_game.clear()
                if event.key == pygame.K_v:
                    sudoku_game.check_sol()
                if event.key == pygame.K_x:
                    sudoku_game.fill_sol()
                if event.key == pygame.K_r:
                    sudoku_game.new_board()
                    
                # entering a value into a cell
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
                
            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                sudoku_game.unclick()
                pos = pygame.mouse.get_pos()
                sudoku_game.click_event(pos)  
                key = None    
            
            # add temp value to cell
            if sudoku_game.board.selected_cell and key:
                sudoku_game.add_temp(key)
                
            # quit event
            if event.type == pygame.QUIT:
                is_playing = False
            
        pygame.display.update()

if __name__ == "__main__":
    main()
    