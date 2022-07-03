import math

import pygame

# make square
# make a 3x3 square
# fill into 9x9 square

# initialize modules
pygame.init()

class Board:
    def __init__(self, width, height, rows, columns):
        # gui window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sudoku')
        self.window.fill((255, 255, 255))

        # baord variables
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns
        self.row_gap = round(self.width / self.rows)
        self.col_gap = round(self.height / self.columns)

    # creates outlined board
    def create_board(self, rgb):
        # creates border
        pygame.draw.rect(self.window, (rgb), [0, 0, self.width, self.height], 2)

        # creates rows
        self.draw_row(rgb, self.row_gap, 3)
        
        # creates columns
        self.draw_col(rgb, self.col_gap, 3)

        pygame.display.update()

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
        cells = []
        x = self.row_gap
        y = self.col_gap

        for row in range(self.rows):
            for col in range(self.columns):
                # 9x9 input boxes
                box = cell(x * row, y * col, x, y)
                cells.append(box)
        return cells


# class Cell:
#     def __init__(self, width, height):



width = 600
height = 600
rows = 9
cols = 9

COLOR_INACTIVE = pygame.Color('black')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


# [left, top, width, height]
# pygame.draw.rect(window, (0, 0, 0), [0, 0, width, height], 1)
# pygame.display.update()

# cell = pygame.Rect(200,200,140,32)







class cell:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLOR_INACTIVE
        self.text = text
        self.text_surface = FONT.render(text, True, self.color)
        self.active = False
        self.thickness = 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            # self.thickness = 2 if self.active else 1

            # if self.active:
            #     self.color = COLOR_ACTIVE
            #     self.thickness = 2
            # else: 
            #     self.color = COLOR_INACTIVE
            #     self.thickness = 1

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.text_surface = FONT.render(self.text, True, self.color, (255, 255, 255))

    def draw(self, window):
        # Blit the text.
        window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(window, self.color, self.rect, self.thickness)



def main(): 
    board = Board(width, height, rows, cols)

    window = pygame.display.set_mode((width, height))
    window.fill((255, 255, 255))

    running = True
    clock = pygame.time.Clock()
    input_boxes = board.add_cells()

    while running:
        board.create_board((0, 0, 0))

        for event in pygame.event.get():
            # let each input box handle an event
            for box in input_boxes:
                box.handle_event(event)

            # quit event
            if event.type == pygame.QUIT:
                running = False

        for box in input_boxes:
            box.draw(window)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
