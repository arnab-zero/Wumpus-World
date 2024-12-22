import time
from xmlrpc.client import Boolean
import pygame
import sys

B_R, B_C = 10, 10
SQUARE_LEN = 60

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
DARKSEAGREEN = (143, 188, 143)
MEDIUMSEAGREEN = (0, 250, 154)

RADIUS = 0.45*SQUARE_LEN

IMAGES = {}
def loadImage():
    pics = ["agent_down1", "agent_left1", "agent_right1", "agent_up1", "breeze", "gold", "bg", "bg1", "pit", "stench", "wumpus" , "dead_wumpus", "arrow_overlay"]
    for pic in pics:
        IMAGES[pic] = pygame.transform.scale(pygame.image.load(f"./images/{pic}.png"), (SQUARE_LEN-1, SQUARE_LEN-1))