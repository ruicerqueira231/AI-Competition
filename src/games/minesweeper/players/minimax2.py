from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from random import choice
from games.state import State
import random

class Minimax2MinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name, depth=3):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: MinesweeperState):
        _, action = self.minimax(state, self.depth, True, float('-inf'), float('inf'))
        return action

    def minimax(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.is_finished():
            return self.evaluate(state), None

        best_action = None
        if maximizing_player:
            max_eval = float('-inf')
            for action in state.get_possible_actions():
                if state.validate_action(action):
                    new_state = state.clone()
                    new_state.update(action)
                    eval = self.minimax(new_state, depth - 1, False, alpha, beta)[0]
                    if eval > max_eval:
                        max_eval = eval
                        best_action = action
                        alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_action
        else:
            min_eval = float('inf')
            for action in state.get_possible_actions():
                if state.validate_action(action):
                    new_state = state.clone()
                    new_state.update(action)
                    eval = self.minimax(new_state, depth - 1, True, alpha, beta)[0]
                    if eval < min_eval:
                        min_eval = eval
                        best_action = action
                        beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_action

    def evaluate(self, state: MinesweeperState):
        score = 0
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()

        for row in range(num_rows):
            for col in range(num_cols):
                cell = grid[row][col]
                if cell == MinesweeperState.MINE_CELL:
                    score -= 100  # Heavy penalty for hitting a mine
                elif cell >= 0:
                    score += 10  # Increment score for each safe cell revealed
                    # Decrease score based on the risk of adjacent cells having mines
                    score -= self.calculate_adjacent_risk(grid, row, col, num_rows, num_cols)

        return score

    def calculate_adjacent_risk(self, grid, row, col, num_rows, num_cols):
        risk_score = 0
        if grid[row][col] > 0:
            for r in range(max(0, row - 1), min(row + 2, num_rows)):
                for c in range(max(0, col - 1), min(col + 2, num_cols)):
                    if grid[r][c] == MinesweeperState.EMPTY_CELL:
                        # Assume higher risk for simplicity; real implementation would use a probabilistic model
                        risk_score += 5
        return risk_score

    def event_end_game(self, final_state: State):
        # ignore
        pass

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_result(self, pos: int, result: int):
        # ignore
        pass