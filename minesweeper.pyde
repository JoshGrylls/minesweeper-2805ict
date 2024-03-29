from random import randint

# Globals
WIDTH = 40
NO_ROWS = 9
NO_COLS = 17
NO_BOMBS = NO_COLS+1
GAMESTATE = "PLAYING" #PLAYING/WON/LOST
DEBUG = "OFF"

# Singular tile
class Tile:
    def __init__(self):
        self.mine = False
        self.mineCount = None
        self.revealed = False
        self.flagged = False

# Create gird as game board
gameBoard = [[Tile() for n in range(NO_COLS)] for n in range(NO_ROWS)]

def restart():
    global DEBUG
    global GAMESTATE
    
    for i in range(NO_ROWS):
        for j in range(NO_COLS):
            gameBoard[i][j].mine = False
            gameBoard[i][j].mineCount = None
            gameBoard[i][j].revealed = False
            gameBoard[i][j].flagged = False
    
    GAMESTATE = "PLAYING"
    DEBUG = "OFF"
            
    # Place bombs randomly around the screen
    for n in range(NO_BOMBS):
        while True:
            x = randint(0, NO_COLS-1)
            y = randint(0, NO_ROWS-1)
            if gameBoard[y][x].mine == False:
                gameBoard[y][x].mine = True
                break

def setup():
    size(NO_COLS*WIDTH, NO_ROWS*WIDTH+60)
    restart()

def draw():
    global timer
    background(120)
    #draw tiles
    if GAMESTATE == "PLAYING":
        # start timer
        timer = millis()
        fill(timer % 255)
        textSize(50)
        text(timer/1000, 40, 410)
        textSize(15)
        y = 0
        for row in gameBoard:
            x = 0
            for tile in row:
                if tile.mine == True and DEBUG == "ON":
                    fill(255, 150, 50)
                elif tile.revealed:
                    fill(255)
                elif not tile.revealed:
                    fill(170)
                rect(x, y, WIDTH, WIDTH)
                
                if tile.flagged:
                    fill(0)
                    text("x", (x+WIDTH/2)-17, (y+WIDTH/2)-9)
                
                # Draw number of surrounding mines
                fill(0, 0, 0)
                if tile.mineCount != None:
                    text(tile.mineCount, (x+WIDTH/2)-3, (y+WIDTH/2)+3)
                
                x += WIDTH
            y += WIDTH 
        
    if GAMESTATE == "WON":
        textSize(15)
        text("YOU WIN!", 155, 395)
        textSize(50)
        text(timer/1000, 40, 410)
    
    if GAMESTATE == "LOST":
        textSize(15)
        text("YOU LOSE..", 140, 395)
        textSize(50)
        text(timer/1000, 40, 410)
    
    textSize(15)
    text("Press Enter", 255, 390)
    text("To Restart", 255, 405)
                
def mousePressed():
    global GAMESTATE
    # Get click x and y coordinates
    clickX = mouseX/WIDTH
    clickY = mouseY/WIDTH
    if mouseButton == LEFT and inBoard(clickX, clickY):
        if gameBoard[clickY][clickX].mine:
            GAMESTATE = "LOST"
        search(clickX, clickY)
    elif mouseButton == RIGHT and inBoard(clickX, clickY):
        # Add flag to tile
        tile = gameBoard[clickY][clickX]
        tile.flagged = True
        
        # Check all mines have been flagged
        gameWon = True
        for row in gameBoard:
            for t in row:
                if t.mine and not t.flagged:
                    gameWon = False
                    break
        if gameWon and GAMESTATE == "PLAYING":
            GAMESTATE = "WON"

def keyPressed():
    global DEBUG
    if key == TAB:
        if DEBUG == "OFF":
            DEBUG = "ON"
            print "Debug Mode ON"
        elif DEBUG == "ON":
            DEBUG = "OFF"
            print "Debug Mode OFF"
    if key == ENTER:
        print "restarting"
        restart()
            
def search(x, y):
    # If trying to search off board
    if not inBoard(x, y):
        return
    tile = gameBoard[y][x]
    # If the tilee has been revealed
    if tile.revealed:
        return
    # If the tile has a mine
    if tile.mine:
        return
    tile.revealed = True
    # If there are surrounding mines
    noOfMines = findNoOfMines(x, y)
    if noOfMines > 0:
        gameBoard[y][x].mineCount = noOfMines
        return
    
    for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        search(x+dx, y+dy)

        
def findNoOfMines(x, y):            
    # count number of mines surrounding the clicked tile
    mineC = 0
    for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        if inBoard(x+dx, y+dy) and gameBoard[y+dy][x+dx].mine:
            mineC += 1
    return mineC
        
        
def inBoard(x, y):
    if x >= 0 and x < NO_COLS and y >= 0 and y < NO_ROWS:
        return True
    return False
