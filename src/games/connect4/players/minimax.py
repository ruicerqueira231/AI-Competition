from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
import math

class MinimaxConnect4Player(Connect4Player):
    def __init__(self, name, depth=4):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: Connect4State):
        possible_actions = state.get_possible_actions()
        if not possible_actions:
            print(f"{self.name} finds no valid moves. Returning a fallback action.")
            return Connect4Action(-1)  # Assume -1 is recognized as a "no move" action.

        best_action = possible_actions[0]  # Default action if none is better found
        best_value = -math.inf

        for action in possible_actions:
            if state.validate_action(action):
                simulated_state = state.clone()
                simulated_state.update(action)
                if simulated_state.is_finished():
                    return action

                value = self.minimax(simulated_state, self.depth - 1, False)
                if value > best_value:
                    best_value = value
                    best_action = action

        return best_action

    def minimax(self, state, depth, is_maximizing_player):
        if depth == 0 or state.is_finished():
            return self.evaluate(state)

        if is_maximizing_player:
            max_eval = -math.inf
            for action in state.get_possible_actions():
                if state.validate_action(action):
                    simulated_state = state.clone()
                    simulated_state.update(action)
                    if simulated_state.is_finished():
                        return math.inf
                    evaluator = self.minimax(simulated_state, depth - 1, False)
                    max_eval = max(max_eval, evaluator)
            return max_eval
        else:
            min_eval = math.inf
            for action in state.get_possible_actions():
                if state.validate_action(action):
                    simulated_state = state.clone()
                    simulated_state.update(action)
                    if simulated_state.is_finished():
                        return -math.inf
                    evaluator = self.minimax(simulated_state, depth - 1, True)
                    min_eval = min(min_eval, evaluator)
            return min_eval


    def check_winner(self, grid, player):
        num_rows = len(grid)
        num_cols = len(grid[0])

        for c in range(num_cols-3):
            for r in range(num_rows):
                if grid[r][c] == player and grid[r][c+1] == player and grid[r][c+2] == player and grid[r][c+3] == player:
                    return True

        # Check vertical locations for win
        for c in range(num_cols):
            for r in range(num_rows-3):
                if grid[r][c] == player and grid[r+1][c] == player and grid[r+2][c] == player and grid[r+3][c] == player:
                    return True

        for c in range(num_cols-3):
            for r in range(3, num_rows):
                if grid[r][c] == player and grid[r-1][c+1] == player and grid[r-2][c+2] == player and grid[r-3][c+3] == player:
                    return True

        for c in range(num_cols-3):
            for r in range(num_rows-3):
                if grid[r][c] == player and grid[r+1][c+1] == player and grid[r+2][c+2] == player and grid[r+3][c+3] == player:
                    return True

        return False

    def evaluate(self, state):
        grid = state.get_grid()
        current_player = state.get_acting_player()
        last_player = 1 if current_player == 0 else 0

        if state.is_finished():
            if self.check_winner(grid, last_player):
                return math.inf if last_player == self.get_acting_player() else -math.inf
            else:
                return 0

        score = 0
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        my_symbol = state.get_acting_player()
        opponent_symbol = 1 - my_symbol

        three_in_a_row = 100
        two_in_a_row = 10
        center_column_bonus = 20

        def count_line(row, col, d_row, d_col, symbol):
            count = 0
            for i in range(4):
                if 0 <= row + d_row * i < num_rows and 0 <= col + d_col * i < num_cols:
                    if grid[row + d_row * i][col + d_col * i] == symbol:
                        count += 1
                    elif grid[row + d_row * i][col + d_col * i] != Connect4State.EMPTY_CELL:
                        return 0
                else:
                    return 0
            return count

        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == Connect4State.EMPTY_CELL:
                    if col in [2, 3, 4]:
                        score += center_column_bonus

                    for d_row, d_col in directions:
                        player_count = count_line(row, col, d_row, d_col, my_symbol)
                        opponent_count = count_line(row, col, d_row, d_col, opponent_symbol)

                        if player_count == 3:
                            score += three_in_a_row
                        elif player_count == 2:
                            score += two_in_a_row

                        if opponent_count == 3:
                            score -= three_in_a_row * 10
                        elif opponent_count == 2:
                            score -= two_in_a_row

        return score

    def event_action(self, pos: int, action, new_state):
        # Optional: Implement any special logic when an action is taken
        pass

    def event_end_game(self, final_state):
        # Optional: Implement any cleanup or final messages here
        pass