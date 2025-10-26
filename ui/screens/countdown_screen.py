"""
Tela de countdown (3, 2, 1...).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from config.app_config import COUNTDOWN_SECONDS


class CountdownScreen(Screen):
    """
    Tela de countdown antes do karaoke.
    Pode ser reutilizada para ensaio e performance.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.label = Label(
            text='3',
            font_size='200sp',
            bold=True
        )
        self.add_widget(self.label)
        
        self.counter = COUNTDOWN_SECONDS
        self.next_screen = 'rehearsal'  # Default, pode ser mudado
    
    def on_enter(self):
        """Iniciar countdown ao entrar na tela."""
        self.counter = COUNTDOWN_SECONDS
        self.label.text = str(self.counter)
        Clock.schedule_interval(self.update_countdown, 1.0)
    
    def update_countdown(self, dt):
        """Atualizar número do countdown."""
        self.counter -= 1
        
        if self.counter > 0:
            self.label.text = str(self.counter)
        else:
            # Ir para próxima tela
            self.manager.current = self.next_screen
            return False  # Parar clock