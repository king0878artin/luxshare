"""Shared configuration for LuxShare."""
APP_NAME = "LuxShare"
APP_VERSION = "1.0.0"
PACKAGE_NAME = "luxshare"

# Transfer limits
MAX_FILE_SIZE = 5 * 1024 * 1024 * 1024  # 5 GiB
CHUNK_SIZE = 1024 * 1024
BUFFER_SIZE = 64 * 1024

# Local-network discovery and transfer
DISCOVERY_PORT = 37020
TRANSFER_PORT = 37021
DISCOVERY_INTERVAL = 2.0
DEVICE_TIMEOUT = 8.0
SERVER_BACKLOG = 10
CONNECTION_TIMEOUT = 30.0
PROTOCOL_VERSION = 1
MAX_HEADER_SIZE = 64 * 1024

# Android
MIN_ANDROID_API = 26
ANDROID_API = 35
RECEIVE_FOLDER_NAME = "Received"

# UI
WINDOW_TITLE = APP_NAME
PADDING = 20
BUTTON_HEIGHT = 58
CORNER_RADIUS = 14
COLORS = {
    "background": (0.035, 0.045, 0.065, 1),
    "surface": (0.075, 0.090, 0.120, 1),
    "surface_light": (0.105, 0.125, 0.165, 1),
    "primary": (0.15, 0.55, 0.95, 1),
    "secondary": (0.12, 0.78, 0.55, 1),
    "text": (0.95, 0.97, 1, 1),
    "muted": (0.55, 0.62, 0.72, 1),
    "danger": (0.95, 0.25, 0.28, 1),
    "white": (1, 1, 1, 1),
}

ALLOW_EMPTY_FILES = True
VERIFY_SHA256 = True
AUTO_RENAME_DUPLICATES = True
DEBUG = False
