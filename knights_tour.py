# find board dimensions
# use backtracking algorithm to find correct path
# create a gui to display this


# create + fill board
# place knight on first square
# find possible knight moves
    # none = back track

# to move knight, increase current position by its move set (e.g. up 2 right 1)

UNVISITED = -1

def print_board(board):
    """
    Prints the solved board

    Args:
        board (2d list): chess board
    """
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end=' ')
        print()

def gen_board(length):
    """
    Generates a 2d list to represent a chess board

    Args:
        length (int): chess board length

    Returns:
        2d list: chess board
    """
    return [[UNVISITED] * length for i in range(length)]

def solve(length):
    """
    Solves Knight's Tour problem

    Args:
        length (int): board length
    """
    board = gen_board(length)
    move = 0

    # place knight on first square
    board[0][0] = 0

    if move_knight(board, 0, 0, move): print_board(board)
    else: print("No solution")


def is_valid_move(board, x, y):
    """
    Checks if move is valid

    Args:
        board (2d list): board
        x (int): row
        y (int): column

    Returns:
        boolean: True = valid; False = invalid
    """
    if x >= 0 and y >= 0 and x < len(board) and y < len(board) and board[x][y] == UNVISITED: return True
    return False

def move_knight(board, x, y, move):
    """
    Recursively moves the knight across the board

    Args:
        board (2d list): board
        x (int): row
        y (int): column
        move (int): move number

    Returns:
        boolean: True = finished moving; False = impossible to move knight
    """
    # possible move set
    knight_x = [1, 2, 2, 1, -1, -2, -2, -1]
    knight_y = [2, 1, -1, -2, -2, -1, 1, 2]

    # win condition
    if move + 1 == len(board)**2: return True

    # loops through possible moves
    for i in range(len(knight_x)):
        new_x = x + knight_x[i]
        new_y = y + knight_y[i]

        if is_valid_move(board, new_x, new_y):
            move += 1
            board[new_x][new_y] = move

            if (move_knight(board, new_x, new_y, move)): return True

            # back tracks if move leads to dead end
            board[new_x][new_y] = UNVISITED
            move -= 1
    
    return False


if __name__ == '__main__':
    solve(5)
