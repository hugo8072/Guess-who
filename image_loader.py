from PIL import Image, ImageTk
import os
from typing import Dict

from PIL.ImageTk import PhotoImage


class ImageLoader:
    def __init__(self, player_image_directory: str, logo_image_directory: str) -> None:
        """
        Initialize the class with directories for player and logo images.

        Args:
            player_image_directory (str): Directory path for player images.
            logo_image_directory (str): Directory path for logo images.
        """
        self.player_image_directory = player_image_directory
        self.logo_image_directory = logo_image_directory

    def load_all_player_images(self) -> Dict[str, ImageTk.PhotoImage]:
        """
        Load all player images from the specified directory.

        Returns:
            Dict[str, ImageTk.PhotoImage]: A dictionary mapping player names to their images.
        """
        player_images = {}
        for filename in os.listdir(self.player_image_directory):
            if filename.endswith('.png'):
                player_name = filename.replace('_', ' ').replace('.png', '')
                image_path = os.path.join(self.player_image_directory, filename)
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    player_images[player_name] = ImageTk.PhotoImage(image)
                else:
                    player_images[player_name] = None
        return player_images

    def load_logo_image(self, logo_name: str) -> PhotoImage | None:
        """
        Load the image of a logo.

        Args:
            logo_name (str): The name of the logo.

        Returns:
            PhotoImage | None: The loaded logo image, or None if not found.
        """
        photo_file = f"{logo_name}.png"
        image_path = os.path.join(self.logo_image_directory, photo_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            return ImageTk.PhotoImage(image)
        else:
            print(f"Image not found for logo: {logo_name}")
            return None
