from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
import math

class MinimaxConnect4Player(Connect4Player):
    def __init__(self, name, depth=4):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: Connect4State):
        best_action = None
        best_value = -math.inf

        for action in state.get_possible_actions():
            if state.validate_action(action):
                simulated_state = state.clone()
                simulated_state.update(action)
                if simulated_state.is_finished():  # Check if the move is a winning move
                    return action
                value = self.minimax(simulated_state, self.depth - 1, False)
                if value > best_value:
                    best_value = value
                    best_action = action

        if best_action is None:
            raise Exception("No valid actions available")
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
                    if simulated_state.is_finished():  # Immediate evaluation for winning moves
                        return math.inf  # Assign infinity score for a guaranteed win
                    evaluator = self.minimax(simulated_state, depth - 1, False)
                    max_eval = max(max_eval, evaluator)
            return max_eval
        else:
            min_eval = math.inf
            for action in state.get_possible_actions():
                if state.validate_action(action):
                    simulated_state = state.clone()
                    simulated_state.update(action)
                    if simulated_state.is_finished():  # Immediate evaluation for losing moves
                        return -math.inf  # Assign negative infinity to avoid losing
                    evaluator = self.minimax(simulated_state, depth - 1, True)
                    min_eval = min(min_eval, evaluator)
            return min_eval

    def evaluate(self, state):
        if state.is_finished():
            if state.get_winner() == state.get_acting_player():
                return math.inf  # Huge positive value for a win
            else:
                return -math.inf  # Huge negative value for a loss

        score = 0
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        my_symbol = state.get_acting_player()
        opponent_symbol = 1 - my_symbol

        def within_bounds(row, col):
            return 0 <= row < num_rows and 0 <= col < num_cols

        def check_direction(row, col, d_row, d_col, symbol):
            length = 1
            for i in range(1, 4):
                new_row, new_col = row + d_row * i, col + d_col * i
                if within_bounds(new_row, new_col) and grid[new_row][new_col] == symbol:
                    length += 1
                else:
                    break

            for i in range(1, 4):
                new_row, new_col = row - d_row * i, col - d_col * i
                if within_bounds(new_row, new_col) and grid[new_row][new_col] == symbol:
                    length += 1
                else:
                    break
            return length

        for row in range(num_rows):
            for col in range(num_cols):
                current_symbol = grid[row][col]
                if current_symbol == my_symbol:
                    for d_row, d_col in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        if check_direction(row, col, d_row, d_col, my_symbol) >= 3:
                            score += 100  # Prioritize near-wins

                elif current_symbol == opponent_symbol:
                    for d_row, d_col in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        if check_direction(row, col, d_row, d_col, opponent_symbol) >= 3:
                            score -= 100  # Block opponent near-wins

        return score




    def event_action(self, pos: int, action, new_state):
        # Optional: Implement any special logic when an action is taken
        pass

    def event_end_game(self, final_state):
        # Optional: Implement any cleanup or final messages here
        pass
