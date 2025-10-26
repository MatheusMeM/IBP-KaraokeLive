"""
Leaderboard Screen for IBP-KaraokeLive
Phase 0: Basic leaderboard screen adapted from Interactive Stand Game
"""

import json
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty


class LeaderboardScreen(Screen):
    """Leaderboard screen displaying top scores."""

    leaderboard_data = ListProperty([])
    status_text = StringProperty("Carregando ranking...")

    def __init__(self, **kwargs):
        """Initialize the leaderboard screen."""
        super().__init__(**kwargs)
        self.load_leaderboard()

    def on_enter(self):
        """Called when entering the screen."""
        print("Entered Leaderboard Screen")
        self.load_leaderboard()

    def load_leaderboard(self):
        """Load leaderboard data from JSON file."""
        try:
            with open('data/leaderboard.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not data:
                self.status_text = "Nenhum score registrado ainda.\nSeja o primeiro a jogar!"
                self.leaderboard_data = []
            else:
                # Sort by score descending
                sorted_data = sorted(data, key=lambda x: x.get('score', 0), reverse=True)
                self.leaderboard_data = sorted_data[:10]  # Top 10
                self.status_text = f"Top {len(self.leaderboard_data)} jogadores"

        except FileNotFoundError:
            self.status_text = "Arquivo de ranking não encontrado."
            self.leaderboard_data = []
        except json.JSONDecodeError:
            self.status_text = "Erro ao carregar ranking."
            self.leaderboard_data = []
        except Exception as e:
            self.status_text = f"Erro: {str(e)}"
            self.leaderboard_data = []

    def update_leaderboard(self, scores: list, highlight_player: str = None):
        """
        Update leaderboard with provided scores.
        
        Args:
            scores: List of score dictionaries
            highlight_player: Optional player name to highlight
        """
        if not scores:
            self.status_text = "Nenhum score registrado hoje.\nSeja o primeiro a jogar!"
            self.leaderboard_data = []
        else:
            self.leaderboard_data = scores[:10]  # Top 10
            self.status_text = f"Top {len(self.leaderboard_data)} jogadores de hoje"

    def go_to_welcome(self):
        """Navigate back to welcome screen."""
        self.manager.current = 'welcome'

    def refresh_leaderboard(self):
        """Refresh the leaderboard data."""
        self.load_leaderboard()