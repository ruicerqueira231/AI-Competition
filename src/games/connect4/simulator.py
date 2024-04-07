from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.game_simulator import GameSimulator


class Connect4Simulator(GameSimulator):

    def __init__(self, player1: Connect4Player, player2: Connect4Player, num_rows: int = 6, num_cols: int = 7):
        super(Connect4Simulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the connect4 grid
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols

    def on_init_game(self):
        return Connect4State(self.__num_rows, self.__num_cols)

    def on_before_end_game(self, state: Connect4State):
        # ignored for this simulator
        pass

    def on_end_game(self, state: Connect4State):
        # ignored for this simulator
        pass

    @staticmethod
    def get_player_type():
        return Connect4Player

    @staticmethod
    def get_state_type():
        return Connect4State

    @staticmethod
    def get_action_type():
        return Connect4Action