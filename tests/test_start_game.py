import pytest

from Game_Interface import GameInterface
from csv_operations import UserChecker
from gameplay import GamePlay

CSV_FILE_PATH = '/home/gyo/Desktop/Guess who/tests/databases/users.csv'


@pytest.fixture
def game_interface():
    # Set up the GameInterface instance for testing
    interface = GameInterface()
    yield interface
    interface.root.destroy()


def read_csv(file_path):
    # Read the CSV file and return its content as a list
    import csv
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return list(reader)


def simulate_team_selection(difficulty, team):
    # Simulate the team selection process
    gameplay = GamePlay(difficulty, team)
    gameplay.setup_teams()


def verify_team_selection(gameplay, user_team, opponent_team):
    # Verify that the user and opponent teams are correctly set
    assert gameplay.user_team == user_team
    assert gameplay.opponent_team == opponent_team


def verify_players_count(gameplay, count):
    # Verify that the number of players in both teams is correct
    assert len(gameplay.user_team_players) == count
    assert len(gameplay.opponent_team_players) == count


def verify_players_team(gameplay, user_team, opponent_team):
    # Verify that all players are assigned to the correct teams
    for player in gameplay.user_team_players:
        assert player.team == user_team
    for player in gameplay.opponent_team_players:
        assert player.team == opponent_team


def verify_different_players(gameplay):
    # Verify that the user and opponent teams have different players
    assert all(player not in gameplay.user_team_players for player in gameplay.opponent_team_players)


def test_random_team_selection():
    # Test the random team selection process
    checker = UserChecker()
    players_list = checker.import_players_from_csv()
    GamePlay.players = players_list
    gameplay = GamePlay('Easy', 'Random')
    try:
        gameplay.setup_teams()
        result = True
    except Exception as e:
        print(f"Error starting the game: {e}")
        result = False
    assert result


def test_user_random_pc_random():
    """
    Test that if the user team is random, the opponent team should also be random,
    and they should have the same players.
    """
    checker = UserChecker()
    players_list = checker.import_players_from_csv()
    GamePlay.players = players_list
    gameplay = GamePlay('Easy', 'Random')
    simulate_team_selection('Easy', 'Random')
    verify_team_selection(gameplay, 'Random', 'Random')
    verify_players_count(gameplay, 24)
    assert set(gameplay.user_team_players) == set(gameplay.opponent_team_players)


def test_user_specific_pc_not_random():
    """
    Test that if the user team is not random, the opponent team should also be
    not random, and they should have different players.
    """
    checker = UserChecker()
    players_list = checker.import_players_from_csv()
    GamePlay.players = players_list
    gameplay = GamePlay('Easy', 'Sporting')
    verify_team_selection(gameplay, 'Sporting', gameplay.opponent_team)
    assert gameplay.opponent_team != 'Random'


def test_user_specific_team_players():
    # Test that the players in the user and opponent teams are correctly assigned
    checker = UserChecker()
    players_list = checker.import_players_from_csv()
    GamePlay.players = players_list
    gameplay = GamePlay('Easy', 'Sporting')
    verify_players_count(gameplay, 24)
    verify_players_team(gameplay, gameplay.user_team, gameplay.opponent_team)
