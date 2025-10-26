"""
Tela de performance - música com letras (fone + caixa).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from modules.audio_player import SimpleAudioPlayer
from modules.audio_router import AudioRouter
from modules.lyric_display import LyricDisplay
from config.app_config import AUDIO_FILE, LYRICS_FILE


class PerformanceScreen(Screen):
    """Tela de performance do karaoke."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Componentes
        self.audio_player = SimpleAudioPlayer(AUDIO_FILE)
        self.lyric_display = LyricDisplay(LYRICS_FILE)
        self.audio_router = AudioRouter()
        
        # UI (similar ao RehearsalScreen, mas com visual diferente)
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10
        )
        
        # Título com indicador "AO VIVO"
        title = Label(
            text='🔴 PERFORMANCE AO VIVO',
            font_size='40sp',
            color=(1, 0, 0, 1),  # Vermelho
            size_hint_y=0.1
        )
        layout.add_widget(title)
        
        # Linha anterior
        self.prev_label = Label(
            text='',
            font_size='25sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.2
        )
        layout.add_widget(self.prev_label)
        
        # Linha atual (amarelo brilhante)
        self.current_label = Label(
            text='Aguarde...',
            font_size='55sp',
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=0.4
        )
        layout.add_widget(self.current_label)
        
        # Próxima linha
        self.next_label = Label(
            text='',
            font_size='30sp',
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=0.2
        )
        layout.add_widget(self.next_label)
        
        # Timer
        self.timer_label = Label(
            text='0:00 / 0:30',
            font_size='20sp',
            size_hint_y=0.1
        )
        layout.add_widget(self.timer_label)
        
        self.add_widget(layout)
        
        self.update_event = None
    
    def on_enter(self):
        """Iniciar performance."""
        # Configurar roteamento (fone + caixa)
        self.audio_router.set_performance_mode()
        
        # Tocar música
        self.audio_player.play()
        
        # Agendar atualização
        self.update_event = Clock.schedule_interval(self.update, 1/30)
    
    def update(self, dt):
        """Atualizar letras e timer."""
        current_time = self.audio_player.get_position()
        duration = self.audio_player.get_duration()
        
        # Timer
        self.timer_label.text = (
            f"{int(current_time // 60)}:{int(current_time % 60):02d} / "
            f"{int(duration // 60)}:{int(duration % 60):02d}"
        )
        
        # Letras
        lines = self.lyric_display.get_context_lines(current_time)
        
        self.prev_label.text = lines['prev'] or ''
        self.current_label.text = lines['current'] or 'Aguarde...'
        self.next_label.text = lines['next'] or ''
        
        # Verificar fim
        if not self.audio_player.is_playing():
            self.finish_performance()
    
    def finish_performance(self):
        """Finalizar e ir para congratulations."""
        if self.update_event:
            self.update_event.cancel()
        
        self.audio_player.stop()
        
        # Ir para tela de parabéns
        self.manager.current = 'congratulations'
    
    def on_leave(self):
        """Cleanup."""
        if self.update_event:
            self.update_event.cancel()
        self.audio_player.stop()