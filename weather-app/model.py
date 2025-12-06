from dataclasses import dataclass
from datetime import datetime as dt

@dataclass
class Coordinates:
    latitude: float
    longitude: float

    def coordinates(self):
        return f'{self.latitude},{self.longitude}'

@dataclass
class Weather:
    date: dt
    details: dict
    temp: str
    weather: str
    description: str

    def __str__(self):
        return f"{self.date:%H:%M} {self.temp}C {self.description}"