import pygame
import sys
from game.game import Game


def draw_text(surface, text, pos, font, color=(255,255,255)):
    img = font.render(text, True, color)
    surface.blit(img, pos)

def draw_player_hand(surface, player, pos, font):
    for i, card in enumerate(player.hand):
        card_str = f"{card.value} of {card.suit}"
        draw_text(surface, card_str, (pos[0], pos[1] + i*30), font)


def main():

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("fodinha dos krias")
    font = pygame.font.SysFont(None, 26)

    game_instance = Game(['Player1', 'Player2', 'Player3', 'Player4'])
    game_instance.start()

    selected_card= None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                hand_y = 430
                hand_x = 50
                for i, card in enumerate(game_instance.players[0].hand):
                    rect = pygame.Rect(hand_x, hand_y + i*30, 120, 28)
                    if rect.collidepoint(mx, my):
                        selected_card=i

        win.fill((0,120,0))

        # Draw all players
        for idx, player in enumerate(game_instance.players):
            x = 50 + idx * 180
            y = 400 if idx == 0 else 50
            draw_text(win, f"{player.name} (Score: {player.score})", (x, y), font)
            if idx == 0:
                draw_player_hand(win, player, (x, y + 30), font, selected_card)
            else:
                draw_player_hand(win, player, (x, y + 30), font)

        pygame.display.update()

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()