import os
from PIL import Image, ImageTk


class ImageLoader:
    def __init__(self, player_image_directory='Images/Faces', logo_image_directory='Images/Logos'):
        self.player_image_directory = player_image_directory
        self.logo_image_directory = logo_image_directory

    def load_player_image(self, player_name):

        photo_file = f"{player_name.replace(' ', '_')}.png"
        image_path = os.path.join(self.player_image_directory, photo_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            return ImageTk.PhotoImage(image)
        else:
            print(f"Image not found for player: {player_name}")
            return None

    def load_logo_image(self, logo_name):
        photo_file = f"{logo_name}.png"
        image_path = os.path.join(self.logo_image_directory, photo_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            return ImageTk.PhotoImage(image)
        else:
            print(f"Image not found for logo: {logo_name}")
            return None
