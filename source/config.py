import os

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FULLSCREEN = True
# FULLSCREEN = True means real screensize will be detected at runtime,
# otherwise it will use SCREEN_WIDTH and SCREEN_HEIGHT

# Timings
ANIMATION_INTERVAL = 0.4
COUNTDOWN_STEP_TIME = 1.0
FLASH_DURATION = 0.3
PRINTING_DURATION = 30  # seconds to show the printing animation
THANKS_DURATION = 5  # seconds to show the thank-you screen

# Strip canvas
STRIP_CANVAS_WIDTH = 1200
STRIP_CANVAS_HEIGHT = 1800
STRIP_BG_COLOR = (245, 245, 240)  # off-white

# Photo dimensions and aspect ratio
PHOTO_TARGET_WIDTH = 560
PHOTO_TARGET_HEIGHT = 536
PHOTO_ASPECT_RATIO = PHOTO_TARGET_WIDTH / PHOTO_TARGET_HEIGHT

# Paths
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SOURCE_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# File paths for images
IMG_TOUCH_1 = os.path.join(ASSETS_DIR, "touch-to-start-1.jpg")
IMG_TOUCH_2 = os.path.join(ASSETS_DIR, "touch-to-start-2.jpg")
IMG_PLAID_BG = os.path.join(ASSETS_DIR, "plaid-background.jpg")
IMG_BTN_COLOUR = os.path.join(ASSETS_DIR, "colour-button.png")
IMG_BTN_BW = os.path.join(ASSETS_DIR, "bw-button.png")
IMG_BTN_PRINT_YES = os.path.join(ASSETS_DIR, "print-yes-button.png")
IMG_BTN_PRINT_NO = os.path.join(ASSETS_DIR, "print-no-button.png")
IMG_QR_BACKGROUND = os.path.join(ASSETS_DIR, "qr-code-background.jpg")
COUNTDOWN_IMAGES = [
    os.path.join(ASSETS_DIR, "3.png"),
    os.path.join(ASSETS_DIR, "2.png"),
    os.path.join(ASSETS_DIR, "1.png"),
]
IMG_PRINTING_1 = os.path.join(ASSETS_DIR, "printing-1.jpg")
IMG_PRINTING_2 = os.path.join(ASSETS_DIR, "printing-2.jpg")
IMG_THANKS = os.path.join(ASSETS_DIR, "thanks-for-stopping-by.jpg")
FONT_DATE_PATH = os.path.join(ASSETS_DIR, "DS-DIGIT.TTF")

# Button dimensions and positions
BTN_WIDTH = 380
BTN_HEIGHT = 228
BTN_COLOUR_POS = (SCREEN_WIDTH // 2 - BTN_WIDTH - 20, SCREEN_HEIGHT // 2 - BTN_HEIGHT // 2)
BTN_BW_POS = (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - BTN_HEIGHT // 2)
BTN_PRINT_YES_POS = BTN_COLOUR_POS
BTN_PRINT_NO_POS = BTN_BW_POS

# Misc
TOTAL_PHOTOS = 3
CAMERA_INDEX = 0
DOWNLOAD_LINK_EXPIRY_SECONDS = 3600  # QR download link + R2 copy both expire after 1 hour

