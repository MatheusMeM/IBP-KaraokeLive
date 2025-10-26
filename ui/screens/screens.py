"""
IBP-KaraokeLive Screen Classes
Phase 0: Simplified screens (Welcome, Instructions, Leaderboard only)
Adapted from Interactive Stand Game
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label


class WelcomeScreen(Screen):
    """Initial welcome/idle screen."""
    pass


class InstructionsScreen(Screen):
    """Instructions screen with dynamic content."""
    
    def update_content(self, title: str, body: str, button_text: str) -> None:
        """
        Updates the text of the labels and button on the screen.
        
        Args:
            title: Title text
            body: Body/instructions text
            button_text: Button label
        """
        self.ids.title_label.text = title
        self.ids.body_label.text = body
        self.ids.action_button.text = button_text


class LeaderboardScreen(Screen):
    """Leaderboard display screen."""
    
    def update_leaderboard(self, scores, player_name=None):
        """Clears and rebuilds the leaderboard display with improved visual design."""
        grid = self.ids.leaderboard_grid
        grid.clear_widgets()

        # Sort scores descending
        sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        
        # Add header with professional styling - ALL IN PORTUGUESE
        header_color = (0/255, 64/255, 119/255, 1)  # color_primary_blue
        grid.add_widget(Label(
            text='POSIÇÃO',
            bold=True,
            font_size='32sp',
            color=header_color,
            font_name='Roboto'
        ))
        grid.add_widget(Label(
            text='NOME',
            bold=True,
            font_size='32sp',
            color=header_color,
            font_name='Roboto'
        ))
        grid.add_widget(Label(
            text='PONTUAÇÃO',
            bold=True,
            font_size='32sp',
            color=header_color,
            font_name='Roboto'
        ))

        # Add top scores with alternating colors for better readability
        for i, entry in enumerate(sorted_scores[:15]):
            is_player = player_name and entry.get('name') == player_name
            
            # Color scheme: player highlighted in green, others in blue tones
            if is_player:
                text_color = (134/255, 188/255, 37/255, 1)  # color_primary_green
                font_weight = True
                font_size = '28sp'
            else:
                text_color = (0/255, 64/255, 119/255, 1)  # color_primary_blue
                font_weight = False
                font_size = '24sp'
            
            # Rank label
            rank_text = f"#{i + 1}" if i < 3 else str(i + 1)
            rank_label = Label(
                text=rank_text,
                color=text_color,
                bold=font_weight,
                font_size=font_size,
                font_name='Roboto'
            )
            
            # Name label
            name_label = Label(
                text=entry.get('name', 'N/A'),
                color=text_color,
                bold=font_weight,
                font_size=font_size,
                font_name='Roboto'
            )
            
            # Score label
            score_label = Label(
                text=str(entry.get('score', 0)),
                color=text_color,
                bold=font_weight,
                font_size=font_size,
                font_name='Roboto'
            )

            grid.add_widget(rank_label)
            grid.add_widget(name_label)
            grid.add_widget(score_label)
