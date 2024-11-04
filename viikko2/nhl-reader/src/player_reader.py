import requests
from player import Player

class PlayerReader:
    def __init__(self, url):
        self.url = url
        self.players = []

    def get_players(self, season):
        response = requests.get(f"{self.url}/{season}/players").json()
        self.players = [Player(player_dict) for player_dict in response]
        return self.players

