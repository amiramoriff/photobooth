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

        self.btn_colour_img = self._load_png(config.IMG_BTN_COLOUR)
        self.btn_bw_img = self._load_png(config.IMG_BTN_BW)
        self.btn_print_yes_img = self._load_png(config.IMG_BTN_PRINT_YES)
        self.btn_print_no_img = self._load_png(config.IMG_BTN_PRINT_NO)

        btn_size = (config.BTN_WIDTH, config.BTN_HEIGHT)
        self.btn_colour_img = pygame.transform.scale(self.btn_colour_img, btn_size)
        self.btn_bw_img = pygame.transform.scale(self.btn_bw_img, btn_size)
        self.btn_print_yes_img = pygame.transform.scale(self.btn_print_yes_img, btn_size)
        self.btn_print_no_img = pygame.transform.scale(self.btn_print_no_img, btn_size)

        self.colour_btn_rect = self.btn_colour_img.get_rect(topleft=config.BTN_COLOUR_POS)
        self.bw_btn_rect = self.btn_bw_img.get_rect(topleft=config.BTN_BW_POS)
        self.print_yes_btn_rect = self.btn_print_yes_img.get_rect(topleft=config.BTN_PRINT_YES_POS)
        self.print_no_btn_rect = self.btn_print_no_img.get_rect(topleft=config.BTN_PRINT_NO_POS)

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

    def draw_touch_to_start(self):
        """ Draws the touch to start screen, alternating between two images """

        current_time = time.time()
        if current_time - self.last_toggle_time >= config.ANIMATION_INTERVAL:
            self.show_first_image = not self.show_first_image
            self.last_toggle_time = current_time

        active_image = self.img1 if self.show_first_image else self.img2
        self.screen.blit(active_image, (0, 0))

        pygame.display.flip()

    def draw_select_filter(self):
        self.screen.blit(self.plaid_bg, (0, 0))
        self.screen.blit(self.btn_colour_img, self.colour_btn_rect)
        self.screen.blit(self.btn_bw_img, self.bw_btn_rect)
        pygame.display.flip()

    def draw_confirm_print(self):
        self.screen.blit(self.plaid_bg, (0, 0))
        self.screen.blit(self.btn_print_yes_img, self.print_yes_btn_rect)
        self.screen.blit(self.btn_print_no_img, self.print_no_btn_rect)
        pygame.display.flip()

    def draw_countdown(self, camera_surface, number_index):
        self.screen.blit(camera_surface, (0, 0))

        if 0 <= number_index < len(self.countdown_imgs):
            num_img = self.countdown_imgs[number_index]
            rect = num_img.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(num_img, rect)

        pygame.display.flip()

    def draw_flash(self):
        self.screen.fill((255, 255, 255))
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

        pygame.display.flip()

    def draw_printing(self):
        current_time = time.time()
        if current_time - self.printing_last_toggle_time >= config.ANIMATION_INTERVAL:
            self.show_printing_first = not self.show_printing_first
            self.printing_last_toggle_time = current_time

        active_image = self.img_printing_1 if self.show_printing_first else self.img_printing_2
        self.screen.blit(active_image, (0, 0))

        pygame.display.flip()

    def draw_thanks(self):
        self.screen.blit(self.img_thanks, (0, 0))
        pygame.display.flip()
