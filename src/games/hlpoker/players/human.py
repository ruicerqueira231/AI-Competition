from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State


class HumanHLPokerPlayer(HLPokerPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: HLPokerState):
        print("------------------------------")
        self.print_state(state)
        return {
            "r":        HLPokerAction.RAISE,
            "raise":    HLPokerAction.RAISE,
            "c":        HLPokerAction.CALL,
            "call":     HLPokerAction.CALL,
            "f":        HLPokerAction.FOLD,
            "fold":     HLPokerAction.FOLD
        }.get(input(f"{self.get_name()} ({self.get_current_pos()}): Choose an action (raise/r, call/c, fold/f):"))

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        print(f">{self.get_name()}: My opponent choose to {action}")

    def event_new_game(self):
        print("--- New game ---")
        self.get_private_cards()

    def event_end_game(self, final_state: State):
        print("--- End game ---")

    def event_result(self, pos: int, result: int):
        if self.get_current_pos() == pos:
            print(f">{self.get_name()}: My score was {result}$")

    def event_new_round(self, round: Round):
        if round.value > Round.Preflop.value:
            #!WARN: Lower score is better
            print(f">{self.get_name()}: My current hand score in {round} round is {HLPokerState.evaluate_hand(self.get_private_cards() + self.get_board_cards())}")

