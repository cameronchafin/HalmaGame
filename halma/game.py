import pygame
from halma.board import Board
from halma.constants import *


class Game:
    """
    The Game class represents the main game logic of the halma game.
    It initializes the game board and the game window, and handles user input
    for selecting and moving pieces on the board. It also determines the winner
    of the game and resets the game state.
    """
    def __init__(self, win):
        """
        Initialize the game.

        Parameters:
            win (pygame.Surface): The game window to draw on.

        Returns:
            None
        """
        self._init()
        self.win = win

    def update(self):
        """
        Redraw the board and update the screen
        """
        self.board.draw(self.win)
        # self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        """
        Initialize the game variables
        """
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def reset(self):
        """
        Reset the game variables
        """
        self._init()

    def select(self, row, col):
        """
        Select a piece on the board and move it if valid.

        Parameters:
            row (int): The row of the selected piece.
            col (int): The column of the selected piece.

        Returns:
            bool: True if the selection was valid and the piece was moved, False otherwise.
        """
        # If a piece has already been selected
        if self.selected:

            # Try to move the piece to the new location
            result = self._move(row, col)

            # If move is not valid, reset the selection and try again
            if not result:
                self.selected = None
                self.select(row, col)       # If not, reselect piece and attempt new move

        # If no piece has been selected yet
        else:
            piece = self.board.get_piece(row, col)

        # Check if user selects a valid piece on their turn
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True

        return False

    def _move(self, row, col):
        """
        Move the selected piece to a new location on the board.

        Parameters:
            row (int): The row of the new location.
            col (int): The column of the new location.

        Returns:
            bool: True if the move was valid and the piece was moved, False otherwise.
        """

        piece = self.board.get_piece(row, col)

        # If selected piece can be moved to new location
        if self.selected and piece == 0 and (row, col) in self.valid_moves:

            # Move the piece
            self.board.move(self.selected, row, col)

            # Switch the turn to the other player
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        """
        Changes the turn to the other player and clears the valid_moves dictionary.
        """

        # clear the dictionary of valid moves for the previous player
        self.valid_moves = {}

        # change the turn to the other player
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
