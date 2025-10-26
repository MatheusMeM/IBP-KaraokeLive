"""
AppManager - Application flow orchestrator
Phase 0: Simple screen navigation and ranking display
"""

import datetime
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

from data.ranking_manager import RankingManager
from config.app_config import IDLE_TIMEOUT


class AppManager:
    """Orchestrates application flow between screens."""
    
    def __init__(self, screen_manager: ScreenManager):
        """
        Initialize the app manager.
        
        Args:
            screen_manager: Kivy ScreenManager instance
        """
        self.sm = screen_manager
        self.ranking = RankingManager()
        self.idle_timeout_event = None
        
        print("AppManager initialized for IBP-KaraokeLive Phase 0")
    
    def show_instructions(self):
        """Show instructions screen before rehearsal."""
        screen = self.sm.get_screen('instructions')
        screen.update_content(
            title='Como Funciona',
            body=('Você terá dois momentos:\n\n'
                  '1️⃣ ENSAIO: Pratique com fones de ouvido\n'
                  '   (só você escuta)\n\n'
                  '2️⃣ PERFORMANCE: Mostre seu talento!\n'
                  '   (todos escutam no som ambiente)\n\n'
                  'Prepare-se para cantar!'),
            button_text='▶ ENSAIO'
        )
        self.go_to_screen('instructions')
    
    def proceed_from_instructions(self):
        """Navigate from instructions to countdown before rehearsal."""
        print("Proceeding from instructions → countdown → rehearsal")
        
        # Configure countdown to transition to rehearsal
        countdown = self.sm.get_screen('countdown')
        countdown.next_screen = 'rehearsal'
        
        # Navigate to countdown screen
        self.go_to_screen('countdown')
    
    def show_leaderboard(self, player_name=None):
        """
        Display today's leaderboard.
        
        Args:
            player_name: Optional player name to highlight
        """
        today_scores = self.ranking.get_today_scores()
        
        self.go_to_screen('leaderboard')
        screen = self.sm.get_screen('leaderboard')
        screen.update_leaderboard(today_scores, player_name)
        
        self.start_idle_timeout()
    
    def go_to_screen(self, screen_name: str):
        """Navigate to specified screen."""
        print(f"→ {screen_name}")
        self.sm.current = screen_name
    
    def return_to_welcome(self):
        """Return to welcome screen."""
        print("Returning to welcome")
        self.cancel_idle_timeout()
        self.go_to_screen('welcome')
    
    def start_idle_timeout(self):
        """Start idle timeout for auto-return to welcome."""
        self.cancel_idle_timeout()
        print(f"Idle timeout: {IDLE_TIMEOUT}s")
        self.idle_timeout_event = Clock.schedule_once(
            lambda dt: self.return_to_welcome(), 
            IDLE_TIMEOUT
        )
    
    def cancel_idle_timeout(self):
        """Cancel active idle timeout."""
        if self.idle_timeout_event:
            self.idle_timeout_event.cancel()
            self.idle_timeout_event = None
    
    def cleanup(self):
        """Cleanup on app close."""
        print("Cleaning up AppManager")
        self.cancel_idle_timeout()