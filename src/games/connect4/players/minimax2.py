from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
import math

class AdvancedMinimaxConnect4Player(Connect4Player):
    def __init__(self, name, depth=5):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: Connect4State):
        possible_actions = state.get_possible_actions()
        if not possible_actions:
            return Connect4Action(-1)

        best_action = possible_actions[0]
        alpha = -math.inf
        beta = math.inf

        for action in possible_actions:
            if state.validate_action(action):
                simulated_state = state.clone()
                simulated_state.update(action)
                value = self.minimax(simulated_state, self.depth - 1, False, alpha, beta)
                if value > alpha:
                    alpha = value
                    best_action = action

        return best_action

    def minimax(self, state, depth, is_maximizing_player, alpha, beta):
        if depth == 0 or state.is_finished():
            return self.evaluate(state)

        if is_maximizing_player:
            max_eval = -math.inf
            for action in state.get_possible_actions():
                simulated_state = state.clone()
                simulated_state.update(action)
                eval = self.minimax(simulated_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for action in state.get_possible_actions():
                simulated_state = state.clone()
                simulated_state.update(action)
                eval = self.minimax(simulated_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def check_winner(self, grid, player):
        num_rows = len(grid)
        num_cols = len(grid[0])

        # Check horizontal locations for win
        for c in range(num_cols-3):
            for r in range(num_rows):
                if grid[r][c] == player and grid[r][c+1] == player and grid[r][c+2] == player and grid[r][c+3] == player:
                    return True

        # Check vertical locations for win
        for c in range(num_cols):
            for r in range(num_rows-3):
                if grid[r][c] == player and grid[r+1][c] == player and grid[r+2][c] == player and grid[r+3][c] == player:
                    return True

        # Check positively sloped diaganols
        for c in range(num_cols-3):
            for r in range(3, num_rows):
                if grid[r][c] == player and grid[r-1][c+1] == player and grid[r-2][c+2] == player and grid[r-3][c+3] == player:
                    return True

        # Check negatively sloped diaganols
        for c in range(num_cols-3):
            for r in range(num_rows-3):
                if grid[r][c] == player and grid[r+1][c+1] == player and grid[r+2][c+2] == player and grid[r+3][c+3] == player:
                    return True

        return False

    def evaluate(self, state):
        grid = state.get_grid()
        current_player = state.get_acting_player()
        last_player = 1 if current_player == 0 else 0  # Toggle to find the last player

        if state.is_finished():
            if self.check_winner(grid, last_player):
                return math.inf if last_player == state.get_acting_player() else -math.inf
            else:
                return 0  # Handle draw or game still ongoing with no more moves

        score = 0
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()

        my_symbol = current_player
        opponent_symbol = 1 - my_symbol

        # Scoring settings for potential and immediate threats
        three_in_a_row = 100
        two_in_a_row = 10
        block_opponent_three = 80  # High value for blocking an opponent's three in a row

        # Helper function to count in-line discs
        def count_line(row, col, d_row, d_col, symbol):
            count = 0
            for i in range(4):
                if 0 <= row + d_row * i < num_rows and 0 <= col + d_col * i < num_cols:
                    if grid[row + d_row * i][col + d_col * i] == symbol:
                        count += 1
                    elif grid[row + d_row * i][col + d_col * i] != Connect4State.EMPTY_CELL:
                        return 0  # Blockage in the line
            return count

        # Check all possible directions
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Horizontal, Vertical, Diagonal-right, Diagonal-left

        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == Connect4State.EMPTY_CELL:
                    # Evaluate potential for 'my_symbol'
                    for d_row, d_col in directions:
                        if count_line(row, col, d_row, d_col, my_symbol) == 3:
                            score += three_in_a_row
                        if count_line(row, col, d_row, d_col, my_symbol) == 2:
                            score += two_in_a_row

                    # Evaluate blocking opponent's potential wins
                    for d_row, d_col in directions:
                        if count_line(row, col, d_row, d_col, opponent_symbol) == 3:
                            score += block_opponent_three

        return score



    def event_action(self, pos: int, action, new_state):
        # Optional: Implement any special logic when an action is taken
        pass

    def event_end_game(self, final_state):
        # Optional: Implement any cleanup or final messages here
        pass