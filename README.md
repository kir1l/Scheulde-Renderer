# Schedule Renderer Module

A powerful Python module for generating beautiful schedule images with customizable styling and high-quality output.

## Features

- Generate schedule tables as high-quality PNG images
- Support for both single day and full week schedules
- Automatic text wrapping and cell sizing
- Clean, minimalist design with customizable colors
- High DPI output for crystal clear rendering
- Built-in support for Russian weekday names

## Installation

1. Install required dependencies:

```bash
pip install pillow
```

2. Clone the repository:

```bash
git clone https://github.com/kir1l/Scheulde-Renderer.git
```

## Usage

Basic example of generating a schedule:

```python
from schedule_renderer.models import Lesson, DaySchedule, WeekDay, WeekSchedule
from schedule_renderer.schedule_renderer import ScheduleRenderer

# Create lessons
lessons = [
    Lesson("09:00", "10:30", "Mathematics", "301", "Smith J.", "Lecture"),
    Lesson("10:40", "12:10", "Programming", "215A", "Johnson B.", "Seminar")
]

# Create day schedule
day_schedule = DaySchedule(WeekDay.MONDAY, lessons)

# Create week schedule
week_schedule = WeekSchedule()
week_schedule.add_day(day_schedule)

# Initialize renderer and generate images
renderer = ScheduleRenderer()
renderer.render_single_day(day_schedule, 'day_schedule.png')
renderer.render_week_schedule(week_schedule, 'week_schedule.png')
```

## Customization

The ScheduleRenderer class accepts various parameters for customization:

- `scale_factor`: scale_factor: Controls overall size of the output image
- Colors can be customized through class properties
- Font sizes and padding are adjustable

## Structure

- `models.py`: Data structures for lessons and schedules
- `schedule_renderer.py`: Main rendering logic
- `main.py`: Usage examples

## Output

- Clean table layout
- Proper text wrapping
- Centered content
- Professional spacing
- Subtle borders
- High DPI for sharp rendering

## Requirements

- Python 3.7+
- Pillow (PIL)
