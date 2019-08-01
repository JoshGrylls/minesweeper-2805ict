from random import randint

# Global constants
WIDTH = 40
NO_BOMBS = 10
NO_ROWS = 9
NO_COLS = 9

# Singular tile
class Tile:
    def __init__(self):
        self.mine = False
        self.mineCount = None

# Create gird as game board
gameBoard = [[Tile() for n in range(NO_COLS)] for n in range(NO_ROWS)]

# Place bombs randomly around the screen
for n in range(NO_BOMBS):
    while True:
        x = randint(0, NO_COLS-1)
        y = randint(0, NO_ROWS-1)
        if gameBoard[y][x].mine == False:
            gameBoard[y][x].mine = True
            break
        
def setup():
    size(360, 360)
    
def draw():
    #draw tiles
    y = 0
    for row in gameBoard:
        x = 0
        for tile in row:
            if tile.mine == True:
                fill(255, 150, 50)
            else:
                fill(255)
            rect(x, y, WIDTH, WIDTH)
            
            # Draw number of surrounding mines
            fill(0, 0, 0)
            if tile.mineCount != None:
                text(tile.mineCount, x+WIDTH/2, y+WIDTH/2)
            
            x += WIDTH
        y += WIDTH
        
def mousePressed():
    # Get click x and y coordinates
    clickX = mouseX/WIDTH
    clickY = mouseY/WIDTH
    
    # count number of mines surrounding the clicked tile
    mineC = 0
    for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        if inBoard(clickX+dx, clickY+dy) and gameBoard[clickY+dy][clickX+dx].mine:
            mineC += 1
    if mineC > 0:
        gameBoard[clickY][clickX].mineCount = mineC
            
def inBoard(x, y):
    if x >= 0 and x < NO_COLS and y >= 0 and y < NO_ROWS:
        return True
    return False
