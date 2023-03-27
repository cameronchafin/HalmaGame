import pygame.draw

from halma.constants import *


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0

    def calc_pos(self):
        """
        Calculates the piece's x and y positions based on its row and column.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def move(self, row, col):
        """
        Moves the piece to the specified row and column.

        Parameters:
            row (int): The row to move the piece to.
            col (int): The column to move the piece to.
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win):
        """
         Draws the piece on the given window.

         Parameters:
             win (pygame.Surface): The window surface to draw on.
         """
        radius = SQUARE_SIZE//2 - PADDING

        # Draw outline
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + OUTLINE)

        # Draw circle
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def __repr__(self):
        """
        Returns a string representation of the piece's color.

        Returns:
            str: The string representation of the piece's color.
        """
        return str(self.color)
