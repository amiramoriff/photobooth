import pygame
import qrcode
import time
import sys
from source import config

class GraphicsManager:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        if config.FULLSCREEN:
            # set the display mode to fullscreen
            # and sets config screen size to the actual screen size
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT = self.screen.get_size()

        else:
            # windowed mode
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        pygame.display.set_caption("Photobooth!")

        self.img1 =self._load_and_scale_image(config.IMG_TOUCH_1)
        self.img2 = self._load_and_scale_image(config.IMG_TOUCH_2)

        self.plaid_bg = self._load_and_scale_image(config.IMG_PLAID_BG)
        self.qr_bg = self._load_and_scale_image(config.IMG_QR_BACKGROUND)
        self.img_printing_1 = self._load_and_scale_image(config.IMG_PRINTING_1)
        self.img_printing_2 = self._load_and_scale_image(config.IMG_PRINTING_2)
        self.img_thanks = self._load_and_scale_image(config.IMG_THANKS)
        self.img_error_bg = self._load_and_scale_image(config.IMG_ERROR_BG)

        self.btn_colour_img = self._load_png(config.IMG_BTN_COLOUR)
        self.btn_bw_img = self._load_png(config.IMG_BTN_BW)
        self.btn_print_yes_img = self._load_png(config.IMG_BTN_PRINT_YES)
        self.btn_print_no_img = self._load_png(config.IMG_BTN_PRINT_NO)
        self.btn_try_again_img = self._load_png(config.IMG_BTN_TRY_AGAIN)
        self.btn_skip_img = self._load_png(config.IMG_BTN_SKIP)

        btn_size = (config.BTN_WIDTH, config.BTN_HEIGHT)
        self.btn_two_strips_img = pygame.transform.scale(self._load_png(config.IMG_BTN_TWO_STRIPS), btn_size)
        self.btn_four_strips_img = pygame.transform.scale(self._load_png(config.IMG_BTN_FOUR_STRIPS), btn_size)
        self.two_strips_btn_rect = self.btn_two_strips_img.get_rect(topleft=config.BTN_TWO_STRIPS_POS)
        self.four_strips_btn_rect = self.btn_four_strips_img.get_rect(topleft=config.BTN_FOUR_STRIPS_POS)

        self.btn_colour_img = pygame.transform.scale(self.btn_colour_img, btn_size)
        self.btn_bw_img = pygame.transform.scale(self.btn_bw_img, btn_size)
        self.btn_print_yes_img = pygame.transform.scale(self.btn_print_yes_img, btn_size)
        self.btn_print_no_img = pygame.transform.scale(self.btn_print_no_img, btn_size)
        self.btn_try_again_img = pygame.transform.scale(self.btn_try_again_img, btn_size)
        self.btn_skip_img = pygame.transform.scale(self.btn_skip_img, btn_size)

        self.colour_btn_rect = self.btn_colour_img.get_rect(topleft=config.BTN_COLOUR_POS)
        self.bw_btn_rect = self.btn_bw_img.get_rect(topleft=config.BTN_BW_POS)
        self.print_yes_btn_rect = self.btn_print_yes_img.get_rect(topleft=config.BTN_PRINT_YES_POS)
        self.print_no_btn_rect = self.btn_print_no_img.get_rect(topleft=config.BTN_PRINT_NO_POS)
        self.try_again_btn_rect = self.btn_try_again_img.get_rect(topleft=config.BTN_TRY_AGAIN_POS)
        self.skip_btn_rect = self.btn_skip_img.get_rect(topleft=config.BTN_SKIP_POS)

        exit_full_img = self._load_png(config.IMG_BTN_EXIT)
        exit_cropped_img = exit_full_img.subsurface(pygame.Rect(*config.EXIT_IMG_CROP_RECT))
        self.btn_exit_img = pygame.transform.smoothscale(exit_cropped_img, config.EXIT_BTN_SIZE)
        self.exit_btn_rect = self.btn_exit_img.get_rect(topleft=config.EXIT_BTN_POS)

        self.status_font = pygame.font.SysFont(None, 36)

        self.countdown_imgs = [self._load_png(path) for path in config.COUNTDOWN_IMAGES]

        self.last_toggle_time = time.time()
        self.show_first_image = True

        self.printing_last_toggle_time = time.time()
        self.show_printing_first = True

    def _load_and_scale_image(self, path):
        # Used for full screen background images (JPGs)
        # uses .convert() (no alpha channel) and force scales to fit screen size

        try:
            img = pygame.image.load(path).convert()
            return pygame.transform.scale(img, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        except pygame.error as e:
            # Hard exit on error
            print(f"Error loading image {path}: {e}")
            pygame.quit()
            sys.exit(1)

    def _load_png(self, path):
        # Used for buttons and countdown numbers (PNGs)
        # uses .convert_alpha() to preserve transparency
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading countdown PNG image {path}: {e}")
            pygame.quit()
            sys.exit(1)

    def _draw_exit_button(self):
        self.screen.blit(self.btn_exit_img, self.exit_btn_rect)

    def draw_touch_to_start(self):
        """ Draws the touch to start screen, alternating between two images """

        current_time = time.time()
        if current_time - self.last_toggle_time >= config.ANIMATION_INTERVAL:
            self.show_first_image = not self.show_first_image
            self.last_toggle_time = current_time

        active_image = self.img1 if self.show_first_image else self.img2
        self.screen.blit(active_image, (0, 0))

        self._draw_exit_button()
        pygame.display.flip()

    def draw_select_filter(self):
        self.screen.blit(self.plaid_bg, (0, 0))
        self.screen.blit(self.btn_colour_img, self.colour_btn_rect)
        self.screen.blit(self.btn_bw_img, self.bw_btn_rect)
        self._draw_exit_button()
        pygame.display.flip()

    def draw_confirm_print(self):
        self.screen.blit(self.plaid_bg, (0, 0))
        self.screen.blit(self.btn_print_yes_img, self.print_yes_btn_rect)
        self.screen.blit(self.btn_print_no_img, self.print_no_btn_rect)
        self._draw_exit_button()
        pygame.display.flip()

    def draw_select_copies(self):
        self.screen.blit(self.plaid_bg, (0, 0))
        self.screen.blit(self.btn_two_strips_img, self.two_strips_btn_rect)
        self.screen.blit(self.btn_four_strips_img, self.four_strips_btn_rect)
        self._draw_exit_button()
        pygame.display.flip()

    def draw_countdown(self, camera_surface, number_index):
        self.screen.blit(camera_surface, (0, 0))

        if 0 <= number_index < len(self.countdown_imgs):
            num_img = self.countdown_imgs[number_index]
            rect = num_img.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(num_img, rect)

        self._draw_exit_button()
        pygame.display.flip()

    def draw_flash(self):
        self.screen.fill((255, 255, 255))
        self._draw_exit_button()
        pygame.display.flip()

    def build_qr_surface(self, data, target_size=190):
        qr = qrcode.QRCode(border=2, box_size=10)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        mode = qr_img.mode
        size = qr_img.size
        raw = qr_img.tobytes()
        surface = pygame.image.fromstring(raw, size, mode)
        return pygame.transform.smoothscale(surface, (target_size, target_size))

    def draw_qr(self, qr_surface):
        self.screen.blit(self.qr_bg, (0, 0))

        qr_rect = qr_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(qr_surface, qr_rect)

        self._draw_exit_button()
        pygame.display.flip()

    def _draw_text_box(self, text, center, max_width, text_color=(255, 255, 255), box_color=(0, 0, 0, 160)):
        # Word-wraps text to max_width and draws it on a semi-transparent box, centered at `center`.
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            candidate = f"{current_line} {word}".strip()
            if self.status_font.size(candidate)[0] <= max_width or not current_line:
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        line_surfaces = [self.status_font.render(line, True, text_color) for line in lines]
        line_height = self.status_font.get_linesize()
        box_width = max((s.get_width() for s in line_surfaces), default=0) + 40
        box_height = line_height * len(line_surfaces) + 30

        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surface.fill(box_color)
        box_rect = box_surface.get_rect(center=center)
        self.screen.blit(box_surface, box_rect)

        for i, line_surface in enumerate(line_surfaces):
            line_rect = line_surface.get_rect(
                center=(center[0], box_rect.top + 15 + line_height * i + line_height // 2)
            )
            self.screen.blit(line_surface, line_rect)

    def draw_printing(self, progress_text=None):
        current_time = time.time()
        if current_time - self.printing_last_toggle_time >= config.ANIMATION_INTERVAL:
            self.show_printing_first = not self.show_printing_first
            self.printing_last_toggle_time = current_time

        active_image = self.img_printing_1 if self.show_printing_first else self.img_printing_2
        self.screen.blit(active_image, (0, 0))

        if progress_text:
            self._draw_text_box(
                progress_text,
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50),
                max_width=config.ERROR_MSG_MAX_WIDTH,
            )

        self._draw_exit_button()
        pygame.display.flip()

    def draw_print_error_message(self, message):
        self.screen.blit(self.img_error_bg, (0, 0))

        self._draw_text_box(
            message,
            center=config.ERROR_MSG_CENTER,
            max_width=config.ERROR_MSG_MAX_WIDTH,
        )

        self._draw_exit_button()
        pygame.display.flip()

    def draw_print_error_action(self):
        self.screen.blit(self.plaid_bg, (0, 0))

        self.screen.blit(self.btn_try_again_img, self.try_again_btn_rect)
        self.screen.blit(self.btn_skip_img, self.skip_btn_rect)

        self._draw_exit_button()
        pygame.display.flip()

    def draw_thanks(self):
        self.screen.blit(self.img_thanks, (0, 0))
        self._draw_exit_button()
        pygame.display.flip()
