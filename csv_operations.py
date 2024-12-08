from abc import ABC, abstractmethod
import csv
from player import Player
import os
from typing import List, Dict
from datetime import datetime


class CSVHandler(ABC):
    @abstractmethod
    def read_csv(self, filename: str) -> List[List[str]]:
        """Abstract method to read a CSV file.

        Args:
            filename (str): The name of the CSV file.

        Returns:
            List[List[str]]: The content of the CSV file as a list of rows.
        """
        pass

    @abstractmethod
    def write_csv(self, data: List[str], filename: str) -> None:
        """Abstract method to write to a CSV file.

        Args:
            data (List[str]): The data to write to the CSV file.
            filename (str): The name of the CSV file.
        """
        pass

    def import_players_from_csv(self, filename: str = 'databases/players.csv') -> List[Player]:
        """Import players from a CSV file and return a list of Player objects.

        Args:
            filename (str): The name of the CSV file.

        Returns:
            List[Player]: A list of Player objects.
        """
        players = []
        rows = self.read_csv(filename)
        for row in rows:
            row = [field.strip() for field in row]
            if len(row) == 9:
                try:
                    name, team, hair_color, hair_length, skin_color, continent, goals, assists, position = row
                    goals = int(goals)
                    assists = int(assists)
                    player = Player(
                        name=name,
                        team=team,
                        hair_color=hair_color,
                        hair_length=hair_length,
                        skin_color=skin_color,
                        continent=continent,
                        goals=goals,
                        assists=assists,
                        position=position
                    )
                    players.append(player)
                except ValueError as ve:
                    print(f"Skipping invalid row due to value error: {row} - {ve}")
            else:
                print(f"Skipping invalid row: {row}")
        return players

    @staticmethod
    def load_records(file_path: str) -> List[Dict[str, str]]:
        records = []
        print(f"Loading records from: {file_path}")
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file, delimiter=',')  # Use comma as the delimiter
                for row in csv_reader:
                    print(f"Read row: {row}")
                    if len(row) == 3 and all(row):  # Ensure the row has exactly 3 elements and none are empty
                        record = {
                            'name': row[0] if row[0] else 'Unknown',
                            'value': row[1],
                            'date': row[2]
                        }
                        records.append(record)
                        print(f"Appended record: {record}")
                    else:
                        print(f"Invalid row: {row}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")
        return records

    def save_user_record(self, difficulty: str, username: str, questions: int) -> None:
        """Save the user's record to the CSV file.

        Args:
            difficulty (str): The difficulty level.
            username (str): The username.
            questions (int): The number of questions asked by the opponent.
        """
        record_file = f"databases/records_{difficulty.lower()}.csv"
        record = [username, str(questions), datetime.now().strftime("%Y-%m-%d")]
        self.write_csv(record, record_file)


class UserChecker(CSVHandler):
    filename = 'databases/users.csv'
    username = None

    def read_csv(self, filename: str) -> List[List[str]]:
        """Read a CSV file and return its content as a list of rows.

        Args:
            filename (str): The name of the CSV file.

        Returns:
            List[List[str]]: The content of the CSV file as a list of rows.
        """
        try:
            with open(filename, 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                return [row for row in csv_reader]
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return []
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []

    def write_csv(self, data: List[str], filename: str) -> None:
        """Write a row of data to a CSV file. Creates the file if it doesn't exist.

        Args:
            data (List[str]): The data to write to the CSV file.
            filename (str): The name of the CSV file.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        try:
            with open(filename, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(data)
        except IOError:
            print(f"Error writing to file: {filename}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def check_user(self, username: str) -> bool:
        """Check if a username exists in the CSV file. Adds the username if it doesn't exist.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        users = self.read_csv(self.filename)
        if any(username in user for user in users):
            return True
        else:
            self.write_csv([username], self.filename)
            return False
