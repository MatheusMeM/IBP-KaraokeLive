# IBP Karaoke Live

Professional karaoke scoring system for live marketing activations.

## Features

- **Real-time Audio Analysis**: RMS-based scoring with configurable thresholds
- **Fake Scoring Mode**: Demo mode with realistic RMS simulation (no microphone required)
- **Multi-output Audio Routing**: Separate headphone and speaker outputs
- **Interactive UI**: Kivy-based fullscreen kiosk interface
- **Lyric Synchronization**: WebVTT format support
- **Leaderboard System**: Persistent ranking storage

## Quick Start

1. **Setup Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Run Application**:
   ```bash
   python main.py
   ```

## Scoring System

The system uses RMS (Root Mean Square) energy analysis to calculate performance scores:

- **Coverage**: Percentage of time above silence threshold (50% of score)
- **Energy**: Average RMS level of active segments (50% of score)
- **Total**: Combined score from 0-100 points

### Fake Scoring Mode

For demo purposes, the system generates realistic fake RMS values:
- Base singing levels: 100-2000 RMS
- Random noise and trends
- Occasional "singing bursts" (2-5x energy)
- Realistic timing (43Hz capture rate)

## Architecture

- **Core**: Game orchestration and state management
- **Audio**: Real-time capture and routing
- **Scoring**: RMS analysis and score calculation
- **UI**: Kivy screens and widgets
- **Data**: Leaderboard and configuration persistence

## Development

- **PEP 8 Compliant**: Clean, readable Python code
- **Modular Design**: Separation of concerns across packages
- **Production Ready**: Tested for live event deployment