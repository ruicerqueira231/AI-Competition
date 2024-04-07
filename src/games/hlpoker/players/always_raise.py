from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.state import HLPokerState
from games.state import State


class AlwaysRaiseHLPokerPlayer(HLPokerPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: HLPokerState):
        return HLPokerAction.RAISE

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
