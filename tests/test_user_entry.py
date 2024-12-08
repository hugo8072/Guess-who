import pytest
import csv
from unittest.mock import patch

from Game_Interface import GameInterface
from csv_operations import UserChecker

CSV_FILE_PATH = '/home/gyo/Desktop/Guess who/tests/databases/users.csv'


@pytest.fixture
def game_interface():
    # Set up the GameInterface instance for testing
    interface = GameInterface()
    yield interface
    interface.root.destroy()


def read_csv(file_path):
    # Read the CSV file and return its content as a list
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return list(reader)


def simulate_username_entry(game_interface, username):
    # Simulate the username entry process
    game_interface.show_username_entry()
    game_interface.root.update()
    game_interface.username_input.insert(0, username)
    assert game_interface.username_input.get() == username
    game_interface.username_entry_on_submit()
    game_interface.root.update()


def verify_username_set_correctly(game_interface, username):
    # Verify that the username is set correctly in the GameInterface
    assert game_interface.username == username


def verify_user_recognized(checker, username):
    # Verify that the user is recognized by the UserChecker
    assert checker.check_user(username)


def verify_user_written_to_csv(username):
    # Verify that the username is written to the CSV file
    csv_content = read_csv(CSV_FILE_PATH)
    assert any(username in row for row in csv_content)


@patch('tkinter.messagebox.showinfo')
def test_username_entry_existing_user(mock_showinfo, game_interface):
    # Test the username entry process for an existing user
    simulate_username_entry(game_interface, "Hugo")
    verify_username_set_correctly(game_interface, "Hugo")
    checker = UserChecker()
    mock_showinfo.assert_called_once_with("Welcome", "Welcome back, Hugo!")
    verify_user_recognized(checker, "Hugo")


@patch('tkinter.messagebox.showinfo')
def test_username_entry_new_user(mock_showinfo, game_interface):
    # Test the username entry process for a new user
    simulate_username_entry(game_interface, "Andre")
    verify_username_set_correctly(game_interface, "Andre")
    mock_showinfo.assert_called_once_with("Welcome", "Welcome, Andre!")

    # Check if the new user "Andre" is written to the CSV file
    verify_user_written_to_csv("Andre")


@patch('tkinter.messagebox.showerror')
def test_empty_username_entry(mock_showerror, game_interface):
    # Test the username entry process with an empty username
    game_interface.show_username_entry()
    game_interface.root.update()
    game_interface.username_input.insert(0, "")
    game_interface.username_entry_on_submit()
    game_interface.root.update()
    mock_showerror.assert_called_once_with("Error", "Username cannot be empty!")


def test_duplicate_username_not_added(game_interface):
    # Test that a duplicate username is not added to the CSV file
    simulate_username_entry(game_interface, "Hugo")
    initial_csv_content = read_csv(CSV_FILE_PATH)
    simulate_username_entry(game_interface, "Hugo")
    final_csv_content = read_csv(CSV_FILE_PATH)
    assert initial_csv_content == final_csv_content


def test_new_user_added_to_csv(game_interface):
    # Test that a new user is added to the CSV file
    simulate_username_entry(game_interface, "Andre")

    # Read the CSV file to check if "Andre" is in it
    csv_content = read_csv(CSV_FILE_PATH)

    # Verify that "Andre" is added to the CSV file
    assert any("Andre" in row for row in csv_content), "The new user 'Andre' was not added to the users.csv file."
