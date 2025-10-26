# Status da Adaptação - Interactive Stand → IBP Karaoke

## ✅ Completado (Fase 1 - Core Modules)
- [x] **modules/** package created with core karaoke functionality
- [x] **AudioRouter** implemented with sounddevice (device-specific routing)
- [x] **SimpleAudioPlayer** integrated with AudioRouter
- [x] **LyricDisplay** with timestamp-based synchronization
- [x] **lyrics.json** created with Jingle IBP 2025 data
- [x] **Integration tests** passing (all 4 test suites ✅)
- [x] **Audio routing tested** on Windows 11 hardware (see AUDIO-ROUTING-TEST-RESULTS.md)
- [x] **PEP 8 compliance** verified across all modules
- [x] **Separation of concerns** maintained (audio, routing, lyrics independent)

## ✅ Completado (Fase 0)
- [x] Projeto base criado (ref_code contém interactive-stand-game como referência)
- [x] Resolução mudada para 1920x1080 horizontal
- [x] Código GPIO removido (sem dependências Raspberry Pi)
- [x] Jogos (quiz/agility) removidos
- [x] Sistema de ranking implementado (teste adiado para fase posterior)
- [x] Fluxo básico funciona (Welcome → Instructions → Welcome)
- [x] Virtual environment configurado (Kivy 2.3.1)

## 📁 Estrutura de Arquivos

```
IBP-KaraokeLive/
├── config/
│   ├── __init__.py
│   └── app_config.py          # Configuration (1920x1080, karaoke paths)
├── data/
│   ├── __init__.py
│   ├── leaderboard.json       # Persistent leaderboard data
│   ├── lyrics.json            # ✨ NEW: Jingle IBP 2025 lyrics with timestamps
│   └── ranking_manager.py     # Leaderboard logic with atomic writes
├── modules/                   # ✨ NEW: Core karaoke modules
│   ├── __init__.py
│   ├── audio_player.py        # Audio playback with routing support
│   ├── audio_router.py        # Device-specific audio routing (sounddevice)
│   └── lyric_display.py       # Timestamp-based lyric synchronization
├── tests/                     # ✨ NEW: Integration tests
│   ├── __init__.py
│   ├── test_audio_routing.py  # Hardware audio routing tests
│   └── test_core_modules.py   # Core modules integration tests
├── ui/
│   ├── __init__.py
│   ├── app_manager.py         # Simple orchestrator (no game logic)
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── screens.py         # WelcomeScreen base
│   │   ├── screens.kv         # Kivy layouts (horizontal 1920x1080)
│   │   ├── instructions_screen.py
│   │   ├── leaderboard_screen.py
│   │   └── welcome_screen.py
│   └── widgets/
│       └── __init__.py
├── assets/
│   ├── audio/
│   ├── fonts/
│   ├── images/
│   │   ├── background_graphic.png
│   │   ├── ibp_logo.png
│   │   └── ibp_logo_simples.png
│   └── video/
├── venv/                      # Virtual environment (Python 3.13, Kivy 2.3.1)
├── main.py                    # Entry point (Windows 11, no GPIO)
├── requirements.txt           # kivy, sounddevice, soundfile, numpy
├── MVP-SIMPLE-v2.md           # MVP specification (simplified approach)
├── AUDIO-ROUTING-TEST-RESULTS.md  # Hardware test results
├── STATUS.md                  # This status documentation
└── .gitignore
```

## 🐛 Problemas Encontrados e Resolvidos

### Durante Setup
1. **Missing screen classes** - InstructionsScreen e LeaderboardScreen precisaram ser criadas separadamente
2. **Missing methods** - Adicionados `proceed_from_instructions()` e `update_content()` ao AppManager
3. **Logo size** - Aumentado de 40% para 60% para melhor visibilidade em 1920x1080
4. **Kivy dependencies** - Instaladas todas as dependências Windows (angle, glew, sdl2)

### Observações Importantes
- **ScoreScreen e virtual keyboard mantidos** para uso futuro no karaoke (entrada de nome do jogador)
- **Todos os componentes GPIO removidos** com sucesso (sem erros de import)
- **Sem dependências de Raspberry Pi** (gpiozero, lgpio eliminados)
- **Separação de responsabilidades** mantida (AppManager = orchestrator, Screens = UI)

## ✅ Critérios de Sucesso da Fase 0 - ATINGIDOS

- [x] Projeto roda no Windows 11 Mini-PC
- [x] Janela abre em 1920x1080 (horizontal)
- [x] Sem erros de GPIO ou bibliotecas faltando
- [x] Navegação entre telas funciona (mouse, teclado ESC/R)
- [x] Sistema de ranking implementado (teste pendente)
- [x] Código limpo (sem jogos ou GPIO)

## 🔄 Próximos Passos (Fase 2 - UI Screens Integration)

### 1. Create Karaoke Screens (MVP-SIMPLE-v2.md)
- [ ] **CountdownScreen** - 3-2-1 countdown before singing
- [ ] **RehearsalScreen** - Practice with lyrics (headphones only)
- [ ] **CTAScreen** - Transition screen between rehearsal and performance
- [ ] **PerformanceScreen** - Live performance (headphones + speakers)
- [ ] **CongratulationsScreen** - End screen with play again option

### 2. Integrate Screens with AppManager
- [ ] Import and register all new screens
- [ ] Wire up navigation flow (Welcome → Instructions → Countdown → Rehearsal → CTA → Countdown → Performance → Congratulations → Welcome)
- [ ] Test complete flow without audio first
- [ ] Add audio integration to screens

### 3. Audio File Preparation
- [ ] Convert Jingle IBP 2025 to MP3 format
- [ ] Place audio file in `assets/audio/jingle_ibp.mp3`
- [ ] Adjust lyrics.json timestamps to match actual audio
- [ ] Test synchronization with actual audio file

### 4. Fine-tuning & Testing
- [ ] Test full karaoke flow on target hardware
- [ ] Verify audio routing works correctly (device 8 = speakers, device 9 = headphones)
- [ ] Adjust lyric timing if needed
- [ ] Test mode transitions (rehearsal → performance)
- [ ] Verify countdown timing (3 seconds)

## 🎯 Estratégia de Desenvolvimento (Building Blocks)

Seguindo a abordagem incremental da Fase 0:
1. **Testar cada componente isoladamente** antes de integração
2. **Um componente por vez** (não acumular mudanças)
3. **Commits frequentes** após cada sucesso
4. **Documentar decisões** e problemas encontrados
5. **Se quebrar:** reverter e tentar abordagem diferente

## 📚 Referências Técnicas

### Código de Referência
- `ref_code/interactive-stand-game/` - Base do projeto (Kivy + navegação)
- `ref_code/ultrastar_parser.py` - Parser de arquivos .txt
- `ref_code/pitcher.py` - Pitch detection com CREPE
- `ref_code/ultrastar_score_calculator.py` - Sistema de pontuação
- `ref_code/ultrastar_writer.py` - Escrita de arquivos UltraStar

### Bibliotecas Principais (implementadas)
- ✅ `sounddevice` - Device-specific audio routing
- ✅ `soundfile` - Audio file loading
- ✅ `numpy` - Audio data processing
- ✅ `kivy` - UI framework

### Hardware Configuration (Windows 11)
- **Device 8:** Speakers (Realtek) - Public/audience output
- **Device 9:** Speakers (USB Audio Device) - Singer/headphones
- **Latency:** ~30ms (acceptable for karaoke)
- **Sample Rate:** 44100 Hz (tested and working)

## 🎤 Next Milestone

**Phase 2 complete when:**
- [ ] All karaoke screens implemented (5 screens)
- [ ] Full navigation flow working
- [ ] Audio plays with correct routing (rehearsal vs performance)
- [ ] Lyrics display synchronized with audio
- [ ] User can complete full karaoke experience

---

**Fase 0 concluída:** 2025-10-26 (Base project structure)
**Fase 1 concluída:** 2025-10-26 (Core modules with audio routing)
**Status atual:** ✅ FASE 1 COMPLETA - Pronto para Fase 2 (UI Integration)

---

## 📊 Phase 1 Technical Details

### Core Modules Architecture
All modules follow PEP 8 standards and separation of concerns:

1. **`modules/audio_router.py`** (219 lines)
   - Direct hardware audio routing using `sounddevice`
   - Device-specific playback (speakers vs headphones)
   - Threading for simultaneous playback on multiple devices
   - Based on successful hardware tests (AUDIO-ROUTING-TEST-RESULTS.md)

2. **`modules/audio_player.py`** (107 lines)
   - High-level audio playback interface
   - Integrates with AudioRouter for device routing
   - Provides simple play/stop/position API
   - Duration calculation from audio data

3. **`modules/lyric_display.py`** (144 lines)
   - Timestamp-based lyric synchronization
   - Context lines (previous, current, next)
   - JSON-based lyric file format
   - No audio or UI dependencies (pure data logic)

### Test Coverage
All modules tested with integration tests:
- ✅ AudioRouter basic functionality
- ✅ SimpleAudioPlayer integration
- ✅ LyricDisplay synchronization
- ✅ Full integration (all modules working together)

### Configuration Updates
- `config/app_config.py` extended with:
  - `AUDIO_FILE = 'assets/audio/jingle_ibp.mp3'`
  - `LYRICS_FILE = 'data/lyrics.json'`
  - `COUNTDOWN_SECONDS = 3`