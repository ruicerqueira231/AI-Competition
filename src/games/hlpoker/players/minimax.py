from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State
from phevaluator import evaluate_cards


class MinimaxHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)

    def minimax(self, state, depth, isMaximizingPlayer):
        print(f"Entering Minimax: Depth={depth}, IsMaximizing={isMaximizingPlayer}, Finished={state.is_finished()}")
        if depth == 0 or state.is_finished():
            eval_state = self.evaluate_state(state)
            print(f"Base Case Reached: Evaluation={eval_state}")
            return eval_state

        if isMaximizingPlayer:
            bestVal = -float('inf')
            for action in state.get_possible_actions():
                cloned_state = state.clone()
                updated_state = cloned_state.update(action)
                print(f"Maximizing: Action={action}, Before Update Finished={cloned_state.is_finished()}")
                value = self.minimax(updated_state, depth - 1, False)
                bestVal = max(bestVal, value)
            return bestVal
        else:
            bestVal = float('inf')
            for action in state.get_possible_actions():
                cloned_state = state.clone()
                updated_state = cloned_state.update(action)
                print(f"Minimizing: Action={action}, Before Update Finished={cloned_state.is_finished()}")
                value = self.minimax(updated_state, depth - 1, True)
                bestVal = min(bestVal, value)
            return bestVal

    def get_action_with_cards(self, state, private_cards, board_cards):
        bestAction = None
        bestValue = -float('inf')
        for action in state.get_possible_actions():
            cloned_state = state.clone()
            updated_state = cloned_state.update(action)
            if updated_state:
                value = self.minimax(updated_state, 3, False)
                if value > bestValue:
                    bestValue = value
                    bestAction = action
        return bestAction

    def evaluate_state(self, state: HLPokerState):
        if state.is_finished():
            return state.get_result(self.get_current_pos())

        full_hand = self.get_private_cards() + state.get_board_cards()
        hand_score = self.evaluate_hand(full_hand)

        # Calculate pot odds
        current_bet = state.get_spent(self.get_current_pos())
        pot = state.get_pot()
        pot_odds = (pot + current_bet) / current_bet if current_bet else float('inf')

        return hand_score * pot_odds

    def evaluate_hand(self, cards):

        card_ranks = [card.__str__() for card in cards]
        hand_rank = evaluate_cards(*card_ranks)
        return hand_rank

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        pass

    def event_new_game(self):
        pass

    def event_end_game(self, final_state):
        pass

    def event_result(self, pos, result):
        pass

    def event_new_round(self, round):
        pass
