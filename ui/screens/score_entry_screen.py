"""Simple score entry screen - text input only (no fancy keyboard)."""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

from data.ranking_manager import RankingManager


class ScoreEntryScreen(Screen):
    """Display score and collect player name."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.ranking = RankingManager()
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # Background
        with main_layout.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=lambda *args: setattr(self.bg_rect, 'pos', main_layout.pos))
        main_layout.bind(size=lambda *args: setattr(self.bg_rect, 'size', main_layout.size))
        
        # Score display
        self.score_label = Label(
            text='YOUR SCORE: 0',
            font_size='80sp',
            bold=True,
            color=(1, 0.84, 0, 1),  # Gold
            size_hint_y=0.3
        )
        main_layout.add_widget(self.score_label)
        
        # Stars display
        self.stars_label = Label(
            text='★ ★ ★ ★ ★',
            font_size='60sp',
            color=(1, 0.84, 0, 1),
            size_hint_y=0.2
        )
        main_layout.add_widget(self.stars_label)
        
        # Name input
        name_label = Label(
            text='Enter Your Name:',
            font_size='40sp',
            size_hint_y=0.1
        )
        main_layout.add_widget(name_label)
        
        self.name_input = TextInput(
            text='',
            multiline=False,
            font_size='50sp',
            size_hint=(0.8, 0.15),
            pos_hint={'center_x': 0.5},
            # Touchscreen keyboard optimization
            write_tab=False,  # Prevent tab input
            on_text_validate=self.submit_score  # Submit on Enter key
        )
        # Apply ASCII-only filter as a function (prevents emojis)
        self.name_input.input_filter = lambda text, from_undo: ''.join(
            c for c in text if ord(c) < 128
        )
        main_layout.add_widget(self.name_input)
        
        # Submit button
        submit_btn = Button(
            text='SUBMIT SCORE',
            font_size='40sp',
            size_hint=(0.6, 0.15),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0.5, 0, 1)
        )
        submit_btn.bind(on_press=self.submit_score)
        main_layout.add_widget(submit_btn)
        
        self.add_widget(main_layout)
        
    def set_score(self, score: int):
        """Set score to display."""
        self.score = score
        self.score_label.text = f'YOUR SCORE: {score}'
        
        # Star rating (0-5 stars)
        stars = min(5, max(0, int(score / 20)))
        self.stars_label.text = '★ ' * stars + '☆ ' * (5 - stars)
        
    def on_enter(self):
        """Clear input when entering."""
        self.name_input.text = ''
        self.name_input.focus = True
        
    def submit_score(self, instance):
        """Submit score to leaderboard."""
        name = self.name_input.text.strip()
        
        if not name:
            print("❌ Name required")
            return
            
        if len(name) < 3:
            print("❌ Name too short (min 3 chars)")
            return
            
        # Save to leaderboard
        success = self.ranking.add_score(name, self.score)
        
        if success:
            print(f"✅ Score saved: {name} = {self.score}")
            
            # Navigate to leaderboard
            leaderboard = self.manager.get_screen('leaderboard')
            leaderboard.refresh_leaderboard()
            self.manager.current = 'leaderboard'
        else:
            print("❌ Failed to save score")