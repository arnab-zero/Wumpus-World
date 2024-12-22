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