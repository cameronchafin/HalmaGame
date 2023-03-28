import pygame
from halma.constants import *
from halma.piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.create_board()

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

    def create_board(self):
        """
        Initialize the board with the correct pieces in the correct positions.
        Board is represented as a 2D array filled with piece objects and
        empty squares as 0.
        """
        # Create empty rows for the board
        for row in range(ROWS):
            self.board.append([0] * COLS)

        # Add black pieces to the top left corner
        black_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (3, 0)]
        for row, col in black_positions:
            self.board[row][col] = Piece(row, col, BLACK)

        # Add white pieces to the bottom right corner
        white_positions = [(4, 7), (5, 6), (5, 7), (6, 5), (6, 6), (6, 7), (7, 4), (7, 5), (7, 6), (7, 7)]
        for row, col in white_positions:
            self.board[row][col] = Piece(row, col, WHITE)

    def draw(self, win):
        """
        Draw the current state of the board onto the window provided.

        Parameters:
        win (pygame.Surface): The window to draw the board onto.
        """

        # Draw the background squares for the board.
        self.draw_board(win)

        # Iterate through every square on the board.
        for row in range(ROWS):
            for col in range(COLS):
                # Get the piece object located on this square.
                piece = self.board[row][col]
                if piece != 0:
                    # If there is a piece on the square, draw it.
                    piece.draw(win)

    def get_piece(self, row, col):
        """
        Returns the game piece located at the given row and column of the game board.

        Parameters:
            row (int): The row index of the game board.
            col (int): The column index of the game board.

        Returns:
            piece (Piece or int): The game piece at the specified location, or 0 if the location is empty.
        """
        return self.board[row][col]

    def move(self, piece, row, col):
        """
        Move a game piece to the specified row and column on the board.

        Parameters:
            piece (Piece): The game piece to move.
            row (int): The row to move the piece to.
            col (int): The column to move the piece to.
        """

        # Swap the positions of the pieces on the board and
        # update the piece's position attribute
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
