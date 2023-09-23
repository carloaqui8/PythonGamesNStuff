import random
import re

class Board:
    def __init__(self, dim_size=10, num_bombs=10):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        #Initialize a set to keep track of where we've dug. Save (row, col) tuples into this set
        self.dug = set()

    def make_new_board(self):
        #Create physical board (2D list)
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        #Place the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)   #a <= N <= b
            row = loc // self.dim_size                      #Math Stuff
            col = loc % self.dim_size                       #Math Stuff

            if board[row][col] == '*':                      #If there's a bomb already there
                continue
            else:
                board[row][col] = '*'
                bombs_planted += 1
        return board
    
    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if (self.board[r][c] == '*'):               #If there's a bomb
                    continue
                else:
                    self.board[r][c] = self.get_num_neighboring_bombs(r, c)
                
    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0

        for r in range(max(0, row-1), min(self.dim_size-1, (row+1) + 1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1) + 1)):
                if (r == row and c == col):                 #Don't need to check location itself
                    continue
                elif self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col))

        if (self.board[row][col] == '*'):
            return False
        elif (self.board[row][col] > 0):
            return True
        
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1) + 1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1) + 1)):
                if (r, c) in self.dug:
                    continue
                else:
                    self.dig(r, c)
        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] == ' '

        return str(visible_board)


def play(dim_size=10, num_bombs=10):
    #1. Create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    #2. Show the user the board and ask where to dig
    

    #3. If location is a bomb, game over
    #       Else, dig recursively until each square is at least next to a bomb
    #4. Repeat 2 and 3 until there are no more places to dig (win) or until game over
    safe = True
    while (len(board.dug) < board.dim_size ** 2 - num_bombs):
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if (row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size):
            print("Invalid location. Try again")
            continue
        else:
            safe = board.dig(row, col)
            if not safe:
                break

    if safe:
        print("You win")
    else:
        print("dummy")
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]

if __name__ == '__main__':
    play()