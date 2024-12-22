from Agent import Agent
import random

def generateRandomInt ( limit ):
	return random.randrange(limit)


class AI ( Agent ):
    def __init__ ( self , numberOfGolds, arrows):
        self.__moves = 0
        self.__safe_tiles = []
        self.__unsafe_tiles = set()
        self.__tile_history = []
        self.__x_tile = 1
        self.__y_tile = 1
        self.__dir = 'E'
        self.__move_history = []
        self.__has_gold = False
        self.__numberOfGolds = numberOfGolds
        self.__revert_home = False
        self.__path_home = []
        self.__dest_path = []
        self.__dest_node = (1,1)
        self.__in_danger = False
        self.__last_danger = (0,0)
        self.__x_border = 9
        self.__y_border = 9
        self.__stop_iteration = False
        self.__stopped_on_iteration = 0
        self.__dead_wump = False
        self.__found_wump = False
        self.__numberOfWumpus = arrows
        self.__pitless_wump = False
        self.__wump_node = (0,0)
        self.__potential_wump_nodes = []
        self.__stench_nodes = []
        self.__potential_pit_nodes = []
        self.__breeze_nodes = []
        self.__shot_arrow = False
        self.__numberOfArrows = arrows
        self.__isInLoop = False
        pass
    
    def decideAction( self, stench, breeze, glitter, bump, scream ):
        self.__check_bump(bump)
        self.__update_history_tiles()
        self.__moves+=1
        return self.__determineAction(stench, breeze, glitter, bump, scream)
    
    class Node:
        def __init__(self, x,y):
            self.__node = (x,y)
            self.__Nnode = (x,y+1)
            self.__Enode = (x+1,y)
            self.__Snode = (x,y-1)
            self.__Wnode = (x-1,y)
        def getCurrent(self):
            return self.__node
        def getNorth(self):
            return self.__Nnode
        def getEast(self):
            return self.__Enode
        def getSouth(self):
            return self.__Snode
        def getWest(self):
            return self.__Wnode
        def getX(self):
            return self.__node[0]
        def getY(self):
            return self.__node[1]
        
    def __getExploredAllSafeNodes(self):
         for i in range(len(self.__safe_tiles)):
            node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
            if node not in self.__tile_history:
                return False
         return True

    def __Facing_Wump(self):
        if self.__dir == "N":
            if self.__wump_node[1]>self.__y_tile:
                return True
            else:
                return False
        elif self.__dir == "E":
            if self.__wump_node[0]>self.__x_tile:
                return True
            else:
                return False
        elif self.__dir == "S":
            if self.__wump_node[1]<self.__y_tile:
                return True
            else:
                return False
        elif self.__dir == "W":
            if self.__wump_node[0]<self.__x_tile:
                return True
            else:
                return False
        return True

    def __Align_To_Wump(self,stench, breeze, glitter, bump, scream):
        curNode = self.Node(self.__x_tile,self.__y_tile)
        nextNode = self.Node(self.__wump_node[0], self.__wump_node[1])
        self.__print_debug_info(stench, breeze, glitter, bump, scream)
        return self.__NodeToNode(nextNode,curNode)