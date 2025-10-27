"""Script de teste para a tela de entrada de pontuação com identidade IBP.

Este script demonstra a nova tela com:
- Cores da marca IBP
- Textos em português
- Sem emojis (avaliação em texto)
- Background branco com gráfico
- Botões estilizados (BrandedButton)
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.config import Config

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'docs', 'id visual'))
from score_entry_screen_ibp import ScoreEntryScreen


# Mock RankingManager para teste
class MockRankingManager:
    def add_score(self, name, score):
        print(f"[MOCK] Salvaria: {name} = {score} pontos")
        return True


class TestApp(App):
    """Aplicação de teste para tela de entrada de pontuação."""
    
    def build(self):
        # Tamanho do kiosque (1920x1080)
        Window.size = (1920, 1080)
        
        # Criar gerenciador de telas
        sm = ScreenManager()
        
        # Criar tela de entrada de pontuação
        score_screen = ScoreEntryScreen(name='score_entry')
        
        # Mock do gerenciador de ranking
        score_screen.ranking = MockRankingManager()
        
        # Definir pontuação de teste
        score_screen.set_score(78)  # 78 pontos = "MUITO BOM!"
        
        sm.add_widget(score_screen)
        sm.current = 'score_entry'
        
        return sm


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎨 TESTANDO TELA DE ENTRADA DE PONTUAÇÃO - IDENTIDADE VISUAL IBP")
    print("="*70)
    print("\n📋 Características Aplicadas:")
    print("  ✅ Cores da marca IBP")
    print("     • Azul primário: #004077")
    print("     • Verde primário: #86BC25")
    print("     • Fundo branco com gráfico")
    print("     • Container cinza claro")
    print("")
    print("  ✅ Textos em Português")
    print("     • 'SUA PONTUAÇÃO'")
    print("     • 'Digite seu nome:'")
    print("     • 'ENVIAR PONTUAÇÃO'")
    print("     • 'APAGAR', 'ESPAÇO', 'OK'")
    print("")
    print("  ✅ Sem Emojis")
    print("     • Avaliação: 'MUITO BOM!' (em vez de ★★★★☆)")
    print("     • Escala:")
    print("       - 90-100: EXCELENTE!")
    print("       - 75-89: MUITO BOM!")
    print("       - 60-74: BOM")
    print("       - 40-59: REGULAR")
    print("       - 0-39: CONTINUE PRATICANDO")
    print("")
    print("  ✅ Estilo de Botões")
    print("     • BrandedButton (verde com bordas arredondadas)")
    print("     • VirtualKeyButton (cinza com bordas arredondadas)")
    print("     • Efeito de pressionamento")
    print("")
    print("\n📐 Layout:")
    print("  ┌─────────────────────────────────────────────────┐")
    print("  │ FUNDO BRANCO + background_graphic.png           │")
    print("  │                                                 │")
    print("  │  ╔════════════════════════════════════════╗     │")
    print("  │  ║ [Container Cinza Claro]                ║     │")
    print("  │  ║                                        ║     │")
    print("  │  ║  SUA PONTUAÇÃO (verde + borda azul)    ║     │")
    print("  │  ║  78 (azul + borda verde)               ║     │")
    print("  │  ║  MUITO BOM! (azul secundário)          ║     │")
    print("  │  ║                                        ║     │")
    print("  │  ║  Digite seu nome:                      ║     │")
    print("  │  ║  [campo branco com borda azul]         ║     │")
    print("  │  ║                                        ║     │")
    print("  │  ║  [ENVIAR PONTUAÇÃO] (botão verde)      ║     │")
    print("  │  ║                                        ║     │")
    print("  │  ╚════════════════════════════════════════╝     │")
    print("  ├─────────────────────────────────────────────────┤")
    print("  │  ╔════════════════════════════════════════╗     │")
    print("  │  ║ [Teclado Cinza Escuro]                 ║     │")
    print("  │  ║                                        ║     │")
    print("  │  ║  [1][2][3][4][5][6][7][8][9][0][←]    ║     │")
    print("  │  ║  [Q][W][E][R][T][Y][U][I][O][P]       ║     │")
    print("  │  ║  [A][S][D][F][G][H][J][K][L]          ║     │")
    print("  │  ║  [Z][X][C][V][B][N][M][ESPAÇO][✓]     ║     │")
    print("  │  ║                                        ║     │")
    print("  │  ╚════════════════════════════════════════╝     │")
    print("  └─────────────────────────────────────────────────┘")
    print("")
    print("\n🎮 Controles:")
    print("  • Digite usando o teclado na tela")
    print("  • ← (APAGAR) = Remove último caractere")
    print("  • ESPAÇO = Adiciona espaço")
    print("  • ✓ (OK) = Envia pontuação")
    print("  • Botão 'ENVIAR PONTUAÇÃO' também funciona")
    print("  • Limite: 20 caracteres")
    print("  • Mínimo: 3 caracteres para enviar")
    print("")
    print("\n⚠️  Observação:")
    print("  Se o arquivo 'background_graphic.png' não existir,")
    print("  a tela ficará apenas com fundo branco (sem gráfico).")
    print("  O resto funcionará normalmente.")
    print("")
    print("="*70 + "\n")
    
    TestApp().run()
