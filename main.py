import pygame
import sys
from game.game import Game

def main():

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("fodinha dos krias")

    game_instance = Game(['Player1', 'Player2', 'Player3', 'Player4'])
    game_instance.start()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((0,120,0))
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()