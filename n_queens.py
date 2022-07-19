def print_board(board):
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end=' ')
        print()


def gen_board(length):
    return [[0 for i in range(length)] for i in range(length)]

def solve(length):
    board = gen_board(length)
    
    if place_queen(board, 0): print_board(board)
    else: return False

def place_queen(board, col):
    # win condition
    if col >= len(board): return True
    
    for row in range(len(board)):
        if valid_move(board, row, col):
            board[row][col] = 1
            
            if place_queen(board, col + 1): return True
            
            board[row][col] = 0


def valid_move(board, row, col):
    # check row
    for i in range(col):
        if board[row][i] == 1: return False
    
    # top left diagonal
    # starts at the end, decreases one (e.g. 3, 2, 1, 0)
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1: return False
        
    # bottom left diagonal
    for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
        if board[i][j] == 1: return False
    
    return True
    # return board[x][y] == 0 and x >= 0 and x < len(board) and y >= 0 and y < len(board)


if __name__ == "__main__":
    solve(8)