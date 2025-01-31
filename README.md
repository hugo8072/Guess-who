# Guess Who Game 🎮 

## Project Overview 📝 
This project is a Python-based implementation of the classic "Guess Who" game. The game allows users to select teams and guess the players based on various attributes. 

## Features ✨ 
- **Player Management**: Manage player attributes such as name, team, hair color, hair length, skin color, continent, goals, assists, and position. 
- **Image Loading**: Load player and team logo images from specified directories. 
- **Game Interface**: User interface for interacting with the game, including username entry and team selection. 
- **CSV Operations**: Read and write user data to a CSV file. 
- **Testing**: Comprehensive tests for game functionality using `pytest`. 

## Technologies Used ⚙️ 
- **Python**: The primary programming language for the project. 
- **PIL (Pillow)**: Library for image processing. 
- **tkinter**: Standard Python interface to the Tk GUI toolkit. 
- **pytest**: Framework for testing Python code. 
- **unittest.mock**: Library for mocking objects in tests. 

## Getting Started 🚀 

### Prerequisites 📦 
- Python 3.x installed on your machine. 
- Required Python packages (listed in `requirements.txt`). 

### Installation 💻 
1. Clone the repository: 
```sh 
git clone https://github.com/hugo8072/Guess-who 
``` 

2. Navigate to the project directory: 
```sh 
cd Guess_Who_Game 
``` 

3. Install the dependencies:
 ```
sh pip install -r requirements.txt 
``` 


### Configuration ⚙️ Ensure the following directory structure for images:

### Configuration
Ensure the following directory structure for images:
Images/ ├── Faces/ │ ├── player1.png │ └── player2.png └── Logos/ ├── team1.png └── team2.png





### Running the Application 🕹️
Start the game:
```sh
python main.py
 ```


###Running Tests 🧪
Run the tests using pytest:

 ```sh
pytest
    
