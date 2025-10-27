"""Tela de entrada de pontuação com teclado virtual fixo.

Design:
- 30% inferior: Teclado virtual sempre visível
- 70% superior: Pontuação, avaliação, entrada de nome e botão
- Identidade visual IBP aplicada
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.app import App

from data.ranking_manager import RankingManager


# Cores da marca IBP
COLOR_PRIMARY_BLUE = (0/255, 64/255, 119/255, 1)      # #004077
COLOR_SECONDARY_BLUE = (0/255, 105/255, 180/255, 1)   # #0069B4
COLOR_PRIMARY_GREEN = (134/255, 188/255, 37/255, 1)   # #86BC25
COLOR_SECONDARY_GREEN = (82/255, 174/255, 50/255, 1)  # #52AE32
COLOR_WHITE = (1, 1, 1, 1)
COLOR_DARK_GRAY = (137/255, 137/255, 137/255, 1)
COLOR_LIGHT_GRAY = (216/255, 206/255, 205/255, 1)


class BrandedButton(Button):
    """Botão estilizado com identidade IBP."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = 'Roboto'
        self.background_color = (0, 0, 0, 0)  # Transparente
        self.background_normal = ''
        self.color = COLOR_PRIMARY_BLUE
        self.bold = True
        
        # Desenhar fundo com bordas arredondadas
        with self.canvas.before:
            self.bg_color = Color(*COLOR_PRIMARY_GREEN)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(30)]
            )
        
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.bind(state=self._on_state)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _on_state(self, instance, value):
        """Muda cor quando pressionado."""
        if value == 'down':
            self.bg_color.rgba = COLOR_SECONDARY_GREEN
        else:
            self.bg_color.rgba = COLOR_PRIMARY_GREEN


class VirtualKeyButton(Button):
    """Botão de teclado virtual."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = 'Roboto'
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.color = COLOR_WHITE
        self.bold = True
        
        with self.canvas.before:
            self.bg_color = Color(0.3, 0.3, 0.3, 1)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(8)]
            )
        
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.bind(state=self._on_state)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _on_state(self, instance, value):
        if value == 'down':
            self.bg_color.rgba = (0.2, 0.2, 0.2, 1)
        else:
            self.bg_color.rgba = (0.3, 0.3, 0.3, 1)


class CompactVirtualKeyboard(BoxLayout):
    """Teclado virtual compacto QWERTY em português."""
    
    def __init__(self, on_key_press, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(4)
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        self.on_key_press = on_key_press
        
        # Fundo do teclado
        with self.canvas.before:
            Color(*COLOR_DARK_GRAY)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Layout QWERTY em português (4 linhas)
        keyboard_layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'APAGAR'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'ESPACO', 'OK']
        ]
        
        for row_keys in keyboard_layout:
            row = BoxLayout(spacing=dp(4), size_hint_y=0.25)
            
            for key in row_keys:
                # Criar botão
                if key == 'APAGAR':
                    btn = VirtualKeyButton(
                        text='←',
                        font_size=dp(28),
                        size_hint_x=1.2
                    )
                    btn.bg_color.rgba = (0.6, 0.2, 0.2, 1)  # Vermelho
                elif key == 'OK':
                    btn = BrandedButton(
                        text='✓',
                        font_size=dp(32),
                        size_hint_x=1.0
                    )
                elif key == 'ESPACO':
                    btn = VirtualKeyButton(
                        text='ESPAÇO',
                        font_size=dp(18),
                        size_hint_x=2.0
                    )
                else:
                    btn = VirtualKeyButton(
                        text=key,
                        font_size=dp(28),
                        size_hint_x=1.0
                    )
                
                btn.bind(on_press=lambda instance, k=key: self.on_key_press(k))
                row.add_widget(btn)
            
            self.add_widget(row)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class ScoreEntryScreen(Screen):
    """Tela de entrada de pontuação com identidade visual IBP."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.ranking = RankingManager()
        
        # Layout raiz
        root = FloatLayout()
        
        # ===== FUNDO BRANCO COM GRÁFICO =====
        with root.canvas.before:
            Color(*COLOR_WHITE)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *args: setattr(self.bg_rect, 'pos', root.pos))
        root.bind(size=lambda *args: setattr(self.bg_rect, 'size', root.size))
        
        # Gráfico de fundo (opacity baixa)
        bg_graphic = Image(
            source='assets/images/background_graphic.png',
            allow_stretch=True,
            keep_ratio=False,
            opacity=0.15,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        root.add_widget(bg_graphic)
        
        # ===== TECLADO NA BASE (30%) =====
        self.keyboard = CompactVirtualKeyboard(
            on_key_press=self.handle_key_press,
            size_hint=(1, 0.30),
            pos_hint={'x': 0, 'y': 0}
        )
        root.add_widget(self.keyboard)
        
        # ===== ÁREA DE CONTEÚDO (70%) =====
        content_area = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(60), dp(30), dp(60), dp(30)],
            size_hint=(1, 0.70),
            pos_hint={'x': 0, 'y': 0.30}
        )
        
        # Espaçador superior
        content_area.add_widget(BoxLayout(size_hint_y=0.05))
        
        # Container com fundo cinza claro
        content_box = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(40),
            size_hint_y=0.85
        )
        
        # Fundo cinza claro arredondado
        with content_box.canvas.before:
            Color(*COLOR_LIGHT_GRAY)
            self.content_bg = RoundedRectangle(
                pos=content_box.pos,
                size=content_box.size,
                radius=[dp(30)]
            )
        content_box.bind(
            pos=lambda *args: setattr(self.content_bg, 'pos', content_box.pos),
            size=lambda *args: setattr(self.content_bg, 'size', content_box.size)
        )
        
        # 1. Título
        title_label = Label(
            text='SUA PONTUAÇÃO',
            font_name='Roboto',
            font_size=dp(48),
            bold=True,
            color=COLOR_PRIMARY_GREEN,
            size_hint_y=0.15,
            halign='center',
            valign='middle',
            outline_width=2,
            outline_color=COLOR_PRIMARY_BLUE
        )
        title_label.bind(size=title_label.setter('text_size'))
        content_box.add_widget(title_label)
        
        # 2. Pontuação
        self.score_label = Label(
            text='0',
            font_name='Roboto',
            font_size=dp(80),
            bold=True,
            color=COLOR_PRIMARY_BLUE,
            size_hint_y=0.20,
            halign='center',
            valign='middle',
            outline_width=3,
            outline_color=COLOR_PRIMARY_GREEN
        )
        self.score_label.bind(size=self.score_label.setter('text_size'))
        content_box.add_widget(self.score_label)
        
        # 3. Avaliação em estrelas (texto, sem emoji)
        self.stars_label = Label(
            text='',
            font_name='Roboto',
            font_size=dp(36),
            bold=True,
            color=COLOR_SECONDARY_BLUE,
            size_hint_y=0.12,
            halign='center',
            valign='middle'
        )
        self.stars_label.bind(size=self.stars_label.setter('text_size'))
        content_box.add_widget(self.stars_label)
        
        # Espaçador
        content_box.add_widget(BoxLayout(size_hint_y=0.08))
        
        # 4. Label de instrução
        instruction_label = Label(
            text='Digite seu nome:',
            font_name='Roboto',
            font_size=dp(32),
            color=COLOR_PRIMARY_BLUE,
            size_hint_y=0.10,
            halign='center',
            valign='middle'
        )
        instruction_label.bind(size=instruction_label.setter('text_size'))
        content_box.add_widget(instruction_label)
        
        # 5. Campo de entrada (como label)
        input_container = AnchorLayout(
            size_hint_y=0.18,
            anchor_x='center',
            anchor_y='center'
        )
        
        input_box = BoxLayout(
            size_hint=(0.85, 1),
            padding=dp(15)
        )
        
        # Fundo branco do input
        with input_box.canvas.before:
            Color(*COLOR_WHITE)
            self.input_bg = RoundedRectangle(
                pos=input_box.pos,
                size=input_box.size,
                radius=[dp(15)]
            )
            Color(*COLOR_PRIMARY_BLUE)
            self.input_border = RoundedRectangle(
                pos=input_box.pos,
                size=input_box.size,
                radius=[dp(15)]
            )
        input_box.bind(
            pos=self._update_input_bg,
            size=self._update_input_bg
        )
        
        self.name_display = Label(
            text='',
            font_name='Roboto',
            font_size=dp(38),
            bold=True,
            color=COLOR_WHITE,
            halign='center',
            valign='middle'
        )
        self.name_display.bind(size=self.name_display.setter('text_size'))
        
        input_box.add_widget(self.name_display)
        input_container.add_widget(input_box)
        content_box.add_widget(input_container)
        
        # Espaçador
        content_box.add_widget(BoxLayout(size_hint_y=0.05))
        
        # 6. Botão de enviar
        button_container = AnchorLayout(
            size_hint_y=0.12,
            anchor_x='center',
            anchor_y='center'
        )
        
        self.submit_btn = BrandedButton(
            text='ENVIAR PONTUAÇÃO',
            font_size=dp(40),
            size_hint=(0.7, 1)
        )
        self.submit_btn.bind(on_press=self.submit_score)
        
        button_container.add_widget(self.submit_btn)
        content_box.add_widget(button_container)
        
        content_area.add_widget(content_box)
        
        # Espaçador inferior
        content_area.add_widget(BoxLayout(size_hint_y=0.10))
        
        root.add_widget(content_area)
        self.add_widget(root)
    
    def _update_input_bg(self, instance, value):
        """Atualiza fundo do input."""
        # Fundo branco
        self.input_bg.pos = (instance.pos[0] + dp(2), instance.pos[1] + dp(2))
        self.input_bg.size = (instance.size[0] - dp(4), instance.size[1] - dp(4))
        # Borda azul
        self.input_border.pos = instance.pos
        self.input_border.size = instance.size
    
    def handle_key_press(self, key):
        """Processa entrada do teclado virtual."""
        current_text = self.name_display.text
        
        if key == 'APAGAR':
            self.name_display.text = current_text[:-1]
        
        elif key == 'ESPACO':
            if len(current_text) < 20:
                self.name_display.text = current_text + ' '
        
        elif key == 'OK':
            self.submit_score(None)
        
        else:
            if len(current_text) < 20:
                self.name_display.text = current_text + key
    
    def set_score(self, score: int):
        """Define pontuação para exibir."""
        self.score = score
        self.score_label.text = str(score)
        
        # Avaliação em texto (sem emojis)
        if score >= 90:
            rating = 'EXCELENTE!'
        elif score >= 75:
            rating = 'MUITO BOM!'
        elif score >= 60:
            rating = 'BOM'
        elif score >= 40:
            rating = 'REGULAR'
        else:
            rating = 'CONTINUE PRATICANDO'
        
        self.stars_label.text = rating
    
    def on_enter(self):
        """Limpa entrada ao entrar na tela."""
        self.name_display.text = ''
        print(f"\n{'='*50}")
        print(f"🎯 Tela de Entrada de Pontuação - Pontos: {self.score}")
        print(f"{'='*50}")
    
    def submit_score(self, instance):
        """Envia pontuação para o ranking."""
        name = self.name_display.text.strip()

        # Validação
        if not name:
            print("❌ Nome obrigatório")
            self.name_display.color = (1, 0, 0, 1)  # Vermelho
            return

        if len(name) < 3:
            print("❌ Nome muito curto (mínimo 3 caracteres)")
            self.name_display.color = (1, 0, 0, 1)
            return

        # Restaura cor
        self.name_display.color = COLOR_WHITE

        # Salva no ranking
        success = self.ranking.add_score(name, self.score)

        if success:
            print(f"✅ Pontuação salva: {name} = {self.score}")

            # Navigate to leaderboard screen
            app = App.get_running_app()
            app.app_manager.show_leaderboard(player_name=name)
        else:
            print("❌ Falha ao salvar pontuação")
