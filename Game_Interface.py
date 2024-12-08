"""
Game Interface Module

This module provides the graphical user interface for the game. It includes functionalities for:
- Starting the game and selecting difficulty and teams.
- Displaying player images and game menus.
- Handling user interactions and game logic.
- Showing end game results and playing media files.

Classes:
    GameInterface: Manages the game interface and user interactions.

Usage:
    Run this module to start the game interface.

Example:
    python Game_Interface.py

Dependencies:
    - csv
    - os
    - datetime
    - typing
    - tkinter
    - imageio
    - pygame
    - PIL (Pillow)
    - csv_operations
    - gameplay
    - image_loader
    - player

Author:
    Hugo LS

Date:
    8 December 2024
"""
import csv
import os
from datetime import datetime
from typing import List, Tuple, Optional

import tkinter as tk
from tkinter import messagebox, ttk

import imageio
import pygame
from PIL import Image, ImageTk, ImageSequence

from csv_operations import CSVHandler, UserChecker
from gameplay import GamePlay
from image_loader import ImageLoader
from player import Player


class GameInterface:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Game Interface")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.username = None
        self.players_list: List[Player] = []
        self.username_input = None
        base_directory = os.path.join(os.path.dirname(__file__), '..', 'Guess who')
        self.image_loader = ImageLoader(os.path.join(base_directory, 'media/Faces'),
                                        os.path.join(base_directory, 'media/Logos'))
        self.player_images = self.image_loader.load_all_player_images()
        self.team_image_size = (100, 100)
        self.is_user_turn = True
        pygame.mixer.init()
        self.music_file = os.path.join(base_directory, 'media/Video_and_song/champions.mp3')

    def start(self) -> None:
        """Start the game interface by showing the username entry screen."""
        self.play_music()
        self.show_username_entry()
        self.root.mainloop()

    def play_music(self) -> None:
        """Play background music."""
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)

    def play_video(self, video_path: str) -> None:
        """Play best goals video in a new window."""
        video = imageio.get_reader(video_path)
        video_meta = video.get_meta_data()
        frame_rate = video_meta['fps']
        video_width, video_height = video_meta['size']

        video_window = tk.Toplevel(self.root)
        video_window.title("Video Player")

        # Center the video window on the screen with the same size as the video
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - video_height / 2)
        position_right = int(screen_width / 2 - video_width / 2)
        video_window.geometry(f"{video_width}x{video_height}+{position_right}+{position_top}")

        video_label = tk.Label(video_window)
        video_label.pack()

        def stream_video():
            try:
                for frame in video:
                    frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
                    video_label.config(image=frame_image)
                    video_label.image = frame_image
                    video_window.update()
                    self.root.after(int(1000 / frame_rate))  # Adjust frame rate
            except Exception as e:
                print(f"Error playing video: {e}")
            finally:
                video.close()

        stream_video()

    def clear_and_create_frame(self) -> tk.Frame:
        """Clear the current window and create a new frame everytime that a new window is open."""
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        return frame

    def show_username_entry(self) -> None:
        """Username entry screen """
        frame = self.clear_and_create_frame()
        intro_image = self.image_loader.load_logo_image('intro')
        if intro_image:
            image_label = tk.Label(frame, image=intro_image)
            image_label.image = intro_image
            image_label.pack()
        tk.Label(frame, text="Enter the username:").pack()
        self.username_input = tk.Entry(frame)
        self.username_input.pack()
        submit_button = tk.Button(frame, text="Submit", command=self.username_entry_on_submit)
        submit_button.pack()

    def username_entry_on_submit(self) -> None:
        """Handle the username submission."""
        self.username = self.username_input.get()
        if not self.username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return None
        checker = UserChecker()
        if checker.check_user(self.username):
            messagebox.showinfo("Welcome", f"Welcome back, {self.username}!")
        else:
            messagebox.showinfo("Welcome", f"Welcome, {self.username}!")
        self.players_list = checker.import_players_from_csv()
        self.player_images = self.image_loader.load_all_player_images()
        self.show_main_menu()

    def show_main_menu(self) -> None:
        """Shows main menu and split the frame in 3 in order to get photos of the players on the left, buttons on the
        right and photos of the remaining players on the right."""
        frame, frames = self.create_menu_frames(3)
        left_frame, center_frame, right_frame = frames
        tk.Button(center_frame, text="1. New Game", command=self.show_difficulty_menu).pack(pady=10)
        tk.Button(center_frame, text="2. View Records",
                  command=lambda: self.show_difficulty_menu(view_records=True)).pack(pady=10)
        tk.Button(center_frame, text="3. View Video",
                  command=lambda: self.play_video("/home/gyo/Desktop/Guess who/media/Video_and_song/golos.mp4")).pack(
            pady=10)  # Update with the path to your video file
        tk.Button(center_frame, text="Exit", command=self.root.quit).pack(pady=10)
        total_images = len(self.player_images)
        columns = 6
        mid_point = total_images // 2
        left_images = list(self.player_images.items())[:mid_point]
        right_images = list(self.player_images.items())[mid_point:]
        self.display_images_in_grid(left_frame, left_images, columns)
        self.display_images_in_grid(right_frame, right_images, columns)

    def create_menu_frames(self, divisions: int) -> Tuple[tk.Frame, List[tk.Frame]]:
        """Create frames for the menu layout.

        Args:
            divisions (int): The number of divisions (frames) to create.

        Returns:
            Tuple[tk.Frame, List[tk.Frame]]: The main frame and a list of sub-frames.
        """
        frame = self.clear_and_create_frame()
        frames = []
        for i in range(divisions):
            sub_frame = tk.Frame(frame)
            sub_frame.grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
            frame.grid_columnconfigure(i, weight=1 if divisions == 2 else (2 if i == 1 else 1))
            frames.append(sub_frame)
        return frame, frames

    def display_images_in_grid(self, frame: tk.Frame, images: List[Tuple[str, ImageTk.PhotoImage]], columns: int,
                               show_select_buttons: bool = False, gameplay: Optional[GamePlay] = None,
                               check_same_user: bool = False) -> None:
        """
        Display images in a grid layout.

        Args:
            frame (tk.Frame): The frame to display the images in.
            images (List[Tuple[str, ImageTk.PhotoImage]]): The list of images to display.
            columns (int): The number of columns in the grid.
            show_select_buttons (bool): Whether to show select buttons for each player.
            gameplay (Optional[GamePlay]): The gameplay instance.
            check_same_user (bool): Whether to check if shows user or opponent players.
            check_same_user: can be used on future implementations. e.g. if we introduce a new variant of the game
            when both user or opponent can change their player after asking 3 right questions. this way it will
            be possible to reuse the same function to display the players and select the new player.
        """
        row_frame = tk.Frame(frame)
        row_frame.pack()
        col = 0

        for player_name, player_image in images:
            # Container for every image and button
            container = tk.Frame(row_frame)
            container.pack(side=tk.LEFT, padx=10, pady=10)

            # Image label
            img_label = tk.Label(container, image=player_image)
            img_label.image = player_image
            img_label.pack(side=tk.TOP)

            # Player info label
            if gameplay:
                player = next(player for player in gameplay.players if player.name == player_name)
                player_info = (f"Name: {player.name}\nTeam: {player.team}\nGoals: "
                               f"{player.goals}\nAssists: {player.assists}")
                info_label = tk.Label(container, text=player_info)
                info_label.pack(side=tk.TOP)

            # Display selection buttons if show_select_buttons is True
            if show_select_buttons and gameplay:
                if check_same_user:
                    select_button = tk.Button(container, text="Select",
                                              command=lambda p=player: [
                                                  self.update_and_refresh_after_question(gameplay, 8, p.name)])
                else:
                    select_button = tk.Button(container, text="Select",
                                              command=lambda p=player: [gameplay.select_user_player(p),
                                                                        gameplay.select_random_opponent_player(),
                                                                        self.show_in_game_menu(gameplay)])
                select_button.pack(side=tk.TOP, pady=5)

            # Handle column wrapping
            col += 1
            if col >= columns:
                row_frame = tk.Frame(frame)
                row_frame.pack()
                col = 0

    def show_difficulty_menu(self, view_records: bool = False) -> None:
        """
        Display the difficulty selection menu or the view records menu.

        Args:
            view_records (bool): If True, show the records menu instead of the team selection menu.
        """
        frame = self.clear_and_create_frame()
        tk.Label(frame, text="Choose Difficulty").pack(pady=10)
        tk.Button(frame, text="Easy",
                  command=lambda: self.show_records_menu("Easy") if view_records else self.show_team_selection_menu(
                      "Easy")).pack(pady=5)
        tk.Button(frame, text="Medium",
                  command=lambda: self.show_records_menu("Medium") if view_records else self.show_team_selection_menu(
                      "Medium")).pack(pady=5)
        tk.Button(frame, text="Hard",
                  command=lambda: self.show_records_menu("Hard") if view_records else self.show_team_selection_menu(
                      "Hard")).pack(pady=5)
        tk.Button(frame, text="Back", command=self.show_main_menu).pack(pady=5)

    def show_records_menu(self, difficulty: str) -> None:
        """
        Display the records menu for the selected difficulty.

        Args:
            difficulty (str): The selected difficulty level.
        """
        frame = self.clear_and_create_frame()
        tk.Label(frame, text=f"Records for {difficulty}").pack(pady=10)

        # Load records from the corresponding CSV file
        records_file = f"databases/records_{difficulty.lower()}.csv"
        records = CSVHandler.load_records(records_file)

        # Sort records by the minimum value of column B and by date
        sorted_records = sorted(records, key=lambda x: (int(x['value']), x['date']))

        # Display records
        for record in sorted_records:
            record_text = f"Name: {record['name']}, Number of questions: {record['value']}, Date: {record['date']}"
            tk.Label(frame, text=record_text).pack(pady=5)

        tk.Button(frame, text="Back", command=lambda: self.show_difficulty_menu(view_records=True)).pack(pady=10)

    def show_team_selection_menu(self, difficulty: str) -> None:
        """
        Show the team selection menu.

        Args:
            difficulty (str): The selected difficulty level.
        """
        frame = self.clear_and_create_frame()
        tk.Label(frame, text="Choose Your Team").pack(pady=10)
        teams = ["Sporting", "Benfica", "Porto", "Random"]
        for team in teams:
            logo_image = self.image_loader.load_logo_image(team)
            if logo_image:
                button = tk.Button(frame, image=logo_image, command=lambda t=team: self.start_game(difficulty, t))
                button.image = logo_image
                button.pack(side=tk.LEFT, padx=10, pady=10)
        back_button = tk.Button(
            frame,
            text="Back",
            command=self.show_difficulty_menu,
            width=self.team_image_size[0] // 5,
            height=self.team_image_size[1] // 11
        )
        back_button.pack(pady=200)

    def show_select_player_menu(self, gameplay: GamePlay) -> None:
        """
        Show the player selection menu when the game is started.

        Args:
            gameplay (GamePlay): The gameplay instance.
        """
        frame = self.clear_and_create_frame()
        tk.Label(frame, text="Select a Player").pack(pady=10)
        columns = 6
        self.display_images_in_grid(frame, [(player.name, self.player_images[player.name]) for player in
                                            gameplay.user_team_players], columns, show_select_buttons=True,
                                    gameplay=gameplay)

    def show_in_game_menu(self, gameplay: GamePlay, show_user_team: bool = False) -> None:
        """Show the in-game menu.

        Args:
            gameplay (GamePlay): The gameplay instance.
            show_user_team (bool): Whether to show the user's team or opponent team.
        """
        frame, frames = self.create_menu_frames(2)
        left_frame, right_frame = frames

        # Determine which team's players to display
        players_to_display = gameplay.user_team_players if show_user_team else gameplay.opponent_team_players

        # Display players on the left of the screen
        columns = 6
        self.display_images_in_grid(left_frame, [(player.name, self.player_images[player.name]) for player in
                                                 players_to_display], columns, show_select_buttons=True,
                                    gameplay=gameplay, check_same_user=True)

        # Add buttons on the right
        buttons = [
            "1. Does the player have light hair?",
            "2. Does the player have short hair?",
            "3. Is the player tanned?",
            "4. Original continent:",
            "5. Goals last season:",
            "6. Assists last season:",
            "7. Position:"
        ]

        # Create a container frame to center the buttons
        button_container = tk.Frame(right_frame)
        button_container.pack(expand=True)

        for i, button_text in enumerate(buttons, start=1):
            tk.Button(button_container, text=button_text,
                      command=lambda q=i: self.update_and_refresh_after_question(gameplay, q)).pack(pady=5)

        tk.Button(button_container, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_continents_or_positions_menu(self, gameplay: GamePlay, options: dict, title: str, question: int) -> None:
        """Display a selection menu for the continents or positions after selecting
            that option in the in_game_menu.

        Args:
            gameplay (GamePlay): The gameplay instance.
            options (dict): The options to display in the menu.
            title (str): The title of the menu.
            question (int): The question number.
        """

        def select_option(selected_option: int) -> None:
            selected_option_str = options[selected_option]
            # Continue the game flow after selection
            self.update_and_refresh_after_question(gameplay, question, selected_option_str)

        frame = self.clear_and_create_frame()
        self.root.title(title)

        # Create a frame for the buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(fill="both", expand=True)

        # Distribute option buttons
        for number, option in options.items():
            ttk.Button(button_frame, text=option, command=lambda opt=number: select_option(opt)).pack(
                side="top", fill="x", padx=20, pady=10
            )

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def show_goals_or_assists_menu(self, gameplay: GamePlay, question: int) -> None:
        """
        Display a menu for selecting goals or assists conditions.

        Args:
            gameplay (GamePlay): The gameplay instance.
            question (int): The question number.
        """

        def submit_input(option: str) -> None:
            """
            Submit the input value for the selected option.

            Args:
                option (str): The selected option ('less_or_equal' or 'more').
            """
            input_value = input_entry.get()
            if input_value.isdigit():
                self.update_and_refresh_after_question(gameplay, question, f"{option}:{int(input_value)}")
            else:
                messagebox.showerror("Invalid input", "Please enter a valid number.")

        frame = self.clear_and_create_frame()
        self.root.title("Goals or Assists Selector")

        tk.Label(frame, text="Choose 'less or equal' or 'more' and enter the number:").pack(pady=10)

        input_entry = tk.Entry(frame)
        input_entry.pack(pady=10)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Less or equal",
                   command=lambda: submit_input("less_or_equal")).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="More",
                   command=lambda: submit_input("more")).pack(side=tk.LEFT, padx=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def update_and_refresh_after_question(self, gameplay: GamePlay, question: int,
                                          selected_option: Optional[str] = None) -> None:
        """
        Update the game state and refresh the interface after a question is asked.

        Args:
            gameplay (GamePlay): The gameplay instance.
            question (int): The question number.
            selected_option (Optional[str]): The selected option for the question, if any.
            selected_option can be: Continents, positions or player_selected

        If the question requires additional input (e.g., continent,position selection),
        the appropriate menu is shown. Otherwise, the question is processed, and the game state is updated accordingly.
        The interface is refreshed to display the question and answer, and the turn is switched between the user and
        the opponent.
        """
        if question == 4 and self.is_user_turn and not selected_option:
            continent_mapping = gameplay.get_continent_mapping()
            self.show_continents_or_positions_menu(gameplay, continent_mapping, "Continent Selector", question)
            return
        elif question == 7 and self.is_user_turn and not selected_option:
            position_mapping = gameplay.get_position_mapping()
            self.show_continents_or_positions_menu(gameplay, position_mapping, "Position Selector", question)
            return
        elif question in [5, 6] and self.is_user_turn and not selected_option:
            self.show_goals_or_assists_menu(gameplay, question)
            return

        if self.is_user_turn:
            gameplay.opponent_team_players, question, answer = gameplay.process_question(
                question, gameplay.opponent_selected_player, gameplay.opponent_team_players, selected_option
            )

            self.show_question_and_answer(gameplay, question, answer, lambda: self.update_and_refresh_after_question(
                gameplay,
                *gameplay.opponent_turn()),
                                          player_name=selected_option)
            self.is_user_turn = False
        else:
            gameplay.user_team_players, question, answer = gameplay.process_question(
                question, gameplay.user_selected_player, gameplay.user_team_players, selected_option
            )

            self.show_question_and_answer(gameplay, question, answer,
                                          lambda: self.show_in_game_menu(gameplay, show_user_team=False),
                                          is_bot_question=True, player_name=selected_option)
            self.is_user_turn = True

    def show_question_and_answer(self, gameplay, question: str, answer: str, next_command: callable,
                                 is_bot_question: bool = False, player_name: Optional[str] = None) -> None:
        """
        Display the question and answer, and provide an "OK" button to proceed.

        Args:
            gameplay (GamePlay): The gameplay instance.
            question (str): The question to display.
            answer (str): The answer to display.
            next_command (callable): The function to call when the "OK" button is pressed.
            is_bot_question (bool): Whether the question is from the bot.
            player_name (Optional[str]): The name of the player being guessed if is that the case.
        """
        frame = self.clear_and_create_frame()

        # Display the question
        if is_bot_question:
            question = "Opponent question: " + question
        tk.Label(frame, text=question, font=("Helvetica", 16)).pack(pady=10)

        if "Guess player:" in question:
            answer = f"Player: {player_name} - {answer}"
            if answer.endswith("yes"):
                frame.destroy()
                if self.is_user_turn:
                    self.show_end_game(1, player_name, gameplay.difficulty,
                                       gameplay.opponent_question_counter)  # User wins
                else:
                    self.show_end_game(2, player_name, "", 0)
                    """Bot win's. doesn't matter the difficulty or question_counter because 
                    it wont write to the csv file"""
                return
        tk.Label(frame, text=answer, font=("Helvetica", 14)).pack(pady=10)

        # OK button to proceed
        tk.Button(frame, text="OK", command=next_command).pack(pady=20)

    def show_end_game(self, user, player_name, difficulty, question_counter) -> None:
        """
        Display the end game screen with the appropriate message and GIFs.

        Args:
            user (int): Indicates if the user (1) or the bot (2) won.
            player_name (str): The name of the guessed player.
            difficulty (str): The difficulty level of the game.
            question_counter (int): The number of questions asked by the opponent.
        """
        frame, frames = self.create_menu_frames(3)
        left_frame, center_frame, right_frame = frames

        if user == 1:
            self.show_gif_in_frame(left_frame, "media/Logos/dicaprio.gif", (400, 400))
            self.show_gif_in_frame(right_frame, "media/Logos/si.gif", (400, 400))
            message = f"Your guess: {player_name}.\nCongratulations!\nYou guessed the opponent player!"

            # Write to the appropriate CSV file
            record_file = f"databases/records_{difficulty.lower()}.csv"
            with open(record_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.username, question_counter, datetime.now().strftime("%Y-%m-%d")])
        else:
            self.show_gif_in_frame(left_frame, "media/Logos/looser.gif", (400, 400))
            self.show_gif_in_frame(right_frame, "media/Logos/looser2.gif", (400, 400))
            message = f"Bot guess: {player_name}.\nThe bot guessed your player!"

        tk.Label(center_frame, text=message, font=("Helvetica", 16)).pack(pady=10)
        tk.Button(center_frame, text="OK", command=self.show_main_menu).pack(pady=20)

    def show_gif_in_frame(self, frame, gif_path, size):
        """
        Display a GIF in the given frame.

        Args:
            frame (tk.Frame): The frame to display the GIF in.
            gif_path (str): The path to the GIF file.
            size (Tuple[int, int]): The size to resize the GIF frames to.
        """
        try:
            gif_image = Image.open(gif_path)
            frames = [ImageTk.PhotoImage(frame.resize(size, Image.Resampling.LANCZOS)) for frame in
                      ImageSequence.Iterator(gif_image)]

            def update_frame(index):
                if frame_label.winfo_exists():
                    frame_label.config(image=frames[index])
                    self.root.after(100, update_frame, (index + 1) % len(frames))

            frame_label = tk.Label(frame)
            frame_label.pack()
            update_frame(0)
        except Exception as e:
            print(f"Error loading GIF: {e}")

    def start_game(self, difficulty: str, user_team: str) -> None:
        """
        Start the game with the selected difficulty and user team.

        Args:
            difficulty (str): The selected difficulty level.
            user_team (str): The selected user team.
        """
        self.is_user_turn = True
        GamePlay.players = self.players_list
        gameplay = GamePlay(difficulty, user_team)
        messagebox.showinfo("Opponent Team", f"Your opponent's team is: {gameplay.opponent_team}")
        self.show_select_player_menu(gameplay)

    def on_close(self) -> None:
        """Handle the window close event."""
        self.root.quit()


if __name__ == "__main__":
    interface = GameInterface()
    interface.start()
