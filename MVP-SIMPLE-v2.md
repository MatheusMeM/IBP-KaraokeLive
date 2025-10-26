# 🎯 MVP SIMPLICÍSSIMO - IBP-KaraokeLive (Adaptado da Estrutura Existente)

**Status:** Fase 0 ✅ COMPLETO  
**Nova Direção:** MVP extremamente simples, sem parsing complexo  
**Data:** 2025-10-26

---

## 🚨 DECISÃO ARQUITETURAL

**UltraStar Parser abandonado** — complexo demais para o prazo.

**Nova abordagem:** Arquivo de letras simples em JSON/TXT puro com timestamps manuais.

---

## 🎬 FLUXO SIMPLIFICADO (10 Telas)

```
1. Welcome Screen (Idle)    → "PLAY" button
2. Instructions Screen      → "ENSAIO" button
3. Countdown Screen (3,2,1) → Auto-advance
4. Rehearsal Screen         → Música + letras (FONE apenas)
5. CTA Screen              → "VALENDO" button
6. Countdown Screen (3,2,1) → Auto-advance (reuso da mesma tela)
7. Performance Screen       → Música + letras (FONE + CAIXA)
8. Congratulations Screen   → "JOGAR NOVAMENTE" button
9. → Volta para Welcome
```

**Pontos críticos:**
- **SEM detecção de pitch**
- **SEM pontuação**
- **SEM parsing complexo**
- Apenas exibição sincronizada de letras

---

## 📁 ESTRUTURA REAL DO PROJETO (Mantendo arquivos existentes)

```
IBP-KaraokeLive/
├── config/
│   ├── __init__.py
│   └── app_config.py          # ✅ Já existe - adicionar AUDIO/LYRICS paths
│
├── data/
│   ├── __init__.py
│   ├── leaderboard.json       # ⚠️ MANTER - futuro uso
│   ├── ranking_manager.py     # ⚠️ MANTER - futuro uso
│   └── lyrics.json            # 🆕 NOVO - letras do jingle
│
├── ui/
│   ├── __init__.py
│   ├── app_manager.py         # ✏️ MODIFICAR - adicionar novas screens
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── screens.py         # ⚠️ MANTER - base classes
│   │   ├── screens.kv         # ✏️ MODIFICAR - adicionar layouts novos
│   │   ├── welcome_screen.py  # ✅ Já existe
│   │   ├── instructions_screen.py  # ✏️ MODIFICAR - adicionar botão ENSAIO
│   │   ├── countdown_screen.py     # 🆕 NOVO
│   │   ├── rehearsal_screen.py     # 🆕 NOVO
│   │   ├── cta_screen.py           # 🆕 NOVO
│   │   ├── performance_screen.py   # 🆕 NOVO
│   │   ├── congratulations_screen.py # 🆕 NOVO
│   │   └── leaderboard_screen.py   # ⚠️ MANTER - futuro uso
│   │
│   └── widgets/
│       └── __init__.py
│
├── modules/                   # 🆕 NOVA PASTA
│   ├── __init__.py
│   ├── audio_player.py        # 🆕 NOVO
│   ├── audio_router.py        # 🆕 NOVO
│   └── lyric_display.py       # 🆕 NOVO
│
├── assets/
│   ├── audio/
│   │   └── jingle_ibp.mp3     # 🆕 NOVO - música do jingle
│   ├── fonts/
│   ├── images/
│   │   ├── background_graphic.png  # ✅ Já existe
│   │   ├── ibp_logo.png           # ✅ Já existe
│   │   └── ibp_logo_simples.png   # ✅ Já existe
│   └── video/
│
├── ref_code/                  # ⚠️ MANTER - código de referência
│
├── venv/                      # ✅ Já existe
├── main.py                    # ✅ Já existe
├── requirements.txt           # ✅ Já existe
├── STATUS.md                  # ✅ Já existe
├── .gitignore                 # ✅ Já existe
└── MVP-SIMPLE.md              # 📄 Este documento

LEGENDA:
✅ Já existe - não mexer
⚠️ MANTER - não usar agora, mas manter para futuro
🆕 NOVO - criar do zero
✏️ MODIFICAR - adicionar código novo ao existente
```

---

## 📝 ARQUIVO DE LETRAS SIMPLES (data/lyrics.json) - NOVO

Formato extremamente simples — sem parsing complexo:

```json
{
  "title": "Jingle IBP 2025",
  "artist": "IBP",
  "audio_file": "assets/audio/jingle_ibp.mp3",
  "duration": 30,
  "lines": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "IBP Inovação"
    },
    {
      "start": 3.5,
      "end": 7.0,
      "text": "Energia do Futuro"
    },
    {
      "start": 7.0,
      "end": 11.0,
      "text": "Transformando o Setor"
    },
    {
      "start": 11.0,
      "end": 15.0,
      "text": "Com Sustentabilidade"
    },
    {
      "start": 15.0,
      "end": 20.0,
      "text": "IBP, o futuro é agora"
    },
    {
      "start": 20.0,
      "end": 25.0,
      "text": "Juntos construímos"
    },
    {
      "start": 25.0,
      "end": 30.0,
      "text": "O amanhã melhor"
    }
  ]
}
```

**Criação manual:**
1. Ouvir o jingle
2. Anotar tempos aproximados
3. Escrever JSON à mão

---

## ⚙️ MODIFICAÇÕES EM config/app_config.py

**Adicionar ao arquivo existente:**

```python
# Adicionar estas linhas ao final do app_config.py existente

# Karaoke Paths (NOVO)
AUDIO_FILE = 'assets/audio/jingle_ibp.mp3'
LYRICS_FILE = 'data/lyrics.json'

# Karaoke Timing (NOVO)
COUNTDOWN_SECONDS = 3
```

**NÃO remover** nenhuma configuração existente. Apenas adicionar as linhas acima.

---

## 🧩 MÓDULOS CORE (Nova pasta modules/) - CRIAR

### 1. modules/audio_player.py - NOVO

```python
"""
Player de áudio simples usando Kivy SoundLoader.
"""
from kivy.core.audio import SoundLoader
from pathlib import Path


class SimpleAudioPlayer:
    """Reprodutor de áudio básico."""
    
    def __init__(self, audio_path: str):
        """
        Args:
            audio_path: Caminho para arquivo de áudio
        """
        self.audio_path = Path(audio_path)
        self.sound = None
        self.is_loaded = False
        
        self._load()
    
    def _load(self):
        """Carregar arquivo de áudio."""
        if not self.audio_path.exists():
            print(f"❌ Arquivo não encontrado: {self.audio_path}")
            return
        
        self.sound = SoundLoader.load(str(self.audio_path))
        
        if self.sound:
            self.is_loaded = True
            print(f"✅ Áudio carregado: {self.audio_path.name}")
        else:
            print(f"❌ Erro ao carregar: {self.audio_path}")
    
    def play(self):
        """Tocar áudio."""
        if self.sound and self.is_loaded:
            self.sound.play()
    
    def stop(self):
        """Parar áudio."""
        if self.sound:
            self.sound.stop()
    
    def get_position(self) -> float:
        """Retorna posição atual em segundos."""
        if self.sound and self.sound.state == 'play':
            return self.sound.get_pos()
        return 0.0
    
    def get_duration(self) -> float:
        """Retorna duração total em segundos."""
        if self.sound:
            return self.sound.length
        return 0.0
    
    def is_playing(self) -> bool:
        """Verifica se está tocando."""
        return self.sound and self.sound.state == 'play'
```

---

### 2. modules/audio_router.py - NOVO

```python
"""
Controle de saída de áudio (fone vs caixa).
Versão simplificada: assume configuração manual do Windows.
"""


class AudioRouter:
    """
    Gerenciador de roteamento de áudio.
    
    NOTA: No Windows, o roteamento é feito via configuração
    do sistema operacional (Settings > Sound > App volume).
    """
    
    def __init__(self):
        self.mode = 'headphone'  # 'headphone' ou 'both'
    
    def set_rehearsal_mode(self):
        """Modo ensaio (apenas fone)."""
        self.mode = 'headphone'
        print("🎧 Modo: Apenas fone de ouvido")
        print("   Configure Windows Audio para direcionar para fone USB")
    
    def set_performance_mode(self):
        """Modo performance (fone + caixa)."""
        self.mode = 'both'
        print("🔊 Modo: Fone + Caixa de som")
        print("   Configure Windows Audio para usar ambos dispositivos")
    
    def get_instructions(self) -> str:
        """Retorna instruções para usuário."""
        if self.mode == 'headphone':
            return (
                "ENSAIO: Configure saída de áudio para fone USB\n"
                "Windows Settings > Sound > Output Device"
            )
        else:
            return (
                "PERFORMANCE: Configure saída de áudio para ambos\n"
                "Windows Settings > Sound > App volume and device preferences"
            )
```

---

### 3. modules/lyric_display.py - NOVO

```python
"""
Sincronização e exibição de letras.
"""
import json
from pathlib import Path
from typing import Optional, Dict, List


class LyricLine:
    """Representa uma linha de letra."""
    
    def __init__(self, start: float, end: float, text: str):
        self.start = start
        self.end = end
        self.text = text


class LyricDisplay:
    """Gerenciador de sincronização de letras."""
    
    def __init__(self, lyrics_file: str):
        """
        Args:
            lyrics_file: Caminho para arquivo JSON de letras
        """
        self.lyrics_file = Path(lyrics_file)
        self.lines: List[LyricLine] = []
        self.current_index = 0
        
        self._load()
    
    def _load(self):
        """Carregar arquivo de letras."""
        if not self.lyrics_file.exists():
            print(f"❌ Arquivo de letras não encontrado: {self.lyrics_file}")
            return
        
        with open(self.lyrics_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Converter para objetos LyricLine
        for line_data in data['lines']:
            line = LyricLine(
                start=line_data['start'],
                end=line_data['end'],
                text=line_data['text']
            )
            self.lines.append(line)
        
        print(f"✅ {len(self.lines)} linhas de letra carregadas")
    
    def get_current_line(self, current_time: float) -> Optional[LyricLine]:
        """
        Retorna linha atual baseada no tempo.
        
        Args:
            current_time: Tempo atual em segundos
            
        Returns:
            LyricLine se encontrado, None caso contrário
        """
        for i, line in enumerate(self.lines):
            if line.start <= current_time < line.end:
                self.current_index = i
                return line
        
        return None
    
    def get_context_lines(
        self, 
        current_time: float
    ) -> Dict[str, Optional[str]]:
        """
        Retorna linha anterior, atual e próxima.
        
        Returns:
            Dict com 'prev', 'current', 'next'
        """
        current = self.get_current_line(current_time)
        
        result = {
            'prev': None,
            'current': None,
            'next': None
        }
        
        if not current:
            return result
        
        idx = self.current_index
        
        # Linha anterior
        if idx > 0:
            result['prev'] = self.lines[idx - 1].text
        
        # Linha atual
        result['current'] = current.text
        
        # Próxima linha
        if idx < len(self.lines) - 1:
            result['next'] = self.lines[idx + 1].text
        
        return result
```

---

## 🎨 NOVAS TELAS (ui/screens/) - CRIAR

### ui/screens/countdown_screen.py - NOVO

```python
"""
Tela de countdown (3, 2, 1...).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from config.app_config import COUNTDOWN_SECONDS


class CountdownScreen(Screen):
    """
    Tela de countdown antes do karaoke.
    Pode ser reutilizada para ensaio e performance.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.label = Label(
            text='3',
            font_size='200sp',
            bold=True
        )
        self.add_widget(self.label)
        
        self.counter = COUNTDOWN_SECONDS
        self.next_screen = 'rehearsal'  # Default, pode ser mudado
    
    def on_enter(self):
        """Iniciar countdown ao entrar na tela."""
        self.counter = COUNTDOWN_SECONDS
        self.label.text = str(self.counter)
        Clock.schedule_interval(self.update_countdown, 1.0)
    
    def update_countdown(self, dt):
        """Atualizar número do countdown."""
        self.counter -= 1
        
        if self.counter > 0:
            self.label.text = str(self.counter)
        else:
            # Ir para próxima tela
            self.manager.current = self.next_screen
            return False  # Parar clock
```

---

### ui/screens/rehearsal_screen.py - NOVO

```python
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
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
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
```

---

### ui/screens/cta_screen.py - NOVO

```python
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
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
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
```

---

### ui/screens/performance_screen.py - NOVO

```python
"""
Tela de performance - música com letras (fone + caixa).
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from modules.audio_player import SimpleAudioPlayer
from modules.audio_router import AudioRouter
from modules.lyric_display import LyricDisplay
from config.app_config import AUDIO_FILE, LYRICS_FILE


class PerformanceScreen(Screen):
    """Tela de performance do karaoke."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Componentes
        self.audio_player = SimpleAudioPlayer(AUDIO_FILE)
        self.lyric_display = LyricDisplay(LYRICS_FILE)
        self.audio_router = AudioRouter()
        
        # UI (similar ao RehearsalScreen, mas com visual diferente)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título com indicador "AO VIVO"
        title = Label(
            text='🔴 PERFORMANCE AO VIVO',
            font_size='40sp',
            color=(1, 0, 0, 1),  # Vermelho
            size_hint_y=0.1
        )
        layout.add_widget(title)
        
        # Linha anterior
        self.prev_label = Label(
            text='',
            font_size='25sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.2
        )
        layout.add_widget(self.prev_label)
        
        # Linha atual (amarelo brilhante)
        self.current_label = Label(
            text='Aguarde...',
            font_size='55sp',
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=0.4
        )
        layout.add_widget(self.current_label)
        
        # Próxima linha
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
        """Iniciar performance."""
        # Configurar roteamento (fone + caixa)
        self.audio_router.set_performance_mode()
        
        # Tocar música
        self.audio_player.play()
        
        # Agendar atualização
        self.update_event = Clock.schedule_interval(self.update, 1/30)
    
    def update(self, dt):
        """Atualizar letras e timer."""
        current_time = self.audio_player.get_position()
        duration = self.audio_player.get_duration()
        
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
        
        # Verificar fim
        if not self.audio_player.is_playing():
            self.finish_performance()
    
    def finish_performance(self):
        """Finalizar e ir para congratulations."""
        if self.update_event:
            self.update_event.cancel()
        
        self.audio_player.stop()
        
        # Ir para tela de parabéns
        self.manager.current = 'congratulations'
    
    def on_leave(self):
        """Cleanup."""
        if self.update_event:
            self.update_event.cancel()
        self.audio_player.stop()
```

---

### ui/screens/congratulations_screen.py - NOVO

```python
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
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
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
```

---

## ✏️ MODIFICAÇÕES EM ui/app_manager.py

**Adicionar as novas telas ao ScreenManager existente:**

```python
# No método build() ou __init__ do AppManager, adicionar:

from ui.screens.countdown_screen import CountdownScreen
from ui.screens.rehearsal_screen import RehearsalScreen
from ui.screens.cta_screen import CTAScreen
from ui.screens.performance_screen import PerformanceScreen
from ui.screens.congratulations_screen import CongratulationsScreen

# Adicionar screens ao screen_manager:
self.screen_manager.add_widget(CountdownScreen(name='countdown'))
self.screen_manager.add_widget(RehearsalScreen(name='rehearsal'))
self.screen_manager.add_widget(CTAScreen(name='cta'))
self.screen_manager.add_widget(PerformanceScreen(name='performance'))
self.screen_manager.add_widget(CongratulationsScreen(name='congratulations'))
```

**NÃO remover** as screens existentes (welcome, instructions, leaderboard). Apenas adicionar as novas.

---

## 🚀 PRÓXIMOS PASSOS (Ordem de Execução)

### PASSO 1: Criar Nova Estrutura
```bash
# Criar pasta modules
mkdir -p modules
touch modules/__init__.py

# Criar arquivos novos em data
touch data/lyrics.json

# NÃO deletar data/leaderboard.json ou data/ranking_manager.py

git add .
git commit -m "chore: create modules folder and lyrics.json"
```

### PASSO 2: Implementar Módulos Core
```bash
# Copiar código dos 3 módulos:
touch modules/audio_player.py
touch modules/audio_router.py
touch modules/lyric_display.py

# Copiar código fornecido acima

git add modules/
git commit -m "feat: add core audio and lyrics modules"
```

### PASSO 3: Criar Arquivo de Letras
```bash
# Editar data/lyrics.json (copiar exemplo acima)
# Ajustar tempos ouvindo o jingle real

git add data/lyrics.json
git commit -m "feat: add lyrics data file"
```

### PASSO 4: Modificar Configuração
```bash
# Adicionar linhas ao config/app_config.py (não deletar nada existente)

git add config/app_config.py
git commit -m "feat: add karaoke config paths"
```

### PASSO 5: Criar Novas Screens
```bash
# Copiar código das 5 novas screens
touch ui/screens/countdown_screen.py
touch ui/screens/rehearsal_screen.py
touch ui/screens/cta_screen.py
touch ui/screens/performance_screen.py
touch ui/screens/congratulations_screen.py

git add ui/screens/
git commit -m "feat: add karaoke screens (countdown, rehearsal, CTA, performance, congratulations)"
```

### PASSO 6: Integrar no AppManager
```bash
# Modificar ui/app_manager.py (apenas adicionar, não remover)

git add ui/app_manager.py
git commit -m "feat: integrate new screens into app manager"
```

### PASSO 7: Adicionar Áudio
```bash
# Copiar jingle_ibp.mp3 para assets/audio/

git add assets/audio/jingle_ibp.mp3
git commit -m "feat: add IBP jingle audio file"
```

### PASSO 8: Testar Fluxo Completo
```bash
python main.py
# Navegar: Welcome → Instructions → Countdown → Rehearsal → CTA → Countdown → Performance → Congratulations
```

---

## ✅ CRITÉRIOS DE SUCESSO DO MVP

- [ ] Fluxo completo funciona sem travar
- [ ] Letras aparecem sincronizadas com áudio
- [ ] Countdown funciona (3, 2, 1)
- [ ] Música toca em rehearsal e performance
- [ ] Tela de congratulations permite reiniciar
- [ ] Sem erros de import ou runtime
- [ ] **Arquivos antigos mantidos** (leaderboard, ranking_manager)

---

## ⚠️ REGRAS IMPORTANTES

### 🚫 NÃO DELETAR:
- `data/leaderboard.json`
- `data/ranking_manager.py`
- `ui/screens/leaderboard_screen.py`
- Qualquer arquivo existente não mencionado explicitamente para modificação

### ✅ APENAS ADICIONAR:
- Nova pasta `modules/`
- Novo arquivo `data/lyrics.json`
- Novos arquivos em `ui/screens/` (5 novas telas)
- Linhas ao final de `config/app_config.py`
- Imports e registros em `ui/app_manager.py`

### 📝 TESTAR APÓS CADA PASSO:
- Executar `python main.py` após cada commit
- Verificar que não há erros de import
- Confirmar que app ainda abre (mesmo que tela não esteja pronta)

---

## 📝 PROMPT FINAL PARA ROO CODE

```markdown
# MVP SIMPLICÍSSIMO - IMPLEMENTAÇÃO (Estrutura Existente)

Seguir **MVP-SIMPLE.md** (versão atualizada).

## CONTEXTO IMPORTANTE:
- O projeto JÁ EXISTE com estrutura do Interactive Stand
- NÃO deletar arquivos existentes
- APENAS adicionar novos módulos e screens
- MANTER leaderboard e ranking_manager para uso futuro

## ORDEM DE EXECUÇÃO:

1. Criar pasta `modules/` e `modules/__init__.py`
2. Criar `modules/audio_player.py` (código fornecido)
3. Criar `modules/lyric_display.py` (código fornecido)
4. Criar `modules/audio_router.py` (código fornecido)
5. Criar `data/lyrics.json` (exemplo fornecido)
6. ADICIONAR linhas ao `config/app_config.py` (não deletar nada)
7. Criar 5 novas screens em `ui/screens/`
8. MODIFICAR `ui/app_manager.py` (apenas adicionar imports e registros)
9. Testar fluxo completo

## REGRAS CRÍTICAS:
- Copiar código EXATAMENTE como fornecido
- NÃO deletar arquivos existentes (leaderboard, ranking_manager, etc)
- NÃO adicionar features extras
- Testar após cada arquivo criado
- Commit após cada passo bem-sucedido

**COMEÇAR AGORA COM PASSO 1.**
```
