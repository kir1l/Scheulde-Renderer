from PIL import Image, ImageDraw, ImageFont
import textwrap
from models import WeekSchedule, DaySchedule, Lesson

class ScheduleRenderer:
    def __init__(self, scale_factor=3):
        # Масштабный коэффициент для настройки общего размера изображения
        self.scale_factor = scale_factor

        # Внутренний отступ в ячейках таблицы
        self.cell_padding = 20 * scale_factor

        # Базовая высота ячейки
        self.base_cell_height = 60 * scale_factor

        # Ширина ячейки
        self.cell_width = 180 * scale_factor

        # Размер основного шрифта
        self.font_size = 18 * scale_factor

        # Размер шрифта для заголовков
        self.title_font_size = 24 * scale_factor

        # Внешний отступ от краев изображения
        self.margin = 40 * scale_factor

        # Расстояние между блоками дней недели
        self.day_spacing = 40 * scale_factor

        # Цветовая схема
        self.background_color = 'white'        # Цвет фона
        self.header_color = '#1e88e5'         # Цвет заголовков (синий)
        self.header_text_color = 'white'      # Цвет текста в заголовках
        self.text_color = '#333333'           # Цвет основного текста (темно-серый)
        self.border_color = '#e3f2fd'         # Цвет границ (светло-синий)
        
        self.load_fonts()

    def load_fonts(self):
        try:
            self.font = ImageFont.truetype("arial.ttf", self.font_size)
            self.font_bold = ImageFont.truetype("arialbd.ttf", self.font_size)
            self.title_font = ImageFont.truetype("arialbd.ttf", self.title_font_size)
        except:
            self.font = ImageFont.load_default()
            self.font_bold = ImageFont.load_default()
            self.title_font = ImageFont.load_default()

    def get_wrapped_text_height(self, text, max_width):
        lines = textwrap.wrap(text, width=int(max_width/(self.font_size/2)))
        line_height = self.font_size + 4 * self.scale_factor
        return lines, line_height * len(lines)

    def render_week_schedule(self, week_schedule: WeekSchedule, filename: str):
        columns = ['Время', 'Предмет', 'Аудитория', 'Преподаватель', 'Тип']
        
        # Рассчитываем общую высоту
        total_height = self.margin * 2
        for day in week_schedule.days:
            total_height += self.base_cell_height  # День недели
            total_height += self.base_cell_height  # Заголовки колонок
            for lesson in day.lessons:
                max_height = self.base_cell_height
                lesson_data = [
                    f"{lesson.start}-{lesson.end}",
                    lesson.name,
                    str(lesson.classroom),
                    lesson.teacher,
                    lesson.type
                ]
                for value in lesson_data:
                    _, text_height = self.get_wrapped_text_height(
                        str(value), 
                        self.cell_width - self.cell_padding * 2
                    )
                    max_height = max(max_height, text_height + self.cell_padding * 2)
                total_height += max_height
            total_height += self.day_spacing

        # Создаем изображение
        width = (self.cell_width * len(columns)) + (self.margin * 2)
        image = Image.new('RGB', (width, total_height), self.background_color)
        draw = ImageDraw.Draw(image)

        current_y = self.margin
        
        # Рендерим каждый день
        for day in week_schedule.days:
            # Заголовок дня
            text_bbox = draw.textbbox((0, 0), day.day.value, font=self.title_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            draw.text((text_x, current_y), day.day.value, 
                     fill=self.text_color, font=self.title_font)
            current_y += self.base_cell_height

            # Рендерим таблицу дня
            current_y = self.render_day_schedule(
                draw, day, columns, current_y, width
            )
            current_y += self.day_spacing

        image.save(filename, dpi=(300, 300), quality=95)

    def render_day_schedule(self, draw, day: DaySchedule, columns, start_y, width):

        current_y = start_y
        
        # Заголовки колонок
        for col_idx, col_name in enumerate(columns):
            x = (col_idx * self.cell_width) + self.margin
            draw.rectangle([
                x, current_y, 
                x + self.cell_width, current_y + self.base_cell_height
            ], fill=self.header_color)
            
            text_bbox = draw.textbbox((0, 0), col_name, font=self.font_bold)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = x + (self.cell_width - text_width) // 2
            text_y = current_y + (self.base_cell_height - (text_bbox[3] - text_bbox[1])) // 2
            draw.text((text_x, text_y), col_name, 
                     fill=self.header_text_color, font=self.font_bold)

        current_y += self.base_cell_height

        # Данные уроков
        for lesson in day.lessons:
            row_height = self.base_cell_height
            lesson_data = [
                f"{lesson.start}-{lesson.end}",
                lesson.name,
                str(lesson.classroom),
                lesson.teacher,
                lesson.type
            ]
            
            # Определяем высоту строки
            for value in lesson_data:
                _, text_height = self.get_wrapped_text_height(
                    str(value), 
                    self.cell_width - self.cell_padding * 2
                )
                row_height = max(row_height, text_height + self.cell_padding * 2)

            # Рендерим строку
            for col_idx, value in enumerate(lesson_data):
                x = (col_idx * self.cell_width) + self.margin
                
                if col_idx > 0:
                    draw.line([
                        (x, current_y), 
                        (x, current_y + row_height)
                    ], fill=self.border_color, width=self.scale_factor)

                lines, _ = self.get_wrapped_text_height(
                    str(value), 
                    self.cell_width - self.cell_padding * 2
                )
                
                line_height = self.font_size + 4 * self.scale_factor
                total_text_height = line_height * len(lines)
                text_y = current_y + (row_height - total_text_height) // 2

                for line in lines:
                    text_bbox = draw.textbbox((0, 0), line, font=self.font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_x = x + (self.cell_width - text_width) // 2
                    draw.text((text_x, text_y), line, 
                            fill=self.text_color, font=self.font)
                    text_y += line_height

            draw.line([
                (self.margin, current_y), 
                (width - self.margin, current_y)
            ], fill=self.border_color, width=self.scale_factor)
            
            current_y += row_height

        return current_y

    def render_single_day(self, day_schedule: DaySchedule, filename: str):
      columns = ['Время', 'Предмет', 'Аудитория', 'Преподаватель', 'Тип']
      
      # Рассчитываем высоту
      total_height = self.margin * 2 + self.base_cell_height * 2  # Margins + Title + Headers
      
      for lesson in day_schedule.lessons:
         max_height = self.base_cell_height
         lesson_data = [
               f"{lesson.start}-{lesson.end}",
               lesson.name,
               str(lesson.classroom),
               lesson.teacher,
               lesson.type
         ]
         for value in lesson_data:
               _, text_height = self.get_wrapped_text_height(
                  str(value), 
                  self.cell_width - self.cell_padding * 2
               )
               max_height = max(max_height, text_height + self.cell_padding * 2)
         total_height += max_height

      # Создаем изображение
      width = (self.cell_width * len(columns)) + (self.margin * 2)
      image = Image.new('RGB', (width, total_height), self.background_color)
      draw = ImageDraw.Draw(image)

      # Рендерим заголовок дня
      text_bbox = draw.textbbox((0, 0), day_schedule.day.value, font=self.title_font)
      text_width = text_bbox[2] - text_bbox[0]
      text_x = (width - text_width) // 2
      draw.text((text_x, self.margin), day_schedule.day.value, 
               fill=self.text_color, font=self.title_font)

      # Рендерим таблицу
      self.render_day_schedule(
         draw, 
         day_schedule, 
         columns, 
         self.margin + self.base_cell_height, 
         width
      )

      image.save(filename, dpi=(300, 300), quality=95)
