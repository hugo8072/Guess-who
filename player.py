# player.py
class Player:
    def __init__(self, name, team, hair_color, hair_length, skin_color, continent, goals, assists, position):
        self.name = name
        self.team = team
        self.hair_color = hair_color
        self.hair_length = hair_length
        self.skin_color = skin_color
        self.continent = continent
        self.goals = goals
        self.assists = assists
        self.position = position

    def __str__(self):
        return (f"Player(name={self.name},team={self.team}, hair_color={self.hair_color},"
                f" hair_length={self.hair_length}, skin_color={self.skin_color}, continent={self.continent}, "
                f"goals={self.goals}, assists={self.assists}, position={self.position})")
