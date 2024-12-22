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