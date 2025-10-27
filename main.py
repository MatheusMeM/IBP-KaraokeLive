"""
IBP-KaraokeLive - Main Entry Point
Phase 0: Adapted from Interactive Stand Game for horizontal Windows deployment
"""

import os

# --- KIVY CONFIGURATION (MUST BE BEFORE IMPORTS) ---
from kivy.config import Config

# Import our configuration
from config.app_config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FULLSCREEN, BORDERLESS,
    KEYBOARD_MODE, KEYBOARD_LAYOUT
)

# Set window properties before other Kivy imports
Config.set('graphics', 'width', str(WINDOW_WIDTH))
Config.set('graphics', 'height', str(WINDOW_HEIGHT))
Config.set('graphics', 'fullscreen', 'auto' if FULLSCREEN else '0')
Config.set('graphics', 'borderless', '1' if BORDERLESS else '0')
Config.set('graphics', 'resizable', '0')

# Configure virtual keyboard for touchscreen support
Config.set('kivy', 'keyboard_mode', KEYBOARD_MODE)
Config.set('kivy', 'keyboard_layout', KEYBOARD_LAYOUT)

# Reduce keyboard height to prevent blocking UI elements
# Default is 0.3 (30% of screen), reducing to 25% for 1920x1080
Config.set('kivy', 'keyboard_height', '270')  # 25% of 1080px

# Windows-specific: Use default audio driver (no need for ALSA like Raspberry Pi)
# Note: SDL_AUDIODRIVER environment variable can be set if needed

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.instructions_screen import InstructionsScreen
from ui.screens.leaderboard_screen import LeaderboardScreen
from ui.screens.countdown_screen import CountdownScreen
from ui.screens.rehearsal_screen import RehearsalScreen
from ui.screens.cta_screen import CTAScreen
from ui.screens.performance_screen import PerformanceScreen
from ui.screens.score_entry_screen import ScoreEntryScreen
from ui.screens.congratulations_screen import (
    CongratulationsScreen
)
from ui.app_manager import AppManager
from ui.widgets.emergency_reset_button import EmergencyResetButton


class KaraokeApp(App):
    """Main Kivy application for IBP-KaraokeLive."""
    
    def build(self):
        """Build and return the root widget."""
        # Load the KV file that defines screen layouts
        Builder.load_file('ui/screens/screens.kv')

        # Create the screen manager with smooth transitions
        sm = ScreenManager()
        sm.transition = FadeTransition(duration=0.4)

        # Add screens (Phase 0: only basic screens, no games)
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(InstructionsScreen(name='instructions'))
        sm.add_widget(LeaderboardScreen(name='leaderboard'))

        # Phase 3: Add karaoke screens
        sm.add_widget(CountdownScreen(name='countdown'))
        sm.add_widget(RehearsalScreen(name='rehearsal'))
        sm.add_widget(CTAScreen(name='cta'))
        sm.add_widget(PerformanceScreen(name='performance'))
        sm.add_widget(ScoreEntryScreen(name='score_entry'))
        sm.add_widget(
            CongratulationsScreen(name='congratulations')
        )

        # Bind global keyboard shortcuts
        Window.bind(on_keyboard=self.on_key_press)

        # Create the app manager (replaces GameManager, no GPIO/games)
        self.app_manager = AppManager(sm)

        # Create FloatLayout to hold screen manager and emergency button
        root_layout = FloatLayout()
        root_layout.add_widget(sm)

        # Add invisible emergency reset button to top-right corner
        emergency_button = EmergencyResetButton()
        root_layout.add_widget(emergency_button)

        return root_layout
    
    def on_key_press(self, window, key, scancode, codepoint, modifiers):
        """
        Global keyboard listener for development shortcuts.
        
        Args:
            key: Key code (27 = ESC, etc.)
            codepoint: Character representation
        """
        # ESC key (27) - Exit application
        if key == 27:
            print("ESC pressed - Closing application")
            self.stop()
            return True
        
        # 'R' key - Return to welcome screen (dev shortcut)
        if codepoint == 'r':
            print("R pressed - Returning to welcome")
            self.app_manager.return_to_welcome()
            return True
        
        return False
    
    def on_stop(self):
        """Called when the application is closing."""
        print("Application closing. Cleaning up resources...")
        self.app_manager.cleanup()


if __name__ == '__main__':
    print("="*60)
    print("IBP-KaraokeLive - Phase 0: Base Application")
    print(f"Resolution: {WINDOW_WIDTH}x{WINDOW_HEIGHT} (Horizontal)")
    print("Platform: Windows 11 Mini-PC")
    print("="*60)
    KaraokeApp().run()