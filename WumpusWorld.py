from Agent import Agent
from xml.dom import NotFoundErr
import random

class WumpusWorld():
    
    class __Tile:
        agent = False
        visited = False
        pit = False
        wumpus = False
        gold = False
        breeze = False
        stench = False

    def __init__ ( self, debug = False, file = None ):
        self.__debug = debug
        
        # Agent Initialization
        self.__goldLooted = False
        self.__numberOfGolds = 0
        self.__hasArrow = True
        self.__numberOfArrows = 0
        self.__bump = False
        self.__scream = False
        self.__score = 0
        self.__agentDir = 0
        self.__agentX = 0
        self.__agentY = 0
        self.__lastAction = Agent.Action.CLIMB
        self.__board = NotFoundErr
        self.__colDimension = 10
        self.__rowDimension = 10
        self.__agent = None
            
        if file != None:
            self.__board = [[self.__Tile() for j in range(self.__rowDimension)] for i in range(self.__colDimension)]
            self.__addBoardFeatures(file)
        else:
            
            self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
            self.__addBoardFeatures()



    def __addGold ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].gold = True
    

    def __addStench ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].stench = True
    

    def __addBreeze ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].breeze = True
    

    def __isInBounds ( self, c, r ):
        return c < self.__colDimension and r < self.__rowDimension and c >= 0 and r >= 0
    
    def __addPit ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].pit = True
            self.__addBreeze ( c+1, r )
            self.__addBreeze ( c-1, r )
            self.__addBreeze ( c, r+1 )
            self.__addBreeze ( c, r-1 )
    

    def __addWumpus ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].wumpus = True
            self.__addStench ( c+1, r )
            self.__addStench ( c-1, r )
            self.__addStench ( c, r+1 )
            self.__addStench ( c, r-1 )


    def __printBoardInfo ( self ):
        for r in range (self.__rowDimension-1, -1, -1):
            for c in range (self.__colDimension):
                self.__printTileInfo( c, r )
            print("")
            print("")


    def __printTileInfo ( self, c, r ):
        tileString = ""
        
        if self.__board[c][r].pit:    tileString += "P"
        if self.__board[c][r].wumpus: tileString += "W"
        if self.__board[c][r].gold:   tileString += "G"
        if self.__board[c][r].breeze: tileString += "B"
        if self.__board[c][r].stench: tileString += "S"
        
        if self.__agentX == c and self.__agentY == r:
            if self.__agentDir == 0:
                tileString += ">"
            
            elif self.__agentDir == 1:
                tileString += "v"
            
            elif self.__agentDir == 2:
                tileString += "<"
            
            elif self.__agentDir == 3:
                tileString += "^"
            #tileString += "@"
        
        tileString += "."
        
        print(tileString.rjust(8 ), end="")


    def __printActionInfo ( self ):
        if self.__lastAction == Agent.Action.TURN_LEFT:
            print ( "Last Action: Turned Left" )
        elif self.__lastAction == Agent.Action.TURN_RIGHT:
            print ( "Last Action: Turned Right")
        elif self.__lastAction == Agent.Action.FORWARD:
            print ( "Last Action: Moved Forward")
        elif self.__lastAction == Agent.Action.SHOOT:
            print ( "Last Action: Shot the Arrow")
        elif self.__lastAction == Agent.Action.GRAB:
            print ( "Last Action: Grabbed")
        elif self.__lastAction == Agent.Action.CLIMB:
            print ( "Last Action: Climbed")
        else:
            print ( "Last Action: Invalid")


    def __printPerceptInfo ( self ):
        perceptString = "Percepts: "
        
        if self.__board[self.__agentX][self.__agentY].stench: 
            perceptString += "Stench, "
        if self.__board[self.__agentX][self.__agentY].breeze: 
            perceptString += "Breeze, "
        if self.__board[self.__agentX][self.__agentY].gold:   
            perceptString += "Glitter, "
        if self.__bump:                         
            perceptString += "Bump, "
        if self.__scream:                       
            perceptString += "Scream"
        
        if perceptString[-1] == ' 'and perceptString[-2] == ',':
            perceptString = perceptString[:-2]
        
        print(perceptString)

    
    def __generateRandomInt ( self, limit ):
        return random.randrange(limit)