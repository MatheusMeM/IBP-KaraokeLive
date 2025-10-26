"""
Tela de performance - música com letras (fone + caixa).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window

from modules.audio_router import AudioRouter
from modules.lyric_display import LyricDisplay
from config.app_config import LYRICS_FILE


class PerformanceScreen(Screen):
    """Tela de performance do karaoke."""
    
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
        
        # Título "AO VIVO" com sombra forte
        title = Label(
            text='🔴 PERFORMANCE AO VIVO',
            font_size='45sp',
            bold=True,
            color=(1, 0.2, 0.2, 1),  # Vermelho brilhante
            size_hint_y=0.1,
            outline_width=3,
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
            font_size='60sp',
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
        """Iniciar performance."""
        # Bind keyboard for skip shortcut (development)
        Window.bind(on_keyboard=self._on_keyboard)
        
        # Configurar roteamento e carregar áudios (vocal + instrumental)
        self.audio_router.set_performance_mode()
        vocal_file = 'assets/audio/Ibp - Energia da Revolucao.wav'
        instrumental_file = (
            'assets/audio/Ibp - Energia da Revolucao_Voiceless.wav'
        )
        self.audio_router.load_audio(vocal_file, instrumental_file)
        
        # Iniciar video com fade-in
        self.video.state = 'play'
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.video)
        
        # Tocar música via AudioRouter (dual playback)
        self.audio_router.play()
        
        # Agendar atualização
        self.update_event = Clock.schedule_interval(self.update, 1/30)
    
    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        """
        Handle keyboard input for development shortcuts.
        
        Args:
            key: Key code
            codepoint: Character code
        
        Returns:
            True if handled, False otherwise
        """
        # 'S' key = skip (development shortcut)
        if codepoint == 's' or codepoint == 'S':
            print("🔧 DEV: Skip shortcut pressed - performance")
            self.finish_performance()
            return True
        return False
    
    def update(self, dt):
        """Atualizar letras e timer."""
        current_time = self.audio_router.get_position()
        duration = self.audio_router.get_duration()
        
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
        
        # Verificar fim usando is_playing()
        if not self.audio_router.is_playing():
            self.finish_performance()
    
    def finish_performance(self):
        """Finalizar e ir para congratulations."""
        if self.update_event:
            self.update_event.cancel()
        
        self.audio_router.stop()
        self.video.state = 'stop'
        
        # Ir para tela de parabéns
        self.manager.current = 'congratulations'
    
    def on_leave(self):
        """Cleanup."""
        # Unbind keyboard
        Window.unbind(on_keyboard=self._on_keyboard)
        
        if self.update_event:
            self.update_event.cancel()
        self.audio_router.stop()
        self.video.state = 'stop'