"""
Leaderboard Screen for IBP-KaraokeLive
Phase 0: Basic leaderboard screen adapted from Interactive Stand Game
"""

import json
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
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
        """Load TODAY'S leaderboard using RankingManager."""
        try:
            from data.ranking_manager import RankingManager
            
            ranking = RankingManager()
            today_scores = ranking.get_today_scores()
            
            if not today_scores:
                self.status_text = "Nenhum score hoje.\nSeja o primeiro!"
                self.leaderboard_data = []
            else:
                self.leaderboard_data = today_scores[:10]
                self.status_text = f"Top {len(self.leaderboard_data)} de Hoje"
            
            # Populate the grid with widgets
            self._populate_grid()
                
        except Exception as e:
            self.status_text = f"Erro: {str(e)}"
            self.leaderboard_data = []
            self._populate_grid()

    def _populate_grid(self):
        """Populate the leaderboard grid with score widgets."""
        grid = self.ids.get('leaderboard_grid')
        if not grid:
            return
        
        # Clear existing widgets
        grid.clear_widgets()
        
        if not self.leaderboard_data:
            # Show empty state
            empty_label = Label(
                text=self.status_text,
                font_size='40sp',
                color=(0/255, 64/255, 119/255, 1),
                halign='center',
                valign='middle',
                size_hint_y=None,
                height=100
            )
            grid.add_widget(empty_label)
            return
        
        # Add header row
        for header_text in ['#', 'Nome', 'Pontos']:
            header = Label(
                text=header_text,
                font_size='35sp',
                bold=True,
                color=(0/255, 64/255, 119/255, 1),
                size_hint_y=None,
                height=50
            )
            grid.add_widget(header)
        
        # Add score rows
        for idx, score_entry in enumerate(self.leaderboard_data, 1):
            # Rank
            rank_label = Label(
                text=str(idx),
                font_size='32sp',
                color=(0/255, 64/255, 119/255, 1),
                size_hint_y=None,
                height=45
            )
            grid.add_widget(rank_label)
            
            # Name
            name_label = Label(
                text=score_entry.get('name', 'N/A'),
                font_size='32sp',
                color=(0/255, 64/255, 119/255, 1),
                size_hint_y=None,
                height=45
            )
            grid.add_widget(name_label)
            
            # Score
            score_label = Label(
                text=f"{score_entry.get('score', 0.0):.2f}",
                font_size='32sp',
                bold=True,
                color=(134/255, 188/255, 37/255, 1),
                size_hint_y=None,
                height=45
            )
            grid.add_widget(score_label)

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
            self.leaderboard_data = scores[:10]
            self.status_text = f"Top {len(self.leaderboard_data)} jogadores de hoje"
        
        self._populate_grid()

    def go_to_welcome(self):
        """Navigate back to welcome screen."""
        self.manager.current = 'welcome'

    def refresh_leaderboard(self):
        """Refresh the leaderboard data."""
        self.load_leaderboard()