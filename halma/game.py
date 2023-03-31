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
        self.draw_valid_moves(self.valid_moves)
        self.draw_selected(self.selected)
        pygame.display.update()

    def _init(self):
        """
        Initialize the game variables
        """
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = []

    def get_board(self):
        """
        Returns the current board state as a 2D list.
        """
        return self.board

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

    def draw_selected(self, selected):
        """
        Draws a circle on the board around the selected piece

        Parameters:
            selected (Piece): The selected piece object.

        Returns:
            None
        """

        if self.selected:
            pygame.draw.circle(self.win, LIGHT_GREEN, (selected.x, selected.y), 47, 10)

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

    def draw_valid_moves(self, moves):
        """
        Draw circles on board to represent the valid moves for the selected piece.

        Parameters:
            moves (dict): A dictionary of valid moves for the selected piece.

        Returns:
            None
        """

        # loop through each valid move and draw a blue circle on the board to represent it
        for move in moves:
            row, col = move

            # the circle is centered at the middle of the square and has a radius of 15 pixels
            pygame.draw.circle(
                self.win,
                EMERALD,
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                15
            )

    def ai_move(self, board):
        """Updates the game board with the AI's move and switches the turn to the user's.

        Parameters:
            board (Board): The new board state after the AI's move.
        """
        self.board = board
        self.change_turn()

    def change_turn(self):
        """
        Changes the turn to the other player and clears the valid_moves dictionary.
        """

        # clear the list of valid moves for the previous player
        self.valid_moves = []

        # clear the selected piece for the previous player
        self.selected = None

        # change the turn to the other player and increment turns counter
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def winner(self):
        """
        Determine the winner of the game
        """
        return self.board.winner()

