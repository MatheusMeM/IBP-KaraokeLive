"""Score entry screen with fixed virtual keyboard layout.

Layout design:
- Bottom 30% of screen: Always-visible compact virtual keyboard
- Top 70% of screen: Score display, input field, submit button
- No overlap, optimized for 1920x1080 kiosk display
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window

from data.ranking_manager import RankingManager


class CompactVirtualKeyboard(BoxLayout):
    """Compact virtual keyboard optimized for 30% screen height."""
    
    def __init__(self, on_key_press, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(3)
        self.padding = [dp(10), dp(8), dp(10), dp(8)]
        self.on_key_press = on_key_press
        
        # Keyboard background
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)  # Dark gray
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Define keyboard layout (compact 4 rows)
        keyboard_layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '⌫'],  # Numbers + backspace
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],        # Top row
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],            # Middle row
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'SPACE', '✓']         # Bottom row + submit
        ]
        
        for row_keys in keyboard_layout:
            row = BoxLayout(spacing=dp(3), size_hint_y=0.25)
            
            for key in row_keys:
                btn = Button(
                    text=key,
                    font_size=dp(24) if key != 'SPACE' else dp(16),
                    bold=True,
                    background_normal='',
                    background_color=(0.3, 0.3, 0.3, 1) if key not in ['⌫', '✓', 'SPACE'] else (0.2, 0.5, 0.3, 1)
                )
                
                # Spacebar takes 2x width
                if key == 'SPACE':
                    btn.size_hint_x = 2.0
                    btn.text = 'SPACE'
                    btn.font_size = dp(20)
                # Submit button gets green color
                elif key == '✓':
                    btn.background_color = (0.2, 0.7, 0.3, 1)
                # Backspace gets red accent
                elif key == '⌫':
                    btn.background_color = (0.6, 0.2, 0.2, 1)
                
                btn.bind(on_press=lambda instance, k=key: self.on_key_press(k))
                row.add_widget(btn)
            
            self.add_widget(row)
    
    def _update_bg(self, *args):
        """Update background rectangle."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class ScoreEntryScreen(Screen):
    """Score entry screen with fixed keyboard layout."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.ranking = RankingManager()
        
        # Root layout using FloatLayout for precise positioning
        root = FloatLayout()
        
        # Background
        with root.canvas.before:
            Color(0.05, 0.05, 0.1, 1)  # Dark blue background
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *args: setattr(self.bg_rect, 'pos', root.pos))
        root.bind(size=lambda *args: setattr(self.bg_rect, 'size', root.size))
        
        # ===== BOTTOM 30%: FIXED KEYBOARD =====
        self.keyboard = CompactVirtualKeyboard(
            on_key_press=self.handle_key_press,
            size_hint=(1, 0.30),
            pos_hint={'x': 0, 'y': 0}  # Anchored at bottom
        )
        root.add_widget(self.keyboard)
        
        # ===== TOP 70%: CONTENT AREA =====
        content_area = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(40), dp(20), dp(40), dp(20)],
            size_hint=(1, 0.70),
            pos_hint={'x': 0, 'y': 0.30}  # Starts at 30% from bottom
        )
        
        # 1. Score display (20% of content area)
        self.score_label = Label(
            text='YOUR SCORE: 0',
            font_size=dp(72),
            bold=True,
            color=(1, 0.84, 0, 1),  # Gold
            size_hint_y=0.20,
            halign='center',
            valign='middle'
        )
        self.score_label.bind(size=self.score_label.setter('text_size'))
        content_area.add_widget(self.score_label)
        
        # 2. Stars display (15% of content area)
        self.stars_label = Label(
            text='★ ★ ★ ★ ★',
            font_size=dp(50),
            color=(1, 0.84, 0, 1),
            size_hint_y=0.15,
            halign='center',
            valign='middle'
        )
        self.stars_label.bind(size=self.stars_label.setter('text_size'))
        content_area.add_widget(self.stars_label)
        
        # 3. Spacer (10% of content area)
        content_area.add_widget(BoxLayout(size_hint_y=0.10))
        
        # 4. Name label (10% of content area)
        name_label = Label(
            text='Enter Your Name:',
            font_size=dp(32),
            color=(1, 1, 1, 1),
            size_hint_y=0.10,
            halign='center',
            valign='middle'
        )
        name_label.bind(size=name_label.setter('text_size'))
        content_area.add_widget(name_label)
        
        # 5. Text input (20% of content area)
        # Using Label instead of TextInput to avoid OS keyboard
        input_container = BoxLayout(
            size_hint=(0.8, 0.20),
            pos_hint={'center_x': 0.5}
        )
        
        self.name_display = Label(
            text='',
            font_size=dp(40),
            bold=True,
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        self.name_display.bind(size=self.name_display.setter('text_size'))
        
        # Input background
        with input_container.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.input_bg = RoundedRectangle(
                pos=input_container.pos,
                size=input_container.size,
                radius=[dp(10)]
            )
        input_container.bind(
            pos=lambda *args: setattr(self.input_bg, 'pos', input_container.pos),
            size=lambda *args: setattr(self.input_bg, 'size', input_container.size)
        )
        
        input_container.add_widget(self.name_display)
        content_area.add_widget(input_container)
        
        # 6. Spacer (5% of content area)
        content_area.add_widget(BoxLayout(size_hint_y=0.05))
        
        # 7. Submit button (20% of content area)
        self.submit_btn = Button(
            text='SUBMIT SCORE',
            font_size=dp(36),
            bold=True,
            size_hint=(0.6, 0.20),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0.2, 0.7, 0.3, 1)  # Green
        )
        self.submit_btn.bind(on_press=self.submit_score)
        content_area.add_widget(self.submit_btn)
        
        root.add_widget(content_area)
        self.add_widget(root)
    
    def handle_key_press(self, key):
        """Handle virtual keyboard input."""
        current_text = self.name_display.text
        
        if key == '⌫':  # Backspace
            self.name_display.text = current_text[:-1]
        
        elif key == 'SPACE':
            if len(current_text) < 20:  # Max 20 chars
                self.name_display.text = current_text + ' '
        
        elif key == '✓':  # Submit
            self.submit_score(None)
        
        else:  # Regular character
            if len(current_text) < 20:  # Max 20 chars
                self.name_display.text = current_text + key
    
    def set_score(self, score: int):
        """Set score to display."""
        self.score = score
        self.score_label.text = f'YOUR SCORE: {score}'
        
        # Star rating (0-5 stars based on score 0-100)
        stars = min(5, max(0, int(score / 20)))
        filled = '★ ' * stars
        empty = '☆ ' * (5 - stars)
        self.stars_label.text = filled + empty
    
    def on_enter(self):
        """Clear input when entering screen."""
        self.name_display.text = ''
        print(f"\n{'='*50}")
        print(f"🎯 Score Entry Screen - Score: {self.score}")
        print(f"{'='*50}")
    
    def submit_score(self, instance):
        """Submit score to leaderboard."""
        name = self.name_display.text.strip()
        
        # Validation
        if not name:
            print("❌ Name required")
            self.name_display.color = (1, 0, 0, 1)  # Red text
            return
        
        if len(name) < 3:
            print("❌ Name too short (min 3 chars)")
            self.name_display.color = (1, 0, 0, 1)  # Red text
            return
        
        # Reset color
        self.name_display.color = (0, 0, 0, 1)
        
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
