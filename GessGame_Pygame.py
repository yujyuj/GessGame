from GessGame import GessGame
from constants import *
import pygame

class GessGame_Pygame(GessGame):
    

    def pygame_board(self, window):
        window.fill(BLACK)
        # background = pygame.image.load("background_image.png")
        # window.blit(background, (0, 0))

        radius = int(SQUARE_SIZE/3)
        for col in range(20):
            for row in range(20):
                # grid
                pygame.draw.rect(window, PURPLE, (col*SQUARE_SIZE + MARGIN, row*SQUARE_SIZE + MARGIN, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
                pygame.draw.rect(window, BLACK, (col*SQUARE_SIZE + MARGIN, row*SQUARE_SIZE + MARGIN, SQUARE_SIZE, SQUARE_SIZE), 2)

                # # stones
                if self._board[row][col] == '●':
                    pygame.draw.circle(window, BLACK, (int(col*SQUARE_SIZE + SQUARE_SIZE/2 + MARGIN), int(row*SQUARE_SIZE + int(SQUARE_SIZE/2) + MARGIN)), radius)
                elif self._board[row][col] == '○':
                    pygame.draw.circle(window, WHITE, (int(col*SQUARE_SIZE + SQUARE_SIZE/2 + MARGIN), int(row*SQUARE_SIZE + SQUARE_SIZE/2 + MARGIN)), radius - 1) # width == 0 (default) fill the circle
                    pygame.draw.circle(window, BLACK, (int(col*SQUARE_SIZE + SQUARE_SIZE/2 + MARGIN), int(row*SQUARE_SIZE + SQUARE_SIZE/2 + MARGIN)), radius, 2) # width > 0, thickness

        # render text
        x = 0
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']:
            self.draw_text(window, i, 125 + x*50, 1105, 32, WHITE) # for column
            self.draw_text(window, str(x+1), 1125, 1060-x*50, 32, WHITE) # for row
            x += 1
        
    def draw_text(self, window, text, midtop_x, midtop_y, font_size, font_color, font_style = "comicsansms"):
        """
        Takes 6 parameters and sets the image surface's midtop coordinates as the passed in midtop_x and midtop_y
        No return.
        """
        font_name = pygame.font.match_font(font_style)
        font = pygame.font.Font(font_name, font_size)
        text_as_image = font.render(text, False, font_color) # No anti-aliasesd
        text_rect = text_as_image.get_rect()
        text_rect.midtop = (midtop_x, midtop_y) # sets the image midtop coordinates as the passed in midtop_x and midtop_y
        window.blit(text_as_image, text_rect) # computer will figure out the topleft corner of the image and render from there


    def process_click(self, position):

        col_lookup_table = {
            3:'b', 4:'c', 5:'d', 6:'e', 7:'f', 8:'g', 9:'h', 10:'i', 11:'j', 12:'k', 13:'l', 14:'m', 15:'n', 16:'o', 17:'p', 18:'q', 19:'r', 20:'s'
        }

        if 150 <= position[0] <= 1050 and 150 <= position[1] <= 1050:
            col = col_lookup_table.get(position[0]//50) # use look up table to convert col to string
            row = str(22 - position[1]//50)             # use str() and simple calculation to convert row to string
            return col + row

        # return "" when click out of bound
        return ""


    def highlight_ring(self, window, win_pos):

        if 150 <= win_pos[0] <= 1050 and 150 <= win_pos[1] <= 1050:
            left = ((win_pos[0] - MARGIN)//50 + 1) * 50
            top = ((win_pos[1] - MARGIN)//50 + 1) * 50
            pygame.draw.rect(window, CYAN, (left, top, SQUARE_SIZE*3, SQUARE_SIZE*3), 5)
            return

        # simply return when click out of bound
        return


