import logging
from typing import List
from urllib.parse import urljoin

import requests

from app.logger import setup_custom_logger
from app.models import ServerScan, RoomScan, PlayersLocation

logger = setup_custom_logger('scanner')

class Scanner:
    def __init__(self, servers):
        self.servers = servers
        self.scans: List[ServerScan] = []

    def scan(self):
        self.scans = self.scan_servers()

    def scan_servers(self):
        servers_scans = []
        for server in self.servers:
            rooms = self.get_rooms(server)
            rooms_scans = self.scan_rooms(server, rooms)
            servers_scans.append(ServerScan(server, rooms_scans))
        return servers_scans

    def scan_rooms(self, server_path: str, rooms: List[str]):
        rooms_scans = []
        for room in rooms:
            players = self.get_players(server_path, room)
            rooms_scans.append(RoomScan(room, players))
        return rooms_scans

    def get_players_location(self, player_id) -> PlayersLocation:
        for server in self.scans:
            for room in server.rooms:
                if player_id in room.players:
                    return PlayersLocation(room.room_id, server.server_path)

    @staticmethod
    def get_rooms(server):
        server_address = urljoin(server, "stats")
        try:
            general_server_stats = requests.get(server_address).json()
            rooms = general_server_stats["rooms_ids"]
        except (requests.exceptions.ConnectionError, KeyError):
            logger.log(30, f"ConnectionError: {server_address}")
            rooms = []
        return rooms

    @staticmethod
    def get_players(server, room):
        room_stats = requests.get(urljoin(server, f"stats"), params={"room_id": room}).json()
        players_in_room: List[str] = room_stats["players_ids"]
        return players_in_room

    def is_in_game(self, player_id):
        for server in self.scans:
            for room in server.rooms:
                if player_id in room.players:
                    return True
        return False
