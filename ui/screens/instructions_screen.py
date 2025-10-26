"""
Instructions Screen for IBP-KaraokeLive
Phase 0: Basic instructions screen adapted from Interactive Stand Game
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class InstructionsScreen(Screen):
    """Instructions screen showing karaoke rules and controls."""

    title_text = StringProperty("IBP KaraokeLive")
    body_text = StringProperty("")
    button_text = StringProperty("VOLTAR")

    def __init__(self, **kwargs):
        """Initialize the instructions screen."""
        super().__init__(**kwargs)

    def on_enter(self):
        """Called when entering the screen."""
        print("Entered Instructions Screen")

    def update_content(self, title: str = "", body: str = "", button_text: str = "VOLTAR"):
        """
        Update the instruction screen content.
        
        Args:
            title: Screen title text
            body: Main body text
            button_text: Text for the back button
        """
        if title:
            self.title_text = title
        if body:
            self.body_text = body
        if button_text:
            self.button_text = button_text

    def go_to_welcome(self):
        """Navigate back to welcome screen."""
        self.manager.current = 'welcome'

    def go_to_leaderboard(self):
        """Navigate to leaderboard screen."""
        self.manager.current = 'leaderboard'