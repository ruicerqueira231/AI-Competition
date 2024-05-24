from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from random import choice
from games.state import State
import random

class MinimaxMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name, depth=3):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: MinesweeperState):
        # Start the Minimax algorithm and return the best action
        _, action = self.minimax(state, self.depth, True, float('-inf'), float('inf'))
        return action

    def minimax(self, state, depth, maximizing_player, alpha, beta):
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
                if grid[row][col] == MinesweeperState.MINE_CELL:
                    score -= 100
                elif grid[row][col] >= 0:
                    score += 10
                    score += self.complex_safety_assessment(grid, row, col, num_rows, num_cols)

        return score


    def complex_safety_assessment(self, grid, row, col, num_rows, num_cols):
        safety_score = 0
        if grid[row][col] > 0:
            hidden_cells = 0
            flagged_mines = 0
            for r in range(max(0, row - 1), min(row + 2, num_rows)):
                for c in range(max(0, col - 1), min(col + 2, num_cols)):
                    if grid[r][c] == MinesweeperState.EMPTY_CELL:
                        hidden_cells += 1
                    elif grid[r][c] == MinesweeperState.MINE_CELL:
                        flagged_mines += 1

            # Heuristic: If the number of hidden cells is equal to the number of mines minus flagged mines, increase safety score
            if hidden_cells == (grid[row][col] - flagged_mines):
                safety_score += hidden_cells * 5

            if self.is_on_frontier(grid, row, col, num_rows, num_cols):
                safety_score += 10  # Higher score for frontier cells which can open up new areas

        return safety_score

    def is_on_frontier(self, grid, row, col, num_rows, num_cols):
        """ Determine if a cell is on the frontier between revealed and unrevealed cells """
        if grid[row][col] == MinesweeperState.EMPTY_CELL:
            return False
        for r in range(max(0, row - 1), min(row + 2, num_rows)):
            for c in range(max(0, col - 1), min(col + 2, num_cols)):
                if grid[r][c] == MinesweeperState.EMPTY_CELL:
                    return True
        return False

    def adjacent_safe_count(self, grid, row, col, num_rows, num_cols):
        count = 0
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if grid[r][c] == MinesweeperState.EMPTY_CELL:
                    count += 1
        return count

    def event_end_game(self, final_state: State):
        # ignore
        pass

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_result(self, pos: int, result: int):
        # ignore
        pass