# Author: YUL
# Date: 09/18/2020
# Description: The driver.
# The initial class GessGame is imported and inherited by class GessGame_Pygame that's created specifically for this project without any modifications. 

from GessGame_Pygame import GessGame_Pygame
from constants import *
import pygame

def main():  

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gess Game")
    game = GessGame_Pygame()
    game.pygame_board(window)
    pygame.display.update()

    run = True
    from_position = ""
    to_position = ""

    while run:
        if game.get_game_state() == "UNFINISHED": 
            game.draw_text(window, game.get_turn(), 100, 40, 32, PINK)
            if not from_position:
                instruction = "Select a piece"
            else:
                instruction = "Select destination"
            game.draw_text(window, instruction, WIDTH/2, 50, 32, PINK)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # when a mouse click occures, if the from_position is not yet filled, fill it
            elif event.type == pygame.MOUSEBUTTONDOWN and not from_position:
                pos = pygame.mouse.get_pos()
                from_position = game.process_click(pos) # will be "" if clicked off boundary
                game.pygame_board(window)
                game.highlight_piece(window, pos)
                pygame.display.update()

            # when a mouse click occures, if the from_position already yet filled, fill the to_position
            elif event.type == pygame.MOUSEBUTTONDOWN and from_position:
                pos = pygame.mouse.get_pos()
                to_position = game.process_click(pos)

                # when both positions are filled and they are not the same, call make_move() method
                if from_position and to_position and from_position != to_position:
                    game.make_move(from_position, to_position)
                    game.pygame_board(window)
                    pygame.display.update()

                    # reset to empty
                    from_position = ""
                    to_position = ""

                    # some one won or resigned
                    if game.get_game_state() != "UNFINISHED":
                        game.pygame_board(window)
                        pygame.display.update()
                        if game.get_game_state() == "BLACK_WON":
                            text = "BLACK WON"
                        else:
                            text = "WHITE WON"
                        game.draw_text(window, text, WIDTH/2, HEIGHT/2, 64, YELLOW)
                        game.draw_text(window, "Press any key to start a new game", WIDTH/2, 50, 32, PINK)
                        pygame.display.update()

                        # player can start a new game
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    run = False
                                    waiting = False
                                elif event.type == pygame.KEYUP:
                                    waiting = False
                                    game = GessGame_Pygame()
                                    game.pygame_board(window)
                                    pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()