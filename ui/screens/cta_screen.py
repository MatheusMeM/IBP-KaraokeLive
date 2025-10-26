"""
Tela de CTA - transição entre ensaio e performance.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class CTAScreen(Screen):
    """Tela de CTA (Call to Action)."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20
        )
        
        # Título
        title = Label(
            text='🎉 ÓTIMO ENSAIO!',
            font_size='60sp',
            bold=True,
            size_hint_y=0.3
        )
        layout.add_widget(title)
        
        # Mensagem
        message = Label(
            text=(
                'Agora é pra valer!\n\n'
                'Cante com confiança e mostre seu talento.\n\n'
                'Pronto para começar?'
            ),
            font_size='40sp',
            halign='center',
            valign='middle',
            size_hint_y=0.5
        )
        layout.add_widget(message)
        
        # Botão
        start_btn = Button(
            text='▶ VALENDO!',
            font_size='50sp',
            bold=True,
            size_hint_y=0.2
        )
        start_btn.bind(on_press=self.start_performance)
        layout.add_widget(start_btn)
        
        self.add_widget(layout)
    
    def start_performance(self, instance):
        """Ir para countdown antes da performance."""
        # Configurar próximo destino do countdown
        countdown = self.manager.get_screen('countdown')
        countdown.next_screen = 'performance'
        
        self.manager.current = 'countdown'