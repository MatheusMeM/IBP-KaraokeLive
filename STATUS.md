# Status da Adaptação - Interactive Stand → IBP Karaoke

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
│   └── app_config.py          # Configuration (1920x1080, colors, timing)
├── data/
│   ├── __init__.py
│   ├── leaderboard.json       # Persistent leaderboard data
│   └── ranking_manager.py     # Leaderboard logic with atomic writes
├── ui/
│   ├── __init__.py
│   ├── app_manager.py         # Simple orchestrator (no game logic)
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── screens.py         # WelcomeScreen base
│   │   ├── screens.kv         # Kivy layouts (horizontal 1920x1080)
│   │   ├── instructions_screen.py
│   │   └── leaderboard_screen.py
│   └── widgets/
│       └── __init__.py
├── assets/
│   └── images/
│       ├── background_graphic.png
│       ├── ibp_logo.png
│       └── ibp_logo_simples.png
├── ref_code/                  # Reference code (not modified)
│   ├── interactive-stand-game/
│   └── [UltraSinger components]
├── venv/                      # Virtual environment (Python 3.13, Kivy 2.3.1)
├── main.py                    # Entry point (Windows 11, no GPIO)
├── requirements.txt           # kivy>=2.3.0
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

## 🔄 Próximos Passos (Fase 1 - Componentes de Karaoke)

### 1. UltraStar Integration
- [ ] Integrar parser de arquivos `.txt` UltraStar (ref_code/ultrastar_parser.py)
- [ ] Carregar metadados (artista, título, BPM, GAP)
- [ ] Parsear notas e letras sincronizadas

### 2. Audio Pipeline
- [ ] Implementar pitch detection com Aubio
- [ ] Configurar input de microfone
- [ ] Implementar output de áudio (música + backing track)
- [ ] Sincronização áudio-vídeo

### 3. Video Background
- [ ] Adicionar player de vídeo (ffpyplayer ou similar)
- [ ] Sincronizar vídeo com áudio (VIDEOGAP)
- [ ] Fallback para imagem estática se sem vídeo

### 4. Karaoke Gameplay
- [ ] Criar KaraokeGameScreen
- [ ] Exibir letras sincronizadas (scrolling horizontal)
- [ ] Barra de pitch visual (esperado vs cantado)
- [ ] Sistema de pontuação em tempo real
- [ ] Feedback visual (acertos/erros)

### 5. Score & Ranking
- [ ] Integrar UltraStar score calculator (ref_code/ultrastar_score_calculator.py)
- [ ] Calcular golden notes, line bonus
- [ ] Salvar score no ranking com timestamp
- [ ] Exibir leaderboard do dia

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

### Bibliotecas Principais (a adicionar)
- `aubio` - Pitch detection em tempo real
- `ffpyplayer` - Reprodução de vídeo/áudio
- `numpy` - Processamento de arrays de áudio
- `librosa` - Análise de áudio (BPM, onset detection)

## 🎤 Próximo Marco

**Fase 1 completa quando:**
- [ ] Conseguir tocar uma música UltraStar completa
- [ ] Microfone detecta pitch em tempo real
- [ ] Letras aparecem sincronizadas
- [ ] Vídeo background funciona
- [ ] Score calculado corretamente

---

**Data de conclusão Fase 0:** 2025-10-26  
**Status:** ✅ COMPLETO - Pronto para Fase 1