"""
Tela de ensaio - música com letras (apenas fone).
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


class RehearsalScreen(Screen):
    """Tela de ensaio do karaoke."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Componentes de áudio
        self.audio_router = AudioRouter()
        self.lyric_display = LyricDisplay(LYRICS_FILE)
        
        # Video background - add first so it's behind everything
        self.video = Video(
            source='assets/video/Ibp - Energia da Revolução.mp4',
            state='stop',
            allow_stretch=True,
            keep_ratio=False,  # Fill entire screen
            opacity=0.5,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.video)
        
        # UI - Semi-transparent overlay container
        from kivy.uix.floatlayout import FloatLayout
        from kivy.graphics import Color, Rectangle, RoundedRectangle
        
        # Transparent overlay to hold UI elements
        overlay = FloatLayout(size_hint=(1, 1))
        
        # Container with semi-transparent background - smaller, in corner
        container = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(0.35, 0.25),  # Smaller container
            pos_hint={'right': 0.98, 'top': 0.98}  # Top-right corner
        )
        
        # Add semi-transparent black background to container
        with container.canvas.before:
            Color(0, 0, 0, 0.7)  # More opaque for better readability
            self.container_bg = RoundedRectangle(
                pos=container.pos,
                size=container.size,
                radius=[15]
            )
        
        # Bind to update background when container moves/resizes
        container.bind(
            pos=self._update_container_bg,
            size=self._update_container_bg
        )
        
        # Timer (white, small)
        self.timer_label = Label(
            text='0:00 / 0:00',
            font_size='18sp',
            size_hint_y=0.3,
            color=(1, 1, 1, 1),
            halign='center'
        )
        container.add_widget(self.timer_label)
        
        # Mode indicator
        mode_label = Label(
            text='ENSAIO',
            font_size='20sp',
            bold=True,
            size_hint_y=0.4,
            color=(0.5, 0.9, 0.2, 1),  # Green
            halign='center'
        )
        container.add_widget(mode_label)
        
        # Status indicator
        self.status_label = Label(
            text='🎤',
            font_size='30sp',
            size_hint_y=0.3,
            color=(1, 1, 1, 1)
        )
        container.add_widget(self.status_label)
        
        # Lyrics - Large, prominent, centered on screen
        lyrics_container = FloatLayout(
            size_hint=(0.9, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        
        lyrics_box = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, 1)
        )
        
        # Previous line (gray)
        self.prev_label = Label(
            text='',
            font_size='35sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.25,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            halign='center'
        )
        lyrics_box.add_widget(self.prev_label)
        
        # Current line (yellow, large, prominent)
        self.current_label = Label(
            text='Aguarde...',
            font_size='70sp',
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=0.5,
            outline_width=4,
            outline_color=(0, 0, 0, 1),
            halign='center'
        )
        lyrics_box.add_widget(self.current_label)
        
        # Next line (white)
        self.next_label = Label(
            text='',
            font_size='40sp',
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.25,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            halign='center'
        )
        lyrics_box.add_widget(self.next_label)
        
        lyrics_container.add_widget(lyrics_box)
        overlay.add_widget(lyrics_container)
        
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
        # Bind keyboard for skip shortcut (development)
        Window.bind(on_keyboard=self._on_keyboard)
        
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
            print("🔧 DEV: Skip shortcut pressed - rehearsal")
            self.finish_rehearsal()
            return True
        return False
    
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
        print("🎬 Finishing rehearsal...")
        
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None
        
        # Stop audio completely
        self.audio_router.stop()
        self.audio_router.is_playing_flag = False
        
        # Stop and reset video
        self.video.state = 'stop'
        self.video.opacity = 0
        
        # Ir para CTA
        self.manager.current = 'cta'
    
    def on_leave(self):
        """Cleanup ao sair."""
        # Unbind keyboard
        Window.unbind(on_keyboard=self._on_keyboard)
        
        if self.update_event:
            self.update_event.cancel()
        self.audio_router.stop()
        self.video.state = 'stop'