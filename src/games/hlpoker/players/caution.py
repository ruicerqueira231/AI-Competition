from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.action import HLPokerAction
from games.hlpoker.state import HLPokerState
from games.hlpoker.round import Round
from phevaluator.evaluator import evaluate_cards
from random import choice


class CautiousHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        possible_actions = state.get_possible_actions()
        if not possible_actions:
            return HLPokerAction.FOLD

        if len(private_cards) + len(board_cards) < 5:
            return self.cautious_choice(possible_actions)

        hand_strength = self.evaluate_hand_strength(private_cards, board_cards)

        if state.get_current_round() == Round.Preflop:
            return self.preflop_strategy(hand_strength, possible_actions)
        else:
            return self.postflop_strategy(hand_strength, state, possible_actions)

    def evaluate_hand_strength(self, private_cards, board_cards):
        cards = private_cards + board_cards
        if len(cards) < 5:
            return 0

        card_strs = [f"{card.rank}{card.suit}" for card in cards]
        return evaluate_cards(*card_strs)

    def cautious_choice(self, possible_actions):
        if HLPokerAction.FOLD in possible_actions:
            return HLPokerAction.FOLD
        return choice([action for action in possible_actions if action != HLPokerAction.RAISE])

    def preflop_strategy(self, hand_strength, possible_actions):
        # Cautious preflop strategy, avoid raising
        if hand_strength > 1500:
            return HLPokerAction.CALL if HLPokerAction.CALL in possible_actions else HLPokerAction.RAISE
        return self.cautious_choice(possible_actions)

    def postflop_strategy(self, hand_strength, state, possible_actions):
        pot_odds = state.get_pot() / (state.get_spent(state.get_acting_player()) + 1)
        # Cautious postflop strategy, avoid raising unless very strong hand
        if hand_strength / pot_odds > 2.0:
            return HLPokerAction.CALL if HLPokerAction.CALL in possible_actions else HLPokerAction.RAISE
        return self.cautious_choice(possible_actions)

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        pass

    def event_new_game(self):
        pass

    def event_end_game(self, final_state):
        pass

    def event_result(self, pos: int, result: int):
        pass

    def event_new_round(self, round):
        pass
