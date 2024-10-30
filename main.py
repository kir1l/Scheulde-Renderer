from models import Lesson, DaySchedule, WeekDay, WeekSchedule
from schedule_renderer import ScheduleRenderer

def example_usage():
    # Создаем расписание
    week_schedule = WeekSchedule()

    monday_lessons = [
        Lesson("09:00", "10:30", "Математический анализ", "301", "Иванов И.И.", "Лекция"),
        Lesson("10:40", "12:10", "Программирование", "215A", "Петров П.П.", "Семинар")
    ]
    week_schedule.add_day(DaySchedule(WeekDay.MONDAY, monday_lessons))

    tuesday_lessons = [
        Lesson("13:00", "14:30", "Физика", "408", "Сидоров С.С.", "Лекция"),
        Lesson("14:40", "16:10", "Английский язык", "315", "Смирнова А.А.", "Семинар")
    ]
    day_schedule = DaySchedule(WeekDay.TUESDAY, tuesday_lessons)
    week_schedule.add_day(day_schedule)

    # Рендерим расписание
    renderer = ScheduleRenderer()
    renderer.render_week_schedule(week_schedule, 'week_schedule.png')
    renderer.render_single_day(day_schedule, 'day_schedule.png')

if __name__ == "__main__":
    example_usage()
