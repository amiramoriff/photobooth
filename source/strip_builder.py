import os
import time
from PIL import Image, ImageFont, ImageDraw
import numpy as np 
from source import config

class StripBuilder:
    def __init__(self):
        self.canvas_w = config.STRIP_CANVAS_WIDTH
        self.canvas_h = config.STRIP_CANVAS_HEIGHT
        self.bg_color = config.STRIP_BG_COLOR
        self.output_dir = config.OUTPUT_DIR

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def _apply_filter(self, img, filter_type):
        if filter_type == "bw":
            return img.convert("L").convert("RGB")
        return img

    def build_single_strip(self, captured_photos, filter_type="colour", strip_width=None, strip_height=None):
        strip_width = strip_width or self.canvas_w // 2
        strip_height = strip_height or self.canvas_h

        strip = Image.new('RGB', (strip_width, strip_height), self.bg_color)
        draw = ImageDraw.Draw(strip)

        margin_side = 20
        margin_top = 20
        gap = 15
        footer_space = 140

        available_height = strip_height - margin_top - footer_space - (gap * 2)
        target_photo_w = strip_width - (margin_side * 2)
        target_photo_h = available_height // 3

        for i, photo_array in enumerate(captured_photos[:3]):
            if isinstance(photo_array, np.ndarray):
                img = Image.fromarray(photo_array)
            else:
                img = photo_array

            img = self._apply_filter(img, filter_type)

            img_aspect = img.width / img.height
            target_aspect = target_photo_w / target_photo_h

            if img_aspect > target_aspect:
                new_w = int(img.height * target_aspect)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))

            else:
                new_h = int(img.width / target_aspect)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))

            img = img.resize((target_photo_w, target_photo_h), Image.Resampling.LANCZOS)

            y_pos = margin_top + i * (target_photo_h + gap)
            strip.paste(img, (margin_side, y_pos))

        date_str = time.strftime("%Y-%m-%d %H:%M:%S")
        dark_amber = (153, 82, 0)

        try:
            font_date = ImageFont.truetype(config.FONT_DATE_PATH, 48)
        except IOError:
            font_date = ImageFont.load_default()

        footer_center_y = strip_height - (footer_space // 2)
        draw.text((strip_width // 2, footer_center_y), date_str, fill=dark_amber, font=font_date, anchor="mm")

        return strip

    def build_print_sheet(self, captured_photos, filter_type="colour"):
        single_strip = self.build_single_strip(captured_photos, filter_type=filter_type)
        strip_width = single_strip.width

        full_sheet = Image.new('RGB', (self.canvas_w, self.canvas_h), self.bg_color)
        full_sheet.paste(single_strip, (0, 0))
        full_sheet.paste(single_strip, (strip_width, 0))

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        strip_filepath = os.path.join(self.output_dir, f"strip_{timestamp}.jpg")
        sheet_filepath = os.path.join(self.output_dir, f"sheet_{timestamp}.jpg")

        single_strip.save(strip_filepath, quality=95)
        full_sheet.save(sheet_filepath, quality=95)

        print(f"Photostrip saved: {strip_filepath}")
        print(f"Print sheet saved: {sheet_filepath}")

        return sheet_filepath, strip_filepath


    