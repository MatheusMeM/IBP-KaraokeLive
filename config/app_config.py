# IBP-KaraokeLive Configuration
# Phase 0: Base configuration adapted from Interactive Stand Game

# =============================================================================
# WINDOW CONFIGURATION (HORIZONTAL LAYOUT FOR WINDOWS 11 MINI-PC)
# =============================================================================
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FULLSCREEN = True  # Set to False for development, True for production
BORDERLESS = True  # Kiosk mode

# =============================================================================
# FILE PATHS
# =============================================================================
LEADERBOARD_FILE = "data/leaderboard.json"

# =============================================================================
# UI COLORS (IBP BRANDING)
# =============================================================================
# Primary colors from Interactive Stand
COLOR_PRIMARY_BLUE = (0/255, 64/255, 119/255, 1)  # #004077
COLOR_PRIMARY_GREEN = (134/255, 188/255, 37/255, 1)  # #86BC25
COLOR_LIGHT_GRAY = (216/255, 206/255, 205/255, 1)  # #D8CECD
COLOR_DARK_GRAY = (137/255, 137/255, 137/255, 1)  # #898989

# =============================================================================
# TIMING CONFIGURATION
# =============================================================================
INSTRUCTIONS_DURATION = 5.0  # seconds
IDLE_TIMEOUT = 60.0  # seconds before returning to welcome screen

# =============================================================================
# DEVELOPMENT FLAGS
# =============================================================================
DEBUG_MODE = True  # Set to False for production