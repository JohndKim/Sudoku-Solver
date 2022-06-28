# sudoku solver

def solve(board):
    """
    Outputs the solution if board is solved
    Args:
        board (2d array): sudoku board
    """
    if (solve_board(board)): print_solution(board)
    else: print("No solution")

def solve_board(board):
    """
    Solves the sudoku board through backtracking

    Args:
        board (2d array): sudoku board

    Returns:
        _type_: True = solution found; False = no solution
    """
    if not find_empty_space(board): return True

    row, col = find_empty_space(board)
    moves = gen_moves(board, row, col)

    # goes through each possible move
    for move in moves:
        # added move to board
        board[row][col] = move
        # checks if next square has legal moves
        if (solve_board(board)): return True
        
        # else back track
        board[row][col] = 0

    return False

def find_empty_space(board):
    """finds empty sudoku space

    Args:
        board (2d array): sudoku board

    Returns:
        _type_: empty board index
    """
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0: return i, j
    return False

def get_box_list(board, row, col):
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
            box_list.append(board[i + box_row][j + box_col])
    
    return box_list
            

def get_col_list(board, col):
    """
    gets the list of integers in the column

    Args:
        board (2d array): sudoku board
        col (int): column index

    Returns:
        array: column list
    """
    col_list = []
    for i in range(len(board)):
        col_list.append(board[i][col])
    return col_list


def gen_moves(board, row, col):
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
    row_list = board[row]
    col_list = get_col_list(board, col)
    box_list = get_box_list(board, row, col)

    # find moves
    for i in range(1, 10):
        if i in row_list or i in col_list or i in box_list:
            continue
        moves.append(i)
    return moves

def print_solution(board):
    """
    Prints complete sudoku 

    Args:
        board (2d array): sudoku board
    """
    length = len(board)
    for i in range(length):
        for j in range(length):
            print(board[i][j], end=" | ")
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
    
    solve(board)
