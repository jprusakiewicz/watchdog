from dataclasses import dataclass
from typing import List


@dataclass
class RoomScan:
    room_id: str
    players: List[str]


@dataclass
class ServerScan:
    server_path: str
    rooms: List[RoomScan]


@dataclass
class PlayersLocation:
    room_id: str
    server_path: str
