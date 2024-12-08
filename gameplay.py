"""
Gameplay Module

This module handles the core gameplay logic for the game. It includes functionalities for:
- Setting up teams and selecting players.
- Processing questions and updating the game state.
- Managing the opponent's turn and difficulty levels.

Classes:
    GamePlay: Manages the gameplay logic and player interactions.

Usage:
    Import this module to use the GamePlay class in the game.

Example:
    from gameplay import GamePlay

Dependencies:
    - random
    - statistics
    - typing
    - PIL (Pillow)
    - player

Author:
    Hugo LS

Date:
    8 December 2024
"""
import random
import statistics
from typing import List, Dict, Optional, Tuple

from PIL import ImageTk

from player import Player


class GamePlay:
    players: List[Player] = []  # Class variable to hold the players list
    player_images: Dict[str, ImageTk.PhotoImage] = {}  # Class variable to hold player images

    def __init__(self, difficulty: str, user_team: str, opponent_team: str = None) -> None:
        """Initialize the GamePlay class with the selected parameters.

        Args:
            difficulty (str): The selected difficulty level.
            user_team (str): The selected user team.
            opponent_team (str): The selected opponent team.
        """
        self.questions = None
        self.difficulty = difficulty
        self.user_team = user_team
        self.opponent_team = opponent_team
        self.available_players: List[Player] = []
        self.user_team_players: List[Player] = []
        self.opponent_team_players: List[Player] = []
        self.user_selected_player: Optional[Player] = None
        self.opponent_selected_player: Optional[Player] = None
        self.opponent_asked_continents = []
        self.opponent_asked_positions = []
        self.opponent_asked_questions = []
        self.opponent_question_counter = 0
        self.opponent_yes_questions = []
        self.opponent_asked_player = []

        self.setup_teams()

    def setup_teams(self) -> None:
        """Set up the teams based on the user team selection.
        If the user team is Random, select 24 random players from the list.
        if the user team is Sporting, Benfica or Porto, select the players from the respective team.
        """
        if self.user_team == "Random":
            self.user_team_players = random.sample(self.players, 24)
            self.opponent_team_players = self.user_team_players
            self.opponent_team = "Random"
        else:
            self.user_team_players = [player for player in self.players if player.team == self.user_team]
            possible_teams = ["Sporting", "Benfica", "Porto"]
            self.opponent_team = random.choice(possible_teams)
            self.opponent_team_players = [player for player in self.players if player.team == self.opponent_team]

    def get_opponent_team(self) -> str:
        """Get the opponent team.

        Returns:
            str: The opponent team.
        """
        return self.opponent_team

    def select_user_player(self, player: Player) -> None:
        self.user_selected_player = player

    def select_random_opponent_player(self) -> None:
        self.opponent_selected_player = random.choice(self.opponent_team_players)

    @staticmethod
    def get_continent_mapping() -> Dict[int, str]:
        """Get a mapping of continent options.

        Returns:
            Dict[int, str]: A dictionary mapping option numbers to continent names.
        """
        return {
            1: "Africa",
            2: "Asia",
            3: "Europe",
            4: "North America",
            5: "South America",
            6: "Oceania"
        }

    @staticmethod
    def get_position_mapping() -> Dict[int, str]:
        """Get a mapping of position options.

        Returns:
            Dict[int, str]: A dictionary mapping option numbers to position names.
        """
        return {
            1: "Goalkeeper",
            2: "Defender",
            3: "Midfielder",
            4: "Forward"
        }

    @staticmethod
    def calculate_median(players: List['Player'], stat: str) -> float:
        values = [getattr(player, stat) for player in players]
        return statistics.median(values)

    @staticmethod
    def calculate_stat_condition(player, stat, option, value, correct_answer):
        """Calculate if the player's stat meets the condition.

          Args:
              player (Player): The player object.
              stat (str): The stat attribute to check (e.g., goals, assists).
              option (str): The comparison option ("less_or_equal" or "more").
              value (int): The value to compare against.
              correct_answer (str): The expected answer ("yes" or "no").

          Returns:
              bool: True if the condition is met, False otherwise.
          """

        if option == "less_or_equal":
            return (getattr(player, stat) <= value) if correct_answer == "yes" else (getattr(player, stat) > value)
        else:
            return (getattr(player, stat) > value) if correct_answer == "yes" else (getattr(player, stat) <= value)

    @staticmethod
    def compare_attribute(player: Player, attribute: str, selected_option: str, correct_answer: str) -> bool:
        """Compare the player's attribute with the selected option.

         Args:
             player (Player): The player object.
             attribute (str): The attribute to compare (e.g., continent, position).
             selected_option (str): The selected option to compare against.
             correct_answer (str): The expected answer ("yes" or "no").

         Returns:
             bool: True if the condition is met, False otherwise.
         """
        if correct_answer == "yes":
            return getattr(player, attribute).lower() == selected_option.lower()
        else:
            return getattr(player, attribute).lower() != selected_option.lower()

    @staticmethod
    def update_available_players(question, answer, available_players,
                                 selected_option: Optional[str] = None) -> List[Player]:
        """
        Update the list of available players based on the question and the correct answer.

        Args: question (int): The question number. correct_answer (str): The correct answer to the question ("yes" or
        "no"). available_players (List[Player]): The current list of available players. selected_option (Optional[
        str]): The selected option from the menu (positions, continents, goals, or assists).

        Returns:
            List[Player]: The updated list of available players.
        """
        if question == 1:
            if answer == "yes":
                available_players = [player for player in available_players if player.hair_color.lower() == "light"]
            else:
                available_players = [player for player in available_players if player.hair_color.lower() != "light"]
        elif question == 2:
            if answer == "yes":
                available_players = [player for player in available_players if player.hair_length.lower() == "short"]
            else:
                available_players = [player for player in available_players if player.hair_length.lower() != "short"]
        elif question == 3:
            if answer == "yes":
                available_players = [player for player in available_players if player.skin_color.lower() == "tanned"]
            else:
                available_players = [player for player in available_players if player.skin_color.lower() != "tanned"]
        elif question in [4, 7] and selected_option:
            attribute = "continent" if question == 4 else "position"
            available_players = [player for player in available_players if
                                 GamePlay.compare_attribute(player, attribute, selected_option, answer)]
        elif question in [5, 6] and selected_option:
            option, value = selected_option.split(":")
            value = int(value)
            stat = "goals" if question == 5 else "assists"
            available_players = [player for player in available_players if
                                 GamePlay.calculate_stat_condition(player, stat, option, value, answer)]
        elif question == 8:
            if answer == "no":
                available_players = [player for player in available_players if player.name != selected_option]
        return available_players

    def process_question(self, question: int, selected_player: Player, available_players: List[Player],
                         selected_option: Optional[str] = None) -> Tuple[List[Player], str, str]:
        """
        Process the given question and update the list of available players based on the answer.

        Args: question (int): The question number. selected_player (Player): The player selected by the opponent.
        available_players (List[Player]): The current list of available players. selected_option (Optional[str]): The
        selected option from the menu (positions, continents, goals, or assists).

        Returns: Tuple[List[Player], str, str]: The updated list of available players, the question text,
        and the correct answer.
        """
        question_options = [
            "1. Does the player have light hair?",
            "2. Does the player have short hair?",
            "3. Is the player tanned?",
            "4. Original continent: {}",
            "5. Goals last season: {}",
            "6. Assists last season: {}",
            "7. Position: {}",
            "8. Guess player:"
        ]

        if question is None or question < 1 or question > len(question_options):
            raise ValueError("Invalid question number")

        question_text = question_options[question - 1]
        correct_answer = "yes"

        if question == 1:
            correct_answer = "yes" if selected_player.hair_color.lower() == "light" else "no"
        elif question == 2:
            correct_answer = "yes" if selected_player.hair_length.lower() == "short" else "no"
        elif question == 3:
            correct_answer = "yes" if selected_player.skin_color.lower() == "tanned" else "no"
        elif question in [4, 7] and selected_option:
            attribute = selected_player.continent if question == 4 else selected_player.position
            correct_answer = "yes" if attribute.lower() == selected_option.lower() else "no"
            question_text = question_text.format(selected_option)
        elif question in [5, 6] and selected_option:
            option, value = selected_option.split(":")
            value = int(value)
            stat = "goals" if question == 5 else "assists"
            correct_answer = "yes" if GamePlay.calculate_stat_condition(selected_player, stat, option, value,
                                                                        correct_answer) else "no"
            question_text = question_text.format(f"{option.replace('_', ' ')} {value}")
        elif question == 8:
            correct_answer = "yes" if selected_player.name == selected_option else "no"

        self.available_players = self.update_available_players(question, correct_answer, available_players,
                                                               selected_option)

        if correct_answer == "yes" and question in [4, 7]:
            self.opponent_yes_questions.append(question)

        return self.available_players, question_text, correct_answer

    def opponent_turn(self) -> Tuple[int, Optional[str]]:
        """
        Determine the opponent's turn based on the difficulty level and the current state of the game.

        Returns:
            Tuple[int, Optional[str]]: The question number and the selected option (if any).
        """

        def get_selected_option(opponent_question):
            if opponent_question == 4:
                if self.difficulty == "Easy":
                    available_continents = [c for c in self.get_continent_mapping().values()]
                else:
                    available_continents = [c for c in self.get_continent_mapping().values() if
                                            c not in self.opponent_asked_continents]
                selected_continent = random.choice(available_continents)
                if self.difficulty != "Easy":
                    self.opponent_asked_continents.append(selected_continent)
                return selected_continent
            elif opponent_question == 7:
                if self.difficulty == "Easy":
                    available_positions = [p for p in self.get_position_mapping().values()]
                else:
                    available_positions = [p for p in self.get_position_mapping().values() if
                                           p not in self.opponent_asked_positions]
                selected_position = random.choice(available_positions)
                if self.difficulty != "Easy":
                    self.opponent_asked_positions.append(selected_position)
                return selected_position
            else:
                option = random.choice(["less_or_equal", "more"])
                value = random.randint(0, 10)
                return f"{option}:{value}"

        selected_option = None
        if self.difficulty == "Easy":
            if len(self.user_team_players) <= 10:
                question = 8
                selected_option = random.choice([player.name for player in self.user_team_players
                                                 if player.name not in self.opponent_asked_player])
            else:
                question = random.randint(1, 7)
                selected_option = get_selected_option(question)

        elif self.difficulty == "Medium":
            if len(self.user_team_players) <= 6:
                question = 8
                selected_option = random.choice([player.name for player in self.user_team_players
                                                 if player.name not in self.opponent_asked_player])
            else:
                available_questions = [q for q in range(1, 7) if q not in self.opponent_asked_questions]
                if not available_questions:
                    raise ValueError("No available questions left to ask.")
                question = random.choice(available_questions)
                if question in [4, 5, 6, 7]:
                    selected_option = get_selected_option(question)

        elif self.difficulty == "Hard":
            if len(self.user_team_players) <= 3:
                question = 8
                selected_option = random.choice([player.name for player in self.user_team_players
                                                 if player.name not in self.opponent_asked_player])
            else:
                goals_median = self.calculate_median(self.user_team_players, "goals")
                assists_median = self.calculate_median(self.user_team_players, "assists")
                if self.opponent_question_counter == 0:
                    question = 5
                    selected_option = f"less_or_equal:{int(goals_median)}"
                    self.opponent_asked_questions.append(question)
                elif self.opponent_question_counter == 1 and assists_median > 1:
                    question = 6
                    selected_option = f"less_or_equal:{int(assists_median)}"
                    self.opponent_asked_questions.append(question)
                else:
                    available_questions = [q for q in range(1, 8) if
                                           q not in self.opponent_asked_questions and q
                                           not in self.opponent_yes_questions]

                    if not available_questions:
                        raise ValueError("No available questions left to ask.")
                    question = random.choice(available_questions)
                    if question in [4, 7]:
                        selected_option = get_selected_option(question)
                    elif question in [5, 6]:
                        selected_option = f"less_or_equal:{int(goals_median)}" if question == 5 \
                            else f"less_or_equal:{int(assists_median)}"

        else:
            raise ValueError("Invalid difficulty level")

        if question in [1, 2, 3]:
            self.opponent_asked_questions.append(question)
        self.opponent_question_counter += 1
        return question, selected_option
