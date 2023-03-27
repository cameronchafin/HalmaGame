import pygame
from halma.constants import *


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None

    def draw_board(self, win):
        """
        Draw the checkerboard pattern on the given window.

        Parameters:
            win (pygame.Surface): the surface of the window to draw on.
        """
        # Fill window with dark color
        win.fill(DARK)

        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # Draw light squares
                pygame.draw.rect(win, LIGHT, (
                    row * SQUARE_SIZE,
                    col * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                ))
