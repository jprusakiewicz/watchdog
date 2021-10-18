from typing import List, Optional
from urllib.parse import urljoin

import requests

from logger import setup_custom_logger
from .models import PlayersLocation
from .player import Player
from .scanner import Scanner
from .timer import RepeatedTimer

logger = setup_custom_logger('watchdog')


class Watchdog:
    def __init__(self, servers):
        self.timeout = 50
        self.players: List[Player] = []
        self.servers: List = servers
        self.timer = RepeatedTimer(self.timeout,
                                   self.check_for_dead_players)  # it auto-starts, no need of timer.start()
        self.scanner = Scanner(servers)

    def get_stats(self):
        stats = dict(players=self.players,
                     servers=self.servers,
                     scans=[scan.__dict__ for scan in self.scanner.scans]
                     )
        return stats

    def check_for_dead_players(self):
        logger.debug("checking for dead players")
        self.scanner.scan()
        for player in self.players:
            if player.is_overdue():
                if self.scanner.is_in_game(player.id):
                    players_location = self.scanner.get_players_location(player.id)
                    self.remove_player_from_server(players_location, self.get_player(player.id))
                else:
                    self.players.remove(player)

    def handle_player_call(self, player_id):
        player = self.get_player(player_id)
        if player is None:
            player = Player(player_id)
        player.renew_timeout()

        self.players.append(player)

    def get_player(self, player_id) -> Optional[Player]:
        # this method does 2 things: gets and removes; todo refactor extract removing operation
        try:
            player = next(player for player in self.players if player.id == player_id)
            self.players.remove(player)
        except StopIteration:
            player = None
        return player

    @staticmethod
    def remove_player_from_server(players_location: PlayersLocation, player: Player):
        logger.info(f"removing player {player.id} from {players_location.server_path}")
        try:
            requests.post(
                urljoin(players_location.server_path, f"game/kick_player/{players_location.room_id}/{player.id}"))
        except requests.exceptions.ConnectionError:
            pass
