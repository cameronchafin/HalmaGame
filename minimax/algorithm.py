from copy import deepcopy
import pygame.draw

BLACK = (0, 0, 0)  # user piece color
WHITE = (255, 255, 255)  # AI piece color


def minimax(board, depth, alpha, beta, max_player, game):
    """
    This function uses the minimax algorithm with alpha-beta pruning
    to search for the best move for the current player.

    Parameters:
        board (Board): The current state of the board.
        depth (int): The current depth of the search.
        alpha (int): The current alpha value for alpha-beta pruning.
        beta (int): The current beta value for alpha-beta pruning.
        max_player (bool): True if the current player is the maximizing player, False otherwise.
        game (Game): The current game instance.

    Returns:
        (int, Board): A tuple containing the evaluation score and the board state of the best move found.

    """

    # Check if the maximum search depth has been reached or if a winner has been found
    if depth == 0 or board.winner() is not None:
        return board.evaluate(), board

    if max_player:
        # Max player is trying to maximize the evaluation score
        max_evaluation = float("-inf")
        best_move = None
        # Loop through all valid moves for the current player and evaluate each one
        for move in get_all_moves(board, WHITE, game):
            # Evaluate the current move using the minimax function with alpha-beta pruning
            evaluation = minimax(move, depth-1, alpha, beta, False, game)[0]
            # Update the maximum evaluation score and best move if a better move is found
            if evaluation > max_evaluation:
                max_evaluation = evaluation
                best_move = move
            # Update alpha value for alpha-beta pruning
            alpha = max(alpha, evaluation)
            # If beta is less than or equal to alpha, break out of the loop
            if beta <= alpha:
                break
        return max_evaluation, best_move
    else:
        # Min player is trying to minimize the evaluation score
        min_evaluation = float("inf")
        best_move = None
        # Loop through all valid moves for the current player and evaluate each one
        for move in get_all_moves(board, BLACK, game):
            # Evaluate the current move using the minimax function with alpha-beta pruning
            evaluation = minimax(move, depth - 1, alpha, beta, True, game)[0]
            # Update the minimum evaluation score and best move if a better move is found
            if evaluation < min_evaluation:
                min_evaluation = evaluation
                best_move = move
            # Update beta value for alpha-beta pruning
            beta = min(beta, evaluation)
            # If beta is less than or equal to alpha, break out of the loop
            if beta <= alpha:
                break
        return min_evaluation, best_move


def get_all_moves(board, color, game):
    """
    Returns all possible moves for a given color on the current board.

    Parameters:
        board (Board): current game board
        color (string): color of the pieces to move (either RED or WHITE)
        game (Game): current game object

    Returns:
        list: a list of Board objects representing all possible board
        configurations after a move by the given color
    """
    moves = []

    # iterate through all pieces of the given color on the board
    for piece in board.get_all_pieces(color):
        # get all valid moves for the current piece
        valid_moves = board.get_valid_moves(piece)
        # iterate through all valid moves for the current piece
        for move in valid_moves:

            # visualize AI decision-making by drawing considered moves (optional)
            # visualize(game, board, piece)

            # create a copy of the board and the piece to simulate the move
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)

            # simulate the move on the temporary board
            new_board = simulate_move(temp_piece, move, temp_board, game)

            # add the resulting board configuration to the list of moves
            moves.append(new_board)

    return moves


def simulate_move(piece, move, board, game):
    """
    Simulates a given move on a copy of the current board.

    Args:
        piece (Piece): piece to move
        move (tuple): new position of the piece (row, col)
        board (Board): current game board
        game (Game): current game object

    Returns:
        Board: a new board configuration after the given move has been made
    """
    # move the piece to the new position on the board
    board.move(piece, move[0], move[1])

    return board


def visualize(game, board, piece):
    """
    Visualizes the minimax algorithm by drawing the current board state and highlighting the valid moves for a piece.

    Parameters:
        game (Game): the current Game object.
        board (Board): the current Board object.
        piece (Piece): the Piece object to visualize.

    Returns:
        None
    """
    # Get valid moves for the piece
    valid_moves = board.get_valid_moves(piece)

    # Draw the board and highlight the selected piece
    board.draw(game.win)
    pygame.draw.circle(game.win, (93, 187, 99), (piece.x, piece.y), 47, 10)

    # Draw circles on valid move squares
    game.draw_valid_moves(valid_moves)

    # Update the display
    pygame.display.update()

    # Wait for a short delay (optional)
    # pygame.time.delay(100)
