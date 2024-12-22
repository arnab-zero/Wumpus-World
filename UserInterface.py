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

def board_graphics_init():
    return 

def refreshBoardGraphics(board, dir, show_board, screen):
    # screen.fill((0, 0, 0))
    time.sleep(0.1)
    for c in range(B_C):
        board[c], board[B_C-c-1] = board[B_C-c-1], board[c]
    

    bg_img = IMAGES['bg']
    wump_img = IMAGES['wumpus']
    player_right = IMAGES['agent_right1']
    player_left = IMAGES['agent_left1']
    player_up = IMAGES['agent_up1']
    player_down = IMAGES['agent_down1']
    pit_img = IMAGES['pit']
    gold_img = IMAGES['gold']
    breeze_img = IMAGES['breeze']
    stench_img = IMAGES['stench']
    alt_bg_img = IMAGES['bg1']
    
    for col in range(B_C):
        for row in range(B_R):
            pos = (col*SQUARE_LEN, B_R*SQUARE_LEN - row*SQUARE_LEN+SQUARE_LEN)
            screen.blit(bg_img, pos)
            
            if board[col][row].agent:
                player_img = player_right
                if dir == 0:
                    player_img = player_right
                elif dir == 1:
                    player_img = player_down
                elif dir == 2:
                    player_img = player_left
                elif dir == 3:
                    player_img = player_up
                screen.blit(player_img, pos)
            if board[col][row].wumpus:
                screen.blit(wump_img, pos)
            if board[col][row].pit:
                screen.blit(pit_img, pos)
            if board[col][row].gold:
                screen.blit(gold_img, pos)
            if board[col][row].breeze:
                screen.blit(breeze_img, pos)
            if board[col][row].stench:
                screen.blit(stench_img, pos)
            
            if not board[col][row].visited and not show_board:
                screen.blit(alt_bg_img, pos)

                
    pygame.display.update()
    pass

def choices(screen):
    
    font = pygame.font.Font(None, 80)
    text = font.render('New Game', True, (WHITE))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, B_R*SQUARE_LEN//3))
    screen.blit(text, text_rect)
    
    text = font.render('Custom Game', True, (WHITE))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, B_R*SQUARE_LEN//3+80))
    screen.blit(text, text_rect)

    text = font.render('Exit', True, (WHITE))
    text_rect = text.get_rect(center=(B_C*SQUARE_LEN//2, B_R*SQUARE_LEN//3+160))
    screen.blit(text, text_rect)

    pygame.display.update()