"""
Tela de performance - música com letras (fone + caixa).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

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
        
        # Video background - add first so it's behind everything
        self.video = Video(
            source='assets/video/Ibp - Energia da Revolucao.mp4',
            state='stop',
            allow_stretch=True,
            keep_ratio=False,  # Fill entire screen
            opacity=1,
            volume=0,  # Mute video audio to avoid interference
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.video)
        
        # BLACK STRIP - BOTTOM 8.5%
        subtitle_blocker_lower = BoxLayout(
            size_hint=(1, 0.085),
            pos_hint={'x': 0, 'y': 0}
        )
        with subtitle_blocker_lower.canvas.before:
            Color(0, 0, 0, 1) 
            self.blocker_bg_lower = Rectangle(
                pos=subtitle_blocker_lower.pos,
                size=subtitle_blocker_lower.size
            )
        subtitle_blocker_lower.bind(
            pos=lambda instance, value: setattr(self.blocker_bg_lower, 'pos', value),
            size=lambda instance, value: setattr(self.blocker_bg_lower, 'size', value)
        )
        self.add_widget(subtitle_blocker_lower)
        
        # BLACK STRIP - TOP 8%
        subtitle_blocker_upper = BoxLayout(
            size_hint=(1, 0.08),
            pos_hint={'x': 0, 'y': 0.92}
        )
        with subtitle_blocker_upper.canvas.before:
            Color(0, 0, 0, 1) 
            self.blocker_bg_upper = Rectangle(
                pos=subtitle_blocker_upper.pos,
                size=subtitle_blocker_upper.size
            )
        subtitle_blocker_upper.bind(
            pos=lambda instance, value: setattr(self.blocker_bg_upper, 'pos', value),
            size=lambda instance, value: setattr(self.blocker_bg_upper, 'size', value)
        )
        self.add_widget(subtitle_blocker_upper)
        
        # Lyrics - Large, prominent, centered on screen
        lyrics_container = FloatLayout(
            size_hint=(1, 1)
        )
        
        lyrics_box = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(0.9, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Previous line (gray, smaller)
        self.prev_label = Label(
            text='',
            font_size='40sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.2,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        self.prev_label.bind(size=self.prev_label.setter('text_size'))
        lyrics_box.add_widget(self.prev_label)
        
        # Current line (yellow, large, prominent)
        self.current_label = Label(
            text='Aguarde...',
            font_size='80sp',
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=0.6,
            outline_width=4,
            outline_color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        self.current_label.bind(size=self.current_label.setter('text_size'))
        lyrics_box.add_widget(self.current_label)
        
        # Next line (white, medium)
        self.next_label = Label(
            text='',
            font_size='45sp',
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.2,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        self.next_label.bind(size=self.next_label.setter('text_size'))
        lyrics_box.add_widget(self.next_label)
        
        lyrics_container.add_widget(lyrics_box)
        self.add_widget(lyrics_container)
        
        self.update_event = None
    
    def on_enter(self):
        """Iniciar performance."""
        print("=" * 50)
        print("🎬 Entering PerformanceScreen")
        print(f"Video source: {self.video.source}")
        print("=" * 50)
        
        # Bind keyboard for skip shortcut (development)
        Window.bind(on_keyboard=self._on_keyboard)
        
        # Configurar roteamento e carregar áudios (vocal + instrumental)
        self.audio_router.set_performance_mode()
        vocal_file = 'assets/audio/Ibp - Energia da Revolucao.wav'
        instrumental_file = 'assets/audio/Ibp - Energia da Revolucao_Voiceless.wav'
        self.audio_router.load_audio(vocal_file, instrumental_file)
        
        # Iniciar video with fade-in
        print(f"🎥 Starting video playback")
        self.video.state = 'play'
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.video)
        
        # Tocar música via AudioRouter (dual playback)
        self.audio_router.play()
        
        # Agendar atualização
        self.update_event = Clock.schedule_interval(self.update, 1/30)
    
    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard shortcuts for development."""
        # 'S' key = skip
        if codepoint == 's' or codepoint == 'S':
            print("🔧 DEV: Skip shortcut pressed - performance")
            self.finish_performance()
            return True
        return False
    
    def update(self, dt):
        """Atualizar letras."""
        # Tempo atual via AudioRouter
        current_time = self.audio_router.get_position()
        
        # Atualizar letras
        lines = self.lyric_display.get_context_lines(current_time)
        
        self.prev_label.text = lines['prev'] or ''
        self.current_label.text = lines['current'] or 'Aguarde...'
        self.next_label.text = lines['next'] or ''
        
        # Verificar fim usando is_playing()
        if not self.audio_router.is_playing():
            self.finish_performance()
    
    def finish_performance(self):
        """Finalizar e ir para congratulations."""
        print("🎬 Finishing performance...")
        
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None
        
        # Stop audio completely
        self.audio_router.stop()
        
        # Stop and reset video
        self.video.state = 'stop'
        self.video.opacity = 0
        
        # Ir para tela de parabéns
        self.manager.current = 'congratulations'
    
    def on_leave(self):
        """Cleanup."""
        Window.unbind(on_keyboard=self._on_keyboard)
        
        if self.update_event:
            self.update_event.cancel()
        self.audio_router.stop()
        self.video.state = 'stop'
