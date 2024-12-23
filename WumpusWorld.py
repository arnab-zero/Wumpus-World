from Agent import Agent
from xml.dom import NotFoundErr

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