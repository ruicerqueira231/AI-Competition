from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.state import HLPokerState
from random import choice

from games.state import State


class RandomHLPokerPlayer(HLPokerPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: HLPokerState):
        return choice(state.get_possible_actions())

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
