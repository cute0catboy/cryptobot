from datetime import datetime, timedelta
import time
from dataclasses import dataclass

@dataclass
class Time:
    nanoseconds: int
    time: str
    date: str

class TimeGet:

    def __init__(self):
        self.ns_in_hour = 3_600_000_000_000
        self.now = self.get_now()

    def get_time(self, h: int) -> Time: #скорее всего единственная функция которая в будущем тут останется неизменной, остальные по любому переделаю
        hh = self.getdeltatime_time(h)
        dd = self.getdeltatime_date(h)
        nn = time.time_ns() - self.ns_in_hour * h
        return Time(nn, hh, dd)
        # (nanoseconds, (date, time))

    def get_now(self) -> datetime:
        return datetime.now()

    def getdeltatime_time(self, h: int) -> str:
        delta = self.now - timedelta(hours=h)
        return delta.strftime("%H:%M:%S")

    def getdeltatime_date(self, h: int) -> str:
        delta = self.now - timedelta(hours=h)
        return delta.strftime("%d.%m.%Y")