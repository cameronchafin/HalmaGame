import pygame
from halma.constants import *
from halma.piece import Piece


class Board:
    """
    Represents a Halma board as an 8x8 grid of squares.

    Attributes:
        board (list): A 2D list representing the state of the board.
    """
    def __init__(self):
        self.board = []
        self.create_board()

    def draw_board(self, win):
        """
        Draw the checkerboard pattern on the given window.

        Parameters:
            win (pygame.Surface): the surface of the window to draw on.
        """
        # Fill window with dark color
        win.fill(DARK)

        # Fill in light spaces
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # Draw light squares
                pygame.draw.rect(win, LIGHT, (
                    row * SQUARE_SIZE,
                    col * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                ))

        # Fill in black starting zone
        for square in BLACK_START:
            pygame.draw.rect(win, (60, 60, 60), (
                square[0] * SQUARE_SIZE,
                square[1] * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            ))

        # Fill in black starting zone dark spaces
        for square in BLACK_DARK:
            pygame.draw.rect(win, (32,33,36), (
                square[0] * SQUARE_SIZE,
                square[1] * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            ))

        # Fill in white starting zone
        for square in WHITE_START:
            pygame.draw.rect(win, (214, 214, 214), (
                square[0] * SQUARE_SIZE,
                square[1] * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            ))

        # Fill in white starting zone dark spaces
        for square in WHITE_DARK:
            pygame.draw.rect(win, (158,158,158), (
                square[0] * SQUARE_SIZE,
                square[1] * SQUARE_SIZE,
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
        black_positions = [(0, 0), (0, 1), (0, 2), (0, 3),
                           (1, 0), (1, 1), (1, 2),
                           (2, 0), (2, 1),
                           (3, 0)]
        for row, col in black_positions:
            self.board[row][col] = Piece(row, col, BLACK)

        # Add white pieces to the bottom right corner
        white_positions = [(4, 7),
                           (5, 6), (5, 7),
                           (6, 5), (6, 6), (6, 7),
                           (7, 4), (7, 5), (7, 6), (7, 7)]
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

    def get_all_pieces(self, color):
        """
        Returns a list of all pieces of the given color on the board.

        Parameters:
            color (str): The color of the pieces to search for.

        Returns:
            list: A list of Piece objects of the given color.
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        """
        Move a game piece to the specified row and column on the board.

        Parameters:
            piece (Piece): The game piece to move.
            row (int): The row to move the piece to.
            col (int): The column to move the piece to.
        """

        # Swaps the positions of the pieces on the board and
        # update the piece's position attribute
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def is_valid_square(self, row, col, color):
        """
        Check if a given square is a valid square on the board.

        Parameters:
            row (int): the row number of the square.
            col (int): the column number of the square.
            color (str): the color of the player who owns the piece being moved.
        Returns:
            bool: True if the square is valid, False otherwise.
        """
        # check if row and col are within board bounds
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
            return False

        return True

    def get_valid_moves(self, piece):
        """
        Returns a list of valid moves for the given piece.

        Parameters:
            piece (Piece): the piece for which to find valid moves.

        Returns:
            A list of valid moves for the given piece. Each move is a tuple of
            the form (row, col), representing the position the piece can move to.
        """
        moves = []

        # check all eight directions for valid moves
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if drow == 0 and dcol == 0:
                    continue  # skip current position

                # check squares in current direction
                row = piece.row
                col = piece.col
                row += drow
                col += dcol

                # check if square is in bounds
                if self.is_valid_square(row, col, piece.color):
                    square = self.board[row][col]

                    # check for moves into empty adjacent squares
                    if square == 0:
                        moves.append((row, col))

                    # check for jumps over adjacent pieces
                    if square != 0:
                        next_row = row + drow
                        next_col = col + dcol

                        # check if jump is valid
                        if self.is_valid_square(next_row, next_col, piece.color) and \
                                self.board[next_row][next_col] == 0:

                            # add to moves and mark the square as visited
                            moves.append((next_row, next_col))
                            visited = [(piece.row, piece.col)]

                            # recursively check for more valid jumps from the new position
                            jumps = self.check_jumps(piece, next_row, next_col, visited)
                            if jumps:
                                moves += jumps

        return moves

    def check_jumps(self, piece, row, col, visited):
        """
        Recursively checks for valid jumps from the given starting position.

        Parameters:
            piece (Piece): the piece for which to find valid jumps.
            row (int): the row of the starting position.
            col (int): the column of the starting position.
            visited (list): a list of visited squares.

        Returns:
            A list of valid jumps for the given piece. Each jump is a tuple of the
            form (row, col), representing the position the piece can jump to.
        """
        valid_jumps = []

        # check all eight directions for valid jumps
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if drow == 0 and dcol == 0:
                    continue  # skip current position

                # check square in current direction
                next_row = row + drow
                next_col = col + dcol

                # check if there is an opponent's piece adjacent to the starting position
                if self.is_valid_square(next_row, next_col, piece.color) and self.board[next_row][next_col] != 0:

                    # check square on the other side of the opponent's piece
                    jump_row = next_row + drow
                    jump_col = next_col + dcol

                    # check if the jump is valid and the square has not already been visited
                    if (self.is_valid_square(jump_row, jump_col, piece.color) and
                            self.board[jump_row][jump_col] == 0 and (jump_row, jump_col) not in visited):

                        # add the valid jump to the list and mark the square as visited
                        valid_jumps.append((jump_row, jump_col))
                        visited.append((jump_row, jump_col))

                        # recursively check for more valid jumps from the new position
                        jumps = self.check_jumps(piece, jump_row, jump_col, visited)
                        valid_jumps += jumps

        return valid_jumps

    def evaluate(self):
        """
        Evaluates the current state of the Halma board, returning a score representing
        the relative advantage of the white player over the black player.

        The evaluation is based on three factors:
            1. Distance between each player's pieces and the opposing starting zone.
            2. Number of pieces in the opponent's starting zone.
            3. Penalty for pieces still in their starting zone.

        A positive score indicates an advantage for the white player,
        while a negative score indicates an advantage for the black player.

        Returns:
            A floating-point number representing the evaluation score.
        """
        # Distance between each player's pieces and the opposing starting zone
        black_distance = 0
        white_distance = 0
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece != 0 and piece.color == BLACK:
                    # Manhattan distance to white starting zone
                    black_distance += abs(row - 0) + abs(col - 0)
                elif piece != 0 and piece.color == WHITE:
                    # Manhattan distance to black starting zone
                    white_distance += abs(row - 7) + abs(col - 7)

        # Number of pieces in the opponent's starting zone
        black_proximity = 0
        white_proximity = 0
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece != 0 and piece.color == BLACK and (row, col) in WHITE_START:
                    black_proximity += 1
                elif piece != 0 and piece.color == WHITE and (row, col) in BLACK_START:
                    white_proximity += 1

        # Penalty for pieces still in their starting zone
        black_start_penalty = 0
        white_start_penalty = 0
        for row, col in BLACK_START:
            piece = self.get_piece(row, col)
            if piece != 0 and piece.color == BLACK:
                black_start_penalty += 1
        for row, col in WHITE_START:
            piece = self.get_piece(row, col)
            if piece != 0 and piece.color == WHITE:
                white_start_penalty += 1

        # Total evaluation with modified weights
        evaluation = 4 * (white_distance - black_distance) / 16.0 + (
                       white_proximity - black_proximity) * 2.0 - (
                       white_start_penalty - black_start_penalty) / 4.0
        return evaluation

    def winner(self):
        """
        Determine the winner of the game.

        Returns:
            None if there is no winner, "White wins" if all white pieces are in black's starting zone,
            or "Black wins" if all black pieces are in white's starting zone.
        """
        # Get all the pieces for each player
        white_pieces = self.get_all_pieces(WHITE)
        black_pieces = self.get_all_pieces(BLACK)

        # Check if all the white pieces are in black's starting zone
        white_wins = all(piece.position() in BLACK_START for piece in white_pieces)

        # Check if all the black pieces are in white's starting zone
        black_wins = all(piece.position() in WHITE_START for piece in black_pieces)

        # Return the winner, if there is one
        if white_wins and not black_wins:
            return "White wins"
        elif black_wins and not white_wins:
            return "Black wins"
        else:
            return None
