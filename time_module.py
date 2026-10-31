from datetime import datetime, timedelta

class TimeGet: #("29.10.2026", "15:56:08") у любого временного промежутка

    def __init__(self):
        self.now = self.get_now()
        self.current = self.getdeltatime(0)
        self.hour = self.getdeltatime(1)
        self.day = self.getdeltatime(24)

    def get_now(self) -> datetime:
        return datetime.now()

    def getdeltatime(self, h: int) -> tuple:
        delta = self.now - timedelta(hours=h)
        return (delta.strftime("%d.%m.%Y"), delta.strftime("%H:%M:%S"))