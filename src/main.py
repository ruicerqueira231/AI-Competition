import argparse
import itertools
from collections import namedtuple, defaultdict

from constants import AVAILABLE_GAME_TYPES, AVAILABLE_PLAYER_TYPES

def run_simulation(game_settings):
    removed_players = []

    while len(game_settings['players']) > 1:
        # Initialize score tracking
        scores = defaultdict(int)

        # Iterate over all pairs of players
        for player1, player2 in itertools.combinations(game_settings['players'], 2):
            # Create a simulator with both players as an array
            simulator = game_settings['game']([player1, player2])

            iteration = 0

            while True:
                iteration += 1
                print(f"Iteration {iteration}: {player1.get_name()} VS {player2.get_name()}")
                simulator.run_simulation()
                if game_settings['seat_permutation']:
                    simulator.change_player_positions()
                    print(f"Iteration {iteration}: {player2.get_name()} VS {player1.get_name()}")
                    simulator.run_simulation()

                update_scores(scores, simulator)

                if iteration >= game_settings['num_iterations'] and not check_draw(simulator):
                    break

            simulator.print_stats()

            # Update global scores for each player after all iterations
            update_scores(scores, simulator)

            # Print stats for this pair of players
            simulator.print_stats()

        # Print the leaderboard before removing a player
        print_leaderboard(scores)

        # Remove the player with the lowest score
        removed_player = remove_worst_player(game_settings['players'], scores)
        removed_players.append(removed_player)

        # Reset scores for the next round
        scores.clear()

    last_remaining_player = game_settings['players'][0]
    removed_players.insert(0, last_remaining_player)
    print_final_leaderboard(removed_players)

def check_draw(simulator):
    global_scores = simulator.get_global_score()
    # Assuming there are only two players in each game
    player_scores = list(global_scores.values())
    if len(player_scores) == 2 and player_scores[0] == player_scores[1]:
        return True  # It's a draw
    return False  # Not a draw

def update_scores(scores, simulator):
    # Update global scores for each player
    global_scores = simulator.get_global_score()
    for player_name, score in global_scores.items():
        scores[player_name] += score

def remove_worst_player(players, scores):
    # Find the player with the lowest score
    lowest_score_player = min(players, key=lambda player: scores[player.get_name()])
    players.remove(lowest_score_player)
    return lowest_score_player

def print_leaderboard(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\n" + "=" * 40)
    print("{:^40}".format("Leaderboard"))
    print("=" * 40)
    for position, (player_name, score) in enumerate(sorted_scores, start=1):
        print("{:2}. {:<30} {:>5}".format(position, player_name, score))
    print("=" * 40 + "\n")

def print_final_leaderboard(removed_players):
    print("\n" + "=" * 40)
    print("{:^40}".format("Final Leaderboard"))
    print("=" * 40)
    for position, player in enumerate(removed_players, start=1):
        print("{:2}. {:<30}".format(position, player.get_name()))
    print("=" * 40 + "\n")

def main():
    # Define a namedtuple for a Player
    Player = namedtuple('Player', ['name', 'type'])

    parser = argparse.ArgumentParser(description='Simulate a game with various settings.')

    # Mandatory game type argument
    parser.add_argument('--game', required=True, choices=AVAILABLE_GAME_TYPES.keys(),
                        help='Type of game to simulate. Choices are game1, game2, game3.')

    # Seat permutation (default: True)
    parser.add_argument('--seat-permutation', action='store_true', default=True,
                        help='Permute seats during the simulation. Defaults to True.')

    # Number of iterations (default: 1)
    parser.add_argument('--num-iterations', type=int, default=1,
                        help='Number of iterations in the simulation. Defaults to 1.')

    # Player argument. This should be specified at least twice.
    parser.add_argument('--player', action='append', nargs=2, metavar=('NAME', 'TYPE'),
                        help='Add a player with a name and type. Requires two values. This option should be specified at least twice.')

    args = parser.parse_args()

    # Check if at least two players are provided
    if args.player is None or len(args.player) < 2:
        parser.error('At least two --player arguments are required.')

    try:
        # Retrieve available player types for the selected game
        available_player_types = AVAILABLE_PLAYER_TYPES[args.game]
    except KeyError:
        parser.error(f"No player types available for the game '{args.game}'.")

    players = []
    for name, type_name in args.player:
        # Find the player class that matches the provided type name
        player_class = None
        for cls in available_player_types:
            if cls.__name__ == type_name:
                player_class = cls
                break

        if player_class is None:
            parser.error(f"Player type '{type_name}' is not available for game '{args.game}'.")

        # Create a new player instance
        players.append(player_class(name))

    # Your logic to build the object with these arguments
    game_settings = {
        'game': AVAILABLE_GAME_TYPES[args.game],
        'seat_permutation': args.seat_permutation,
        'num_iterations': args.num_iterations,
        'players': players
    }

    run_simulation(game_settings)

if __name__ == '__main__':
    main()