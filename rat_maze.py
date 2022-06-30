
VISITED = 2

def print_solultion(maze):
    for i in range(len(maze)): 
        for j in range(len(maze)):
            if maze[i][j] == VISITED: print("1", end=' ')
            else: print("0", end=' ')
        print()

def solve(maze):
    x, y = 0, 0
    maze[x][y] = VISITED
    if (move_rat(maze, x, y)): print_solultion(maze)
    else: print("Impossible Maze")

def move_rat(maze, x, y):
    moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]

    if x == len(maze) - 1 and y == len(maze) - 1: return True

    # print_solultion(maze)

    for move in moves:
        new_x = x + move[0]
        new_y = y + move[1]
        if is_valid_move(maze, new_x, new_y):
            maze[new_x][new_y] = VISITED
            if (move_rat(maze, new_x, new_y)): return True
            maze[new_x][new_y] = 1
    
    return False


    

def is_valid_move(maze, x, y):
    if x >= 0 and y >= 0 and x < len(maze) and y < len(maze) and maze[x][y] == 1: return True
    return False

if __name__ == '__main__':

    maze =[[0 for x in range(4)]for y in range(4)]

    maze = [[1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1],
            [0, 1, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 0, 0, 1, 1]]

    solve(maze)
