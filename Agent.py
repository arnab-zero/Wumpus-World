from abc import ABCMeta, abstractmethod
from enum import Enum

class Agent ( metaclass=ABCMeta ):
    
    class Action ( Enum ):
        TURN_LEFT  = 1
        TURN_RIGHT = 2
        FORWARD    = 3
        SHOOT      = 4
        GRAB       = 5
        CLIMB      = 6

    @abstractmethod
    def decideAction ( self, stench, breeze, glitter, bump, scream):
        pass
