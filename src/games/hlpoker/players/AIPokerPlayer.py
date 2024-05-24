from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.action import HLPokerAction
from games.hlpoker.state import HLPokerState
from games.hlpoker.round import Round
from phevaluator.evaluator import evaluate_cards
from random import choice


class SmartHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        possible_actions = state.get_possible_actions()
        if not possible_actions:
            return HLPokerAction.FOLD

        if len(private_cards) + len(board_cards) < 5:
            return choice(possible_actions)

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

    def preflop_strategy(self, hand_strength, possible_actions):
        if hand_strength > 1000:
            return choice([action for action in possible_actions if action != HLPokerAction.FOLD])
        return choice(possible_actions)

    def postflop_strategy(self, hand_strength, state, possible_actions):
        pot_odds = state.get_pot() / (state.get_spent(state.get_acting_player()) + 1)
        if hand_strength / pot_odds > 1.5:
            return choice([action for action in possible_actions if action != HLPokerAction.FOLD])
        return choice(possible_actions)

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
