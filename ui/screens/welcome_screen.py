"""
Welcome Screen - Entry point for IBP-KaraokeLive
Phase 0: Simple welcome screen
"""

from kivy.uix.screenmanager import Screen


class WelcomeScreen(Screen):
    """Welcome/idle screen shown at application start."""
    
    def on_start_button(self):
        """Called when user presses the start button."""
        # Get app manager from app instance
        from kivy.app import App
        app = App.get_running_app()
        app.app_manager.show_instructions()