"""
Tela de parabéns - fim do karaoke.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class CongratulationsScreen(Screen):
    """Tela de parabéns."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20
        )
        
        # Título
        title = Label(
            text='🎉 PARABÉNS! 🎉',
            font_size='70sp',
            bold=True,
            color=(1, 0.84, 0, 1),  # Dourado
            size_hint_y=0.3
        )
        layout.add_widget(title)
        
        # Mensagem
        message = Label(
            text=(
                'Você arrasou no karaoke!\n\n'
                'Obrigado por participar da\n'
                'ativação IBP 2025'
            ),
            font_size='40sp',
            halign='center',
            valign='middle',
            size_hint_y=0.5
        )
        layout.add_widget(message)
        
        # Botão jogar novamente
        restart_btn = Button(
            text='🔄 JOGAR NOVAMENTE',
            font_size='40sp',
            size_hint_y=0.2
        )
        restart_btn.bind(on_press=self.restart)
        layout.add_widget(restart_btn)
        
        self.add_widget(layout)
    
    def restart(self, instance):
        """Reiniciar jogo (volta para welcome)."""
        self.manager.current = 'welcome'