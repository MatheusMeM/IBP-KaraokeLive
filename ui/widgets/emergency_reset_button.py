"""
Emergency Reset Button Widget
Invisible button in top-right corner that triggers emergency reset.
"""

from kivy.uix.button import Button
from kivy.app import App


class EmergencyResetButton(Button):
    """
    Invisible button positioned in top-right corner.
    On press, triggers emergency reset via app_manager.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Make it invisible
        self.opacity = 0
        self.background_color = (0, 0, 0, 0)
        
        # Position in top-right corner
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'right': 1, 'top': 1}
        
    def on_press(self):
        """Trigger emergency reset when button is pressed."""
        print("🚨 Emergency Reset Button pressed - returning to welcome")
        app = App.get_running_app()
        if hasattr(app, 'app_manager'):
            app.app_manager.return_to_welcome()