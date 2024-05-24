from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State
from phevaluator.evaluator import evaluate_cards


class AIHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.private_cards = []  # Initialize private cards
        self.board_cards = []    # Initialize board cards
        self.opponent_model = {}

    def event_new_game(self):
        self.opponent_model = {'folds': 0, 'calls': 0, 'raises': 0}
        self.private_cards = []  # Reset private cards at the start of a new game
        self.board_cards = []    # Reset board cards at the start of a new game

    def event_new_round(self, round):
        cards = self.private_cards + self.board_cards
        if len(cards) >= 5:
            hand_strength = self.assess_hand_strength(cards)
            print(f"Starting {round} with hand strength: {hand_strength}")
        else:
            print(f"Not enough cards to assess hand strength for {round}")

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        self.private_cards = private_cards
        self.board_cards = board_cards
        return self.choose_best_action(state, private_cards, board_cards, state.get_possible_actions())

    def choose_best_action(self, state, private_cards, board_cards, possible_actions):
        cards = private_cards + board_cards
        if len(cards) >= 5:
            hand_strength = self.assess_hand_strength(cards)
            if hand_strength > 5000:
                if HLPokerAction.RAISE in possible_actions:
                    return HLPokerAction.RAISE
                elif HLPokerAction.CALL in possible_actions:
                    return HLPokerAction.CALL
            elif hand_strength > 2000:
                if HLPokerAction.CALL in possible_actions:
                    return HLPokerAction.CALL
            return HLPokerAction.FOLD
        else:
            return HLPokerAction.FOLD 

    def assess_hand_strength(self, cards):
        if len(cards) >= 5:
            card_codes = [f"{card.rank}{card.suit}" for card in cards]
            hand_strength = evaluate_cards(*card_codes)
            return hand_strength
        else:
            return 0  # Return a default low strength value if not enough cards

    def event_my_action(self, action, new_state):
        print(f"{self.get_name()} performed {action}")

    def event_opponent_action(self, action, new_state):
        if action == HLPokerAction.FOLD:
            self.opponent_model['folds'] += 1
        elif action == HLPokerAction.CALL:
            self.opponent_model['calls'] += 1
        elif action == HLPokerAction.RAISE:
            self.opponent_model['raises'] += 1
        print(f"{self.get_name()} observed opponent performed {action}")

    def event_end_game(self, final_state: HLPokerState):
        print(f"Game ended. Final state: {final_state}")
        opponent_cards = self.get_opponent_cards()
        if opponent_cards:
            print(f"Opponent's final cards: {opponent_cards}")

    def event_result(self, pos: int, result: int):
        if pos == self.get_current_pos():
            print(f"{self.get_name()} result this game: {result}")
