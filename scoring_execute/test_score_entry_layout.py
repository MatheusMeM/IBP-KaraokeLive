"""Test script for redesigned score entry screen.

This demonstrates the fixed keyboard layout where:
- Bottom 30% = Always-visible compact keyboard
- Top 70% = Content (score, stars, input, button)

Run this to see the layout before integrating into your app.
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.config import Config

# Import the redesigned screen
import sys
sys.path.insert(0, '/mnt/user-data/outputs')
from score_entry_screen import ScoreEntryScreen


# Mock RankingManager for testing
class MockRankingManager:
    def add_score(self, name, score):
        print(f"[MOCK] Would save: {name} = {score}")
        return True


class TestApp(App):
    """Test application for score entry screen."""
    
    def build(self):
        # Set window size (1920x1080 for kiosk)
        Window.size = (1920, 1080)
        
        # Create screen manager
        sm = ScreenManager()
        
        # Create score entry screen
        score_screen = ScoreEntryScreen(name='score_entry')
        
        # Mock the ranking manager
        score_screen.ranking = MockRankingManager()
        
        # Set a test score
        score_screen.set_score(71)
        
        sm.add_widget(score_screen)
        sm.current = 'score_entry'
        
        return sm


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎹 TESTING REDESIGNED SCORE ENTRY SCREEN")
    print("="*60)
    print("\nLayout Structure:")
    print("  ┌─────────────────────────────────────┐")
    print("  │ TOP 70% - CONTENT AREA              │")
    print("  │                                     │")
    print("  │  • Score Display (large gold text)  │")
    print("  │  • Star Rating (5 stars)            │")
    print("  │  • Label: 'Enter Your Name'         │")
    print("  │  • Text Display (white box)         │")
    print("  │  • Submit Button (green)            │")
    print("  │                                     │")
    print("  ├─────────────────────────────────────┤ 30% mark")
    print("  │ BOTTOM 30% - KEYBOARD (fixed)       │")
    print("  │                                     │")
    print("  │  [1][2][3][4][5][6][7][8][9][0][⌫] │")
    print("  │  [Q][W][E][R][T][Y][U][I][O][P]    │")
    print("  │  [A][S][D][F][G][H][J][K][L]       │")
    print("  │  [Z][X][C][V][B][N][M][SPACE][✓]   │")
    print("  │                                     │")
    print("  └─────────────────────────────────────┘")
    print("\nFeatures:")
    print("  ✓ No OS keyboard popup")
    print("  ✓ No widget overlap")
    print("  ✓ Compact keyboard (30% height)")
    print("  ✓ All content visible in top 70%")
    print("  ✓ Touch-optimized button sizes")
    print("  ✓ Professional spacing and layout")
    print("\nControls:")
    print("  • Type using on-screen keyboard")
    print("  • ⌫ = Backspace")
    print("  • ✓ = Submit score")
    print("  • Max 20 characters")
    print("\n" + "="*60 + "\n")
    
    TestApp().run()
