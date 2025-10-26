"""
Tela de performance - música com letras (fone + caixa).
Versão melhorada com animações de karaoke profissionais.
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
    """Tela de performance do karaoke com animações suaves."""
    
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
            keep_ratio=False,
            opacity=1,
            volume=0,
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
        
        # Lyrics container - centered on screen
        lyrics_container = FloatLayout(
            size_hint=(1, 1)
        )
        
        # Vertical layout for 3-line karaoke display
        lyrics_box = BoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint=(0.95, None),
            height=300,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Previous line (TOP) - cinza, menor, desbotada
        self.prev_label = Label(
            text='',
            font_size='35sp',
            color=(0.5, 0.5, 0.5, 0.7),
            size_hint_y=None,
            height=50,
            outline_width=1,
            outline_color=(0, 0, 0, 0.8),
            halign='center',
            valign='bottom'
        )
        self.prev_label.bind(size=self.prev_label.setter('text_size'))
        lyrics_box.add_widget(self.prev_label)
        
        # Current line (MEIO) - AMARELO, grande, negrito - DESTAQUE MÁXIMO!
        self.current_label = Label(
            text='',
            font_size='70sp',
            bold=True,
            color=(1, 1, 0, 1),  # Amarelo vibrante
            size_hint_y=None,
            height=120,
            outline_width=3,
            outline_color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        self.current_label.bind(size=self.current_label.setter('text_size'))
        lyrics_box.add_widget(self.current_label)
        
        # Next line (EMBAIXO) - branca, tamanho médio
        self.next_label = Label(
            text='',
            font_size='40sp',
            color=(0.95, 0.95, 0.95, 0.85),
            size_hint_y=None,
            height=60,
            outline_width=2,
            outline_color=(0, 0, 0, 0.9),
            halign='center',
            valign='top'
        )
        self.next_label.bind(size=self.next_label.setter('text_size'))
        lyrics_box.add_widget(self.next_label)
        
        lyrics_container.add_widget(lyrics_box)
        self.add_widget(lyrics_container)
        
        # Track last displayed line for smooth transitions
        self.last_current_text = ''
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
        
        # Reset lyrics
        self.last_current_text = ''
        
        # Tocar música via AudioRouter (dual playback)
        self.audio_router.play()
        
        # Agendar atualização (60 FPS para animações suaves)
        self.update_event = Clock.schedule_interval(self.update, 1/60)
    
    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard shortcuts for development."""
        # 'S' key = skip
        if codepoint == 's' or codepoint == 'S':
            print("🔧 DEV: Skip shortcut pressed - performance")
            self.finish_performance()
            return True
        return False
    
    def _animate_line_change(self):
        """Animar transição suave quando a linha muda."""
        # Fade in + scale up da linha atual
        self.current_label.opacity = 0
        self.current_label.font_size = 60  # Número, não string
        
        anim = Animation(
            opacity=1,
            font_size=70,  # Número, não string
            duration=0.3,
            transition='out_cubic'
        )
        anim.start(self.current_label)
        
        # Fade in das outras linhas
        self.prev_label.opacity = 0
        self.next_label.opacity = 0
        
        Animation(opacity=0.7, duration=0.3).start(self.prev_label)
        Animation(opacity=0.85, duration=0.3).start(self.next_label)
    
    def update(self, dt):
        """Atualizar letras com animações suaves."""
        # Tempo atual via AudioRouter
        current_time = self.audio_router.get_position()
        
        # Atualizar letras via sliding window
        lines = self.lyric_display.get_context_lines(current_time)
        
        # Detectar mudança de linha para animar
        new_current = lines['current'] or ''
        line_changed = new_current != self.last_current_text and new_current != ''
        
        # Atualizar textos (vazio se None - SEM "Aguarde...")
        self.prev_label.text = lines['prev'] if lines['prev'] else ''
        self.current_label.text = lines['current'] if lines['current'] else ''
        self.next_label.text = lines['next'] if lines['next'] else ''
        
        # Animar apenas se mudou para uma linha válida
        if line_changed:
            self._animate_line_change()
            self.last_current_text = new_current
        
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
            self.update_event = None
        
        self.audio_router.stop()
        self.video.state = 'stop'