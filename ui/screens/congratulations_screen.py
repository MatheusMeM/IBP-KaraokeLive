"""
Tela de parabéns - fim do karaoke.
"""
from kivy.uix.screenmanager import Screen


class CongratulationsScreen(Screen):
    """Tela de parabéns."""
    
    def restart(self, instance):
        """Reiniciar jogo (volta para welcome)."""
        self.manager.current = 'welcome'