"""
Tela de ensaio - música com letras (apenas fone).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from modules.audio_player import SimpleAudioPlayer
from modules.audio_router import AudioRouter
from modules.lyric_display import LyricDisplay
from config.app_config import AUDIO_FILE, LYRICS_FILE


class RehearsalScreen(Screen):
    """Tela de ensaio do karaoke."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Componentes
        self.audio_player = SimpleAudioPlayer(AUDIO_FILE)
        self.lyric_display = LyricDisplay(LYRICS_FILE)
        self.audio_router = AudioRouter()
        
        # UI
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10
        )
        
        # Título
        title = Label(
            text='🎤 ENSAIO',
            font_size='40sp',
            size_hint_y=0.1
        )
        layout.add_widget(title)
        
        # Linha anterior (cinza)
        self.prev_label = Label(
            text='',
            font_size='25sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.2
        )
        layout.add_widget(self.prev_label)
        
        # Linha atual (amarelo, grande)
        self.current_label = Label(
            text='Aguarde...',
            font_size='50sp',
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=0.4
        )
        layout.add_widget(self.current_label)
        
        # Próxima linha (branco)
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
        """Iniciar ensaio ao entrar na tela."""
        # Configurar roteamento
        self.audio_router.set_rehearsal_mode()
        
        # Tocar música
        self.audio_player.play()
        
        # Agendar atualização
        self.update_event = Clock.schedule_interval(self.update, 1/30)
    
    def update(self, dt):
        """Atualizar letras e timer."""
        # Tempo atual
        current_time = self.audio_player.get_position()
        duration = self.audio_player.get_duration()
        
        # Atualizar timer
        self.timer_label.text = (
            f"{int(current_time // 60)}:{int(current_time % 60):02d} / "
            f"{int(duration // 60)}:{int(duration % 60):02d}"
        )
        
        # Atualizar letras
        lines = self.lyric_display.get_context_lines(current_time)
        
        self.prev_label.text = lines['prev'] or ''
        self.current_label.text = lines['current'] or 'Aguarde...'
        self.next_label.text = lines['next'] or ''
        
        # Verificar fim
        if not self.audio_player.is_playing():
            self.finish_rehearsal()
    
    def finish_rehearsal(self):
        """Finalizar ensaio e avançar."""
        if self.update_event:
            self.update_event.cancel()
        
        self.audio_player.stop()
        
        # Ir para CTA
        self.manager.current = 'cta'
    
    def on_leave(self):
        """Cleanup ao sair."""
        if self.update_event:
            self.update_event.cancel()
        self.audio_player.stop()