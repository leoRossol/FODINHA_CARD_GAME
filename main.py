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

def draw_bet_input(surface, font, bet_value):
    draw_text(surface, f"Faz quantas? {bet_value}", (50,500), font, (255,255,255))


def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("fodinha dos krias")
    font = pygame.font.SysFont(None, 26)

    game = Game(['Player1', 'Player2', 'Player3', 'Player4'])
    game.start_new_round()

    selected_card= None
    bet_value = 0
    input_mode = 'bet'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and game.state == 'betting':
                if event.key == pygame.K_UP:
                    bet_value += 1
                elif event.key == pygame.K_DOWN and bet_value>0:
                    bet_value -= 1
                elif event.key == pygame.K_RETURN:
                    idx = game.get_current_player()
                    if game.set_bet(idx, bet_value):
                        bet_value = 0

            elif event.type == pygame.MOUSEBUTTONDOWN and game.state == 'playing':
                mx, my = pygame.mouse.get_pos()
                hand_y = 430
                hand_x = 50
                for i, card in enumerate(game.players[0].hand):
                    rect = pygame.Rect(hand_x, hand_y + i*30, 120, 28)
                    if rect.collidepoint(mx, my):
                        result = game.play_card(0, i)
                        break

            elif event.type == pygame.KEYDOWN and game.state == 'round_end':
                if event.key == pygame.K_SPACE:
                    if not game.is_game_over():
                        game.next_round()
                    else:
                        running = False

        win.fill((0,120,0))

        # Draw all players
        for idx, player in enumerate(game.players):
            x = 50 + idx * 180
            y = 400 if idx == 0 else 50
            draw_text(win, f"{player.name} (Score: {player.score})", (x, y), font)
            if idx == 0:
                draw_player_hand(win, player, (x, y + 30), font)
            else:
                draw_player_hand(win, player, (x, y + 30), font)

        #DRAW PHASE-SPECIFIC UI
        if game.state == 'betting':
            draw_bet_input(win, font, bet_value)
            draw_text(win, f"Faz quantas {game.get_current_player()+1} ?", (50,470), font, (255,255,0))

        elif game.state == 'playing':
            draw_text(win, f"{game.get_current_player()+1} jogando!", (50,470), font, (0,255,0))

        elif game.state == 'round_end':
            draw_text(win, f"Fim do round! Aperte SPACE para continuar", (50,470), font, (0,255,0))

        elif game.is_game_over():
            draw_text(win, "Fim de jogo!", (50,470), font, (255,0,0))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()