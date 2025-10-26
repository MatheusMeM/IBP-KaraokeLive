"""
Tela de ensaio - música com letras (apenas fone).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.animation import Animation

from modules.audio_router import AudioRouter
from modules.lyric_display import LyricDisplay
from config.app_config import LYRICS_FILE


class RehearsalScreen(Screen):
    """Tela de ensaio do karaoke."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Componentes de áudio
        self.audio_router = AudioRouter()
        self.lyric_display = LyricDisplay(LYRICS_FILE)
        
        # Video background
        self.video = Video(
            source='assets/video/Ibp - Energia da Revolução.mp4',
            state='stop',
            allow_stretch=True,
            keep_ratio=True,
            opacity=0
        )
        self.add_widget(self.video)
        
        # UI - Semi-transparent overlay container
        from kivy.uix.floatlayout import FloatLayout
        from kivy.graphics import Color, Rectangle, RoundedRectangle
        
        overlay = FloatLayout()
        
        # Container with semi-transparent background
        container = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=15,
            size_hint=(0.9, 0.7),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Add semi-transparent black background to container
        with container.canvas.before:
            Color(0, 0, 0, 0.6)  # Semi-transparent black
            self.container_bg = RoundedRectangle(
                pos=container.pos,
                size=container.size,
                radius=[20]
            )
        
        # Bind to update background when container moves/resizes
        container.bind(
            pos=self._update_container_bg,
            size=self._update_container_bg
        )
        
        # Título com sombra
        title = Label(
            text='🎤 ENSAIO',
            font_size='45sp',
            bold=True,
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            outline_width=2,
            outline_color=(0, 0, 0, 1)
        )
        container.add_widget(title)
        
        # Linha anterior (cinza com sombra)
        self.prev_label = Label(
            text='',
            font_size='28sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=0.2,
            outline_width=1,
            outline_color=(0, 0, 0, 1)
        )
        container.add_widget(self.prev_label)
        
        # Linha atual (amarelo brilhante com sombra forte)
        self.current_label = Label(
            text='Aguarde...',
            font_size='55sp',
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=0.4,
            outline_width=3,
            outline_color=(0, 0, 0, 1)
        )
        container.add_widget(self.current_label)
        
        # Próxima linha (branco com sombra)
        self.next_label = Label(
            text='',
            font_size='32sp',
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.2,
            outline_width=1,
            outline_color=(0, 0, 0, 1)
        )
        container.add_widget(self.next_label)
        
        # Timer (branco com sombra)
        self.timer_label = Label(
            text='0:00 / 0:00',
            font_size='24sp',
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            outline_width=1,
            outline_color=(0, 0, 0, 1)
        )
        container.add_widget(self.timer_label)
        
        overlay.add_widget(container)
        self.add_widget(overlay)
        
        self.container = container
        
        self.update_event = None
    
    def _update_container_bg(self, instance, value):
        """Update container background when position/size changes."""
        self.container_bg.pos = instance.pos
        self.container_bg.size = instance.size
    
    def on_enter(self):
        """Iniciar ensaio ao entrar na tela."""
        # Configurar roteamento e carregar áudio (vocal only)
        self.audio_router.set_rehearsal_mode()
        vocal_file = 'assets/audio/Ibp - Energia da Revolucao.wav'
        self.audio_router.load_audio(vocal_file)
        
        # Iniciar video com fade-in
        self.video.state = 'play'
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.video)
        
        # Tocar música via AudioRouter
        self.audio_router.play()
        
        # Agendar atualização
        self.update_event = Clock.schedule_interval(self.update, 1/30)
    
    def update(self, dt):
        """Atualizar letras e timer."""
        # Tempo atual via AudioRouter
        current_time = self.audio_router.get_position()
        duration = self.audio_router.get_duration()
        
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
        
        # Verificar fim usando is_playing()
        if not self.audio_router.is_playing():
            self.finish_rehearsal()
    
    def finish_rehearsal(self):
        """Finalizar ensaio e avançar."""
        if self.update_event:
            self.update_event.cancel()
        
        self.audio_router.stop()
        self.video.state = 'stop'
        
        # Ir para CTA
        self.manager.current = 'cta'
    
    def on_leave(self):
        """Cleanup ao sair."""
        if self.update_event:
            self.update_event.cancel()
        self.audio_router.stop()
        self.video.state = 'stop'