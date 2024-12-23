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
    

    def getLoopBreakingNode(self,stench, breeze, glitter, bump, scream):
        possiblenodes = []
        for i in range(len(self.__tile_history)):
            nodetile = self.__tile_history[len(self.__tile_history)-i-1]
            gnode = self.Node(nodetile[0],nodetile[1])
            sidenode = gnode.getWest()

            if sidenode[0]>=1 and sidenode not in self.__tile_history and sidenode not in possiblenodes: #Left
                possiblenodes.append(sidenode)
            sidenode = gnode.getEast()
            if sidenode[0]<=self.__x_border and sidenode not in self.__tile_history and sidenode not in possiblenodes: #Right
                possiblenodes.append(sidenode)
            sidenode = gnode.getSouth()
            if sidenode[1]>=1 and sidenode not in self.__tile_history and sidenode not in possiblenodes: #down
                possiblenodes.append(sidenode)
            sidenode = gnode.getNorth()
            if sidenode[1]<=self.__y_border and sidenode not in self.__tile_history and sidenode not in possiblenodes: #Left
                possiblenodes.append(sidenode)
        size = len(possiblenodes)
        rand = generateRandomInt(size)
        risk = 100000
        index = 0
        for i in range(len(possiblenodes)):
            sidenode = self.Node(possiblenodes[i][0], possiblenodes[i][1])
            temp = self.getbestpos(sidenode)
            print("temp risk : " , temp, sidenode.getCurrent())
            if(temp<risk):
                risk = temp
                index = i
        
        return possiblenodes[index]
            
    def getbestpos(self, gnode):
        risk = 0
        sidenode = gnode.getEast()
        if sidenode[0]<=self.__x_border:  #Right
            risk += self.calcRisk(sidenode)
            print("right")
        sidenode = gnode.getNorth()
        if sidenode[1]<=self.__y_border:
            risk+=self.calcRisk(sidenode)
            print("up")
        sidenode = gnode.getSouth()
        if sidenode[1]>=1:
            risk+=self.calcRisk(sidenode)
            print("down")
        sidenode = gnode.getWest()
        if sidenode[0]>=1:
            risk+=self.calcRisk(sidenode)
            print("left")
        return risk
        
    def calcRisk(self, sidenode):
        risk = 0
        if sidenode in self.__breeze_nodes:
            risk += 300
        if sidenode in self.__stench_nodes:
            risk += 300
        if sidenode in self.__safe_tiles:
            risk -=10
        return risk
            

    def __Update_Potential_Pit_Locations(self):
        if (self.__x_tile,self.__y_tile) in self.__breeze_nodes:
            return
        else:
            self.__breeze_nodes.append((self.__x_tile,self.__y_tile))
        Pit_Spots = []
        if self.__x_tile-1>=1: #Left
            if (self.__x_tile-1,self.__y_tile) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile-1,self.__y_tile))
        if self.__x_tile+1<=self.__x_border: #Right
            if (self.__x_tile+1,self.__y_tile) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile+1,self.__y_tile))
        if self.__y_tile-1>=1: #Down
            if (self.__x_tile,self.__y_tile-1) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile,self.__y_tile-1))
        if self.__y_tile+1<=self.__y_border: #Up
            if (self.__x_tile,self.__y_tile+1) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile,self.__y_tile+1))
        if len(Pit_Spots)==2:
            if Pit_Spots[0] not in self.__potential_pit_nodes:
                self.__potential_pit_nodes.append(Pit_Spots[0])
            return
        for node in Pit_Spots:
            if node not in self.__potential_pit_nodes:
                self.__potential_pit_nodes.append(node)


    
    def __Update_Potential_Wump_Locations(self):
        if (self.__x_tile,self.__y_tile) in self.__stench_nodes:
            return
        else:
            self.__stench_nodes.append((self.__x_tile,self.__y_tile))
        Wump_Spots = []
        if not self.__found_wump:
            if self.__x_tile-1>=1: #Left
                if (self.__x_tile-1,self.__y_tile) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile-1,self.__y_tile))
            if self.__x_tile+1<=self.__x_border: #Right
                if (self.__x_tile+1,self.__y_tile) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile+1,self.__y_tile))
            if self.__y_tile-1>=1: #Down
                if (self.__x_tile,self.__y_tile-1) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile,self.__y_tile-1))
            if self.__y_tile+1<=self.__y_border: #Up
                if (self.__x_tile,self.__y_tile+1) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile,self.__y_tile+1))
        if len(Wump_Spots)==2:
            self.__numberOfWumpus-=1
            if self.__numberOfWumpus < 1:
                self.__found_wump = True
            self.__potential_wump_nodes = []
            self.__potential_wump_nodes.append(Wump_Spots[0])
            self.__wump_node = Wump_Spots[0]
            return
        for node in Wump_Spots:
            if node in self.__potential_wump_nodes:
                self.__numberOfWumpus-=1
                if self.__numberOfWumpus < 1:
                    self.__found_wump = True
                self.__potential_wump_nodes = []
                self.__potential_wump_nodes.append(node)
                self.__wump_node = node
                break
            else:
                self.__potential_wump_nodes.append(node)
                
        for node in self.__stench_nodes:
            if(self.stench_wump_check(node) == True):
                self.__numberOfWumpus-=1
                if self.__numberOfWumpus < 1:
                    self.__found_wump = True
                break
        if self.__found_wump and not self.__pitless_wump:
            self.__pitless_wump = True



    def stench_wump_check(self, node):

        x = node[0]
        y = node[1]
        if (x-1>=1 and y+1<=self.__y_border): #leftup
            leftup = (x-1,y+1)
            if leftup in self.__stench_nodes: 
                if((x-1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y+1)
                    return True
                elif((x, y+1) in self.__safe_tiles):
                    self.__wump_node = (x-1,y)
                    return True
        if (x-1>=1 and y-1>=1): #leftdown
            leftdown = (x-1,y-1)
            if leftdown in self.__stench_nodes: 
                if((x-1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y-1)
                    return True
                elif((x, y-1) in self.__safe_tiles):
                    self.__wump_node = (x-1,y)
                    return True
        if (x+1<=self.__x_border and y+1<=self.__y_border): #rightup
            rightup = (x+1,y+1)
            if rightup in self.__stench_nodes: 
                if((x+1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y+1)
                    return True
                elif((x, y+1) in self.__safe_tiles):
                    self.__wump_node = (x+1,y)
                    return True
        if (x+1<=self.__x_border and y-1>=1): #rightdown
            rightdown = (x+1,y-1)
            if rightdown in self.__stench_nodes: 
                if((x+1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y-1)
                    return True
                elif((x, y-1) in self.__safe_tiles):
                    self.__wump_node = (x+1,y)
                    return True
        
        return False
    

    def __UpdateSafeStench(self):
        for node in self.__stench_nodes:
            if node not in self.__breeze_nodes:
                self.__UpdateSafeTileManual(node[0],node[1])


    def __UpdateSafeTileManual(self,x_tile,y_tile):        
        if (x_tile,y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((x_tile,y_tile))
            if (x_tile,y_tile) in self.__potential_wump_nodes:
                self.__potential_wump_nodes.remove((x_tile,y_tile))
            if (x_tile,y_tile) in self.__potential_pit_nodes:
                self.__potential_pit_nodes.remove((x_tile,y_tile))
        if x_tile-1>=1: #Left
            if (x_tile-1,y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile-1,y_tile))
                if (x_tile-1,y_tile) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile-1,y_tile))
                if (x_tile-1,y_tile) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile-1,y_tile))
        if x_tile+1<=self.__x_border: #Right
            if (x_tile+1,y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile+1,y_tile))
                if (x_tile+1,y_tile) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile+1,y_tile))
                if (x_tile+1,y_tile) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile+1,y_tile))
        if y_tile-1>=1: #Down
            if (x_tile,y_tile-1) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile,y_tile-1))
                if (x_tile,y_tile-1) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile,y_tile-1))
                if (x_tile,y_tile-1) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile,y_tile-1))
        if y_tile+1<=self.__y_border: #Up
            if (x_tile,y_tile+1) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile,y_tile+1))
                if (x_tile,y_tile+1) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile,y_tile+1))
                if (x_tile,y_tile+1) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile,y_tile+1))


    def __NodeToNode(self, potentialNode, CurrentNode):
        xValue = potentialNode.getX() - CurrentNode.getX()
        yValue = potentialNode.getY() - CurrentNode.getY()
        if (xValue,yValue) == (0,1):
            return self.__GoNorth()
        elif (xValue,yValue) == (1,0):
            return self.__GoEast()
        elif (xValue,yValue) == (0,-1):
            return self.__GoSouth()
        elif (xValue,yValue) == (-1,0):
            return self.__GoWest()
        else:
            return self.__GoNorth()
        

    def __GoNorth(self):
        if self.__dir == 'N':#N
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'E':#E
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':#S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':#W
            self.__dir = 'N'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        

    def __GoEast(self):
        if self.__dir == 'N':#N
            self.__dir = 'E'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'E':#E
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'S':#S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':#W
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        

    def __GoSouth(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'S'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'S':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'W':
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        

    def __GoWest(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':
            self.__dir = 'W'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'W':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        

    def __optimal_home_path(self,x,y, x_target,y_target):
        '''Returns Optimal Path'''
        if (x_target==1 and y_target==1):
            def heuristic(node):
                # Simple Manhattan distance as the heuristic
                return abs(node[0] - x_target) + abs(node[1] - y_target)

            def get_neighbors(node):
                x, y = node
                neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                return [(x, y) for x, y in neighbors if (x, y) in self.__tile_history]

            open_set = [(x, y)]
            came_from = {}
            g_score = {node: float('inf') for node in self.__tile_history}
            g_score[(x, y)] = 0

            while open_set:
                current = min(open_set, key=lambda node: g_score[node] + heuristic(node))
                if current == (x_target, y_target):
                    path = [current]
                    while current in came_from:
                        current = came_from[current]
                        path.append(current)
                    path.reverse()
                    return path

                open_set.remove(current)
                for neighbor in get_neighbors(current):
                    tentative_g_score = g_score[current] + 1  # Assuming each move has a cost of 1
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        if neighbor not in open_set:
                            open_set.append(neighbor)


        else:
            Path = self.__potential_path(x,y,[], x_target,y_target, 0)
            print("Path to (", x_target, y_target, "): ")
            print(Path)
            if Path[-1][0] != x_target or Path[-1][1] != y_target:
                self.__dest_node = (Path[-1][0],Path[-1][1])
            return Path

