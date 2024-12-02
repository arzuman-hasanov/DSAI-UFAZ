import random as rnd
import numpy as np
from math import inf, nan

def alpha_beta_decision(board, turn, ai_level, queue, max_player):
    
    def evaluate_line(line_values, max_player):
        # Evaluation scores for different counts of consecutive pieces.
        counts = {
            4: {max_player: 1000, 3 - max_player: -1000},
            3: {max_player: 100, 3 - max_player: -100},
            2: {max_player: 10, 3 - max_player: -10},
        }

        # Count occurrences of AI player's and opponent's pieces in the line.
        ai_count = line_values.tolist().count(max_player)
        opponent_count = line_values.tolist().count(3 - max_player)

        return counts.get(ai_count, {}).get(opponent_count, 0)
    
    def evaluate_position(board, max_player):
        winner = board.check_victory()
        
        # Assigning a positive infinity score (if player has won)
        if winner == max_player: return inf
        
        # Assigning a negative infinity score (if opponent has won)
        elif winner != 0: return -inf
    
        score = 0
        grid = board.grid
        
        # Evaluating the board for potential victories in rows, columns and diagonals
        for line in range(6): score += np.sum(evaluate_line(grid[:, line][i:i+4], max_player) for i in range(4))
        
        for column in range(7): score += np.sum(evaluate_line(grid[column, :][i:i+4], max_player) for i in range(3))

        diagonals = get_diagonals(board)
        for diagonal in diagonals: score += np.sum(evaluate_line(diagonal[i:i+4], max_player) for i in range(len(diagonal) - 3))
        return score

    def get_diagonals(board):
        grid = board.grid
        diags = []
        
        # Iterate through diagonals starting from the top-left corner.
        for i in range(grid.shape[1] - grid.shape[0] + 1):
            diags.append(grid.diagonal(offset=i))
            
        # Flip the grid and iterate through diagonals starting from the top-right corner.
        flipped_grid = np.fliplr(grid)
        for i in range(-grid.shape[0] + 1, 1):
            diags.append(flipped_grid.diagonal(offset=i))
        return diags

    
    # Minimize the value using minimax algorithm with alpha-beta
    def min_value(board, depth, alpha, beta, max_player):
        if depth == 0 or board.check_victory():
            return evaluate_position(board, max_player)
    
        value = inf
        best_move = None
        for move in ordering_moves(board):
            if not board.column_filled(move):
                # Copy the board to keep original one
                child_board = board.copy()
                child_board.add_disk(move, 3 - max_player, update_display=False)
                
                # Find the maximum value for the child board
                child_value = max_value(child_board, depth - 1, alpha, beta, max_player)
                value = min(value, child_value)
                
                # alpha-beta pruning
                if value <= alpha:
                    return value
                beta = min(beta, value)
                
                # Update the best move
                if best_move is None or child_value < value:
                    best_move = move
        return value

    # Maximize the value using the minimax algorithm with alpha-beta
    def max_value(board, depth, alpha, beta, max_player):
        
        # If we've reached the specified depth or the game is over
        if depth == 0 or board.check_victory():
            return evaluate_position(board, max_player)

        # Initialize negative infinity to find maximum achievable value
        value = -inf
        best_move = None
        
        for move in ordering_moves(board):
            if not board.column_filled(move):
                
                # Create a child board with the potential move.
                child_board = board.copy()
                child_board.add_disk(move, max_player, update_display=False)
                child_value = min_value(child_board, depth - 1, alpha, beta, max_player)
                
                # Update maximum value.
                value = max(value, child_value)
                
                # alpha-beta pruning
                if value >= beta:
                    return value
                alpha = max(alpha, value)
                
                # Update the best move
                if best_move is None or child_value > value:
                    best_move = move
        return value

    # we use this function to generate a list of available moves on the game board
    def ordering_moves(board):
        
        # Get all possible moves
        possible_moves = board.get_possible_moves()
        
        # Filter out filled columns
        unfilled_moves = [move for move in possible_moves if not board.column_filled(move)]

        # Determine the center column index
        center_column = board.grid.shape[1] // 2 

        # Sort moves based on their distance from the center column (ascending)
        unfilled_moves.sort(key=lambda move: abs(move - center_column))

        return unfilled_moves


    best_move = None
    best_value = -inf 
    alpha = -inf
    beta = inf
    
    # Iterate through ordered moves, pick the best move for potential victory,
    # and store the result in a queue.
    for move in ordering_moves(board):
        child_board = board.copy()
        child_board.add_disk(move, max_player, update_display=False)

        if child_board.check_victory():
            queue.put(move)
            return 

        value = min_value(child_board, ai_level, alpha, beta, max_player)
        
        # Update the best move and value.
        if value > best_value:
            best_value = value
            best_move = move
            alpha = max(alpha, best_value)

    queue.put(best_move)