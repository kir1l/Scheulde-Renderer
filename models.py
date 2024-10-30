from dataclasses import dataclass
from typing import Union, List
from enum import Enum

class WeekDay(Enum):
    MONDAY = "Понедельник"
    TUESDAY = "Вторник"
    WEDNESDAY = "Среда"
    THURSDAY = "Четверг"
    FRIDAY = "Пятница"
    SATURDAY = "Суббота"

@dataclass
class Lesson:
    start: str
    end: str
    name: str
    classroom: Union[str, int]
    teacher: str
    type: str

@dataclass
class DaySchedule:
    day: WeekDay
    lessons: List[Lesson]

class WeekSchedule:
    def __init__(self):
        self.days: List[DaySchedule] = []
    
    def add_day(self, day_schedule: DaySchedule):
        self.days.append(day_schedule)
