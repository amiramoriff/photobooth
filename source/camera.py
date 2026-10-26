import cv2
import pygame
import numpy as np 
from picamera2 import Picamera2
from source import config

class CameraManager:
    def __init__(self):
        self.picam2 = Picamera2()

        preview_config = self.picam2.create_preview_configuration(
            # higher quality used for capturing photo
            main={"size": (1440, 1080), "format": "RGB888"},

            # lower quality used for live prebire to reduce CPU load
            lores={"size": (640, 480), "format": "YUV420"},
            sensor={
                "output_size": (2304, 1728)
            },
        )
        self.picam2.configure(preview_config)
        self.started = False

    def start(self):
        if not self.started:
            self.picam2.start()
            self.started = True

    def _crop_to_photo_aspect(self, frame_rgb):
        h, w, _ = frame_rgb.shape
        target_aspect = config.PHOTO_ASPECT_RATIO
        current_aspect = w / h

        if current_aspect > target_aspect:
            new_w = int(h * target_aspect)
            x_offset = (w - new_w) // 2
            return frame_rgb[:, x_offset:x_offset + new_w]

        else:
            new_h = int(w / target_aspect)
            y_offset = (h - new_h) // 2
            return frame_rgb[y_offset:y_offset + new_h, :]

    def get_preview_surface(self, target_width, target_height):
        try:
            frame = self.picam2.capture_array("lores")
        except Exception as e:
            print(f"Error capturing frame: {e}")
            surface = pygame.Surface((target_width, target_height))
            surface.fill((0, 0, 0))
            return surface

        frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_I420)
        cropped_frame = self._crop_to_photo_aspect(frame)

        crop_h, crop_w, _ = cropped_frame.shape
        cropped_aspect = crop_w / crop_h
        target_aspect = target_width / target_height

        if target_aspect > cropped_aspect:
            render_h = target_height
            render_w = int(render_h * cropped_aspect)

        else:
            render_w = target_width
            render_h = int(render_w / cropped_aspect)

        frame_resized = cv2.resize(cropped_frame, (render_w, render_h), interpolation=cv2.INTER_LINEAR)

        # convert numpy array directly into pygame surface
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_resized))

        canvas = pygame.Surface((target_width, target_height))
        canvas.fill((0, 0, 0))
        x_offset = (target_width - render_w) // 2
        y_offset = (target_height - render_h) // 2
        canvas.blit(frame_surface, (x_offset, y_offset))

        return canvas

    def capture_frame(self):
        frame = self.picam2.capture_array("main")
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return cv2.flip(frame_rgb, 1)

    def stop(self):
        if self.started:
            self.picam2.stop()
            self.started = False
