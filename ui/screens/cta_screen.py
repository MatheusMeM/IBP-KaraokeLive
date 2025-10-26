"""
Tela de CTA - transição entre ensaio e performance.
"""
from kivy.uix.screenmanager import Screen


class CTAScreen(Screen):
    """Tela de CTA (Call to Action)."""
    
    def start_performance(self, instance):
        """Ir para countdown antes da performance."""
        # Configurar próximo destino do countdown
        countdown = self.manager.get_screen('countdown')
        countdown.next_screen = 'performance'
        
        self.manager.current = 'countdown'