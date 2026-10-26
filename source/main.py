import os
import pygame
import sys
import time
from source import config
from source.graphics import GraphicsManager
from source.camera import CameraManager
from source.strip_builder import StripBuilder
from source.printer import PrinterManager
from source.uploader import Uploader

def main():

    # Initialise manager classes
    graphics = GraphicsManager()
    camera = CameraManager()
    strip_builder = StripBuilder()
    printer = PrinterManager(printer_name="SELPHY")
    uploader = Uploader()

    # Initialise loop-state variables
    clock = pygame.time.Clock()
    state = "TOUCH_TO_START"
    running = True

    countdown_index = 0
    countdown_step_start = 0
    flash_start_time = 0
    photo_count = 0
    captured_photos = []
    selected_filter = "colour"
    pending_sheet_path = None
    pending_strip_path = None
    qr_surface = None
    printing_start_time = 0
    thanks_start_time = 0

    def cleanup_pending_files():
        # Delete temporary sheet / strip JPG files
        nonlocal pending_sheet_path, pending_strip_path
        for path in (pending_strip_path, pending_sheet_path):
            if path and os.path.exists(path):
                os.remove(path)
        pending_strip_path = None
        pending_sheet_path = None

    while running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if state == "TOUCH_TO_START":
                    state = "SELECT_FILTER"
                    camera.start()

                elif state == "SELECT_FILTER":
                    hit_filter = None
                    if graphics.colour_btn_rect.collidepoint(pos):
                        hit_filter = "colour"
                    elif graphics.bw_btn_rect.collidepoint(pos):
                        hit_filter = "bw"

                    if hit_filter:
                        selected_filter = hit_filter
                        state = "COUNTDOWN"
                        countdown_index = 0
                        countdown_step_start = time.time()
                        photo_count = 0
                        captured_photos = []

                elif state == "SHOW_QR":
                    qr_surface = None
                    state = "CONFIRM_PRINT"

                elif state == "CONFIRM_PRINT":
                    if graphics.print_yes_btn_rect.collidepoint(pos):
                        print("Sending to printer")
                        printer.print_file(pending_sheet_path)

                        printing_start_time = current_time
                        state = "PRINTING"

                    elif graphics.print_no_btn_rect.collidepoint(pos):
                        print("Printing skipped by user")
                        cleanup_pending_files()

                        thanks_start_time = current_time
                        state = "THANKS"

        if state == "TOUCH_TO_START":
             graphics.draw_touch_to_start()

        elif state == "SELECT_FILTER":
            graphics.draw_select_filter()

        elif state == "COUNTDOWN":
            if current_time - countdown_step_start >= config.COUNTDOWN_STEP_TIME:
                countdown_index += 1
                countdown_step_start = current_time

            if countdown_index >= len(config.COUNTDOWN_IMAGES):
                state = "FLASH"
                flash_start_time = current_time

                photo = camera.capture_frame()
                captured_photos.append(photo)
                photo_count += 1
                print(f"Captured photo {photo_count} of {config.TOTAL_PHOTOS}!")
            else:
                cam_surface = camera.get_preview_surface(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
                graphics.draw_countdown(cam_surface, countdown_index)

        elif state == "FLASH":
            if current_time - flash_start_time < config.FLASH_DURATION:
                graphics.draw_flash()
            else:
                if photo_count < config.TOTAL_PHOTOS:
                    state = "COUNTDOWN"
                    countdown_index = 0
                    countdown_step_start = time.time()
                else:
                    camera.stop()
                    pending_sheet_path, pending_strip_path = strip_builder.build_print_sheet(
                        captured_photos,
                        filter_type = selected_filter
                    )

                    photo_count = 0
                    captured_photos = []

                    qr_surface = None
                    try:
                        key = os.path.basename(pending_strip_path)
                        download_url = uploader.upload_and_get_link(
                            pending_strip_path, key, config.DOWNLOAD_LINK_EXPIRY_SECONDS
                        )
                        qr_surface = graphics.build_qr_surface(download_url)
                    except Exception as e:
                        print(f"Upload failed: {e}")

                    state = "SHOW_QR" if qr_surface is not None else "CONFIRM_PRINT"

        elif state == "SHOW_QR":
            graphics.draw_qr(qr_surface)

        elif state == "CONFIRM_PRINT":
            graphics.draw_confirm_print()

        elif state == "PRINTING":
            graphics.draw_printing()
            if current_time - printing_start_time >= config.PRINTING_DURATION:
                cleanup_pending_files()
                thanks_start_time = current_time
                state = "THANKS"

        elif state == "THANKS":
            graphics.draw_thanks()
            if current_time - thanks_start_time >= config.THANKS_DURATION:
                state = "TOUCH_TO_START"

        clock.tick(30 if state in ("COUNTDOWN", "FLASH") else 12)

    camera.stop()
    pygame.quit()
    sys.exit()
