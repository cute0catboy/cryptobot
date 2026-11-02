from datetime import datetime, timedelta
import time

class TimeGet:

    def __init__(self):
        self.ns_in_hour = 3_600_000_000_000
        self.now = self.get_now()

        self.ns_time = time.time_ns()
        self.ns_time_hour = time.time_ns() - self.ns_in_hour
        self.ns_time_day = time.time_ns() - self.ns_in_hour*24

        self.current = self.getdeltatime(0)
        self.hour = self.getdeltatime(1)
        self.day = self.getdeltatime(24)

    def get_now(self) -> datetime:
        return datetime.now()

    def getdeltatime(self, h: int) -> tuple:
        delta = self.now - timedelta(hours=h)
        return (delta.strftime("%d.%m.%Y"), delta.strftime("%H:%M:%S"))