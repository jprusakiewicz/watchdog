from datetime import datetime, timedelta


class Player:
    def __init__(self, id: str):
        self.id: str = id
        self.timestamp: datetime = datetime.now()
        self.timeout: int = 47

    def renew_timeout(self):
        self.timestamp = datetime.now() + timedelta(0, self.timeout)

    def is_overdue(self) -> bool:
        if self.timestamp <= datetime.now():
            return True
        return False