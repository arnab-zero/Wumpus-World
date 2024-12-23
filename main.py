from WumpusWorld import WumpusWorld
import time
from UserInterface import *

def main(wrld_file=None):
    world = WumpusWorld(True, file=wrld_file)
    score = world.run(screen)
    print("Your agent scored: " + str(score))
    show_msg_up("Game Over !!!", screen, color=BLUE)
    show_msg_down("Score: " + str(score), screen, color=YELLOW)
    time.sleep(5)
    game()

screen = board_graphics_init()
pygame.display.set_caption("Wumpus Game World !!!")

def game():
    screen.fill((90, 90, 90)) 
    choice = mainMenu(screen)
    if choice == 1:
        screen.fill((50, 50, 50))
        main()
    elif choice == 2:
        with open("GameFiles/gameFile.txt", "r") as file:
            screen.fill((50, 50, 50))
            main(file)
    elif choice == 3:
        pygame.quit()

game()
You sent
Okk

