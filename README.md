# IBP Karaoke Live

Professional karaoke scoring system for live marketing activations, engineered for Windows 11 kiosk deployments with real-time audio processing and interactive touchscreen interfaces.

## Architecture Overview

The system employs a modular architecture with clear separation of concerns across four primary domains:

- **Core Application**: Kivy-based window management and configuration
- **Audio Processing**: Real-time audio routing, playback, and analysis
- **User Interface**: Screen navigation and interaction handling
- **Data Management**: Persistent storage and configuration handling

## System Requirements

### Platform Dependencies
- Windows 11 (primary target)
- Python 3.13+
- DirectX-compatible audio hardware
- Multi-channel audio output capability

### Core Dependencies
```
kivy>=2.3.0
sounddevice>=0.5.3
soundfile>=0.13.1
numpy>=2.3.4
pyaudio>=0.2.14
ffpyplayer>=4.5.0
pillow>=10.0.0
```

## Configuration Architecture

### Window Configuration (`config/app_config.py`)
The application operates in horizontal kiosk mode optimized for 1920x1080 displays:

```python
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FULLSCREEN = True
BORDERLESS = True  # Eliminates window decorations
```

### Audio Hardware Configuration
Device-specific routing addresses the challenge of simultaneous headphone and speaker output:

- **Device 8**: Speakers (Realtek) - Public/audience output
- **Device 9**: USB Audio Device (headphones) - Singer monitoring

These device IDs are identified during audio routing hardware validation and provide direct hardware access through sounddevice.

### Brand Configuration
IBP visual identity implementation through color palette constants:
```python
COLOR_PRIMARY_BLUE = (0/255, 64/255, 119/255, 1)    # #004077
COLOR_PRIMARY_GREEN = (134/255, 188/255, 37/255, 1) # #86BC25
```

## Core Application Layer

### Entry Point (`main.py`)
The application initializes Kivy with hardware-specific configuration before UI load:

- Window properties set before Kivy imports (critical for correct initialization)
- Virtual keyboard configuration for touchscreen support
- Global keyboard shortcuts for development and emergency controls
- Screen manager with smooth transition effects

### Application Orchestration (`ui/app_manager.py`)
Central coordinator managing screen transitions and application state:

- **Flow Control**: Navigation between screens with state preservation
- **Idle Management**: Automatic timeout handling for kiosk operations
- **Ranking Integration**: Leaderboard display with player highlighting
- **Event Scheduling**: Kivy clock integration for timed transitions

## Audio Processing Subsystem

### Audio Routing (`modules/audio_router.py`)
Hardware-level audio routing with device-specific playback control:

**Core Capabilities:**
- Dual-device simultaneous playback (headphones + speakers)
- Callback-based non-blocking streams for low-latency control
- Thread-safe stop mechanisms preventing audio artifacts
- Mode-specific routing (rehearsal vs performance)

**Technical Implementation:**
```python
def _play_stream(self, device: int, data: np.ndarray, stream_key: str):
    # Callback-based audio streaming with hardware routing
    # Non-blocking approach prevents UI freezes
    # Thread-safe stop control for immediate playback termination
```

**Device Management:**
- Direct hardware access through sounddevice.OutputStream
- Configurable device IDs for hardware-specific routing
- Stream synchronization ensuring precise timing across devices
- Automatic cleanup preventing resource leaks

### Audio Player Interface (`modules/audio_player.py`)
High-level abstraction providing simplified audio control:

- **Interface Uniformity**: Common play/stop/position API
- **Router Integration**: Delegation to AudioRouter for actual playback
- **Duration Calculation**: Sample-accurate audio length determination
- **Mode Management**: Rehearsal/performance mode transitions

### Scoring Analysis (`modules/scoring/audio_analyzer.py`)
Real-time audio analysis for performance evaluation:

**RMS-Based Scoring Algorithm:**
1. **Coverage Calculation**: Percentage of time above silence threshold (500 RMS)
2. **Energy Assessment**: Average RMS level of active segments
3. **Weighted Scoring**: 50% coverage + 50% energy = final score (0-100)

**Technical Implementation:**
```python
def get_score(self):
    # Coverage: Percentage of time above silence threshold
    coverage = (active_chunks / total_chunks * 100)
    
    # Energy: Average RMS of active segments
    avg_rms = np.mean(active_rms_values)
    
    # Weighted combination
    final_score = (coverage/80.0 * 50) + (avg_rms/5000.0 * 50)
```

**Fake Scoring Mode**: For demonstration without microphone input:
- Realistic RMS value simulation (100-2000 base levels)
- Natural noise and trend generation
- "Singing burst" events (2-5x energy spikes)
- Authentic timing simulation (43Hz capture rate)

## User Interface Architecture

### Screen Management (`ui/screens/`)
The system implements ten specialized screens with distinct functionality:

**Navigation Flow:**
```
Welcome → Instructions → Countdown → Rehearsal → CTA → 
Countdown → Performance → ScoreEntry → Congratulations → Welcome
```

**Screen Specifications:**

1. **WelcomeScreen** (`welcome_screen.py`): Entry point with IBP branding
2. **InstructionsScreen** (`instructions_screen.py`): Dynamic content display
3. **CountdownScreen** (`countdown_screen.py`): 3-second preparation timer
4. **RehearsalScreen** (`rehearsal_screen.py`): Practice with headphones only
5. **CTAScreen** (`cta_screen.py`): Transition between rehearsal and performance
6. **PerformanceScreen** (`performance_screen.py`): Full karaoke experience
7. **ScoreEntryScreen** (`score_entry_screen.py`): Name entry with virtual keyboard
8. **CongratulationsScreen** (`congratulations_screen.py`): Completion celebration
9. **LeaderboardScreen** (`leaderboard_screen.py`): Today's top scores display

### Kivy Layout System (`ui/screens/screens.kv`)
Declarative UI definition with IBP visual identity:

**Design Principles:**
- Consistent spacing and typography
- Rounded corners for modern appearance
- Color-coded feedback systems
- Responsive layout for 1920x1080 optimization

**Custom Components:**
- `BrandedButton`: IBP-styled interactive elements
- `VirtualKeyButton`: Touch-optimized input controls
- `BrandedLabel`: Consistent text styling

### Virtual Keyboard Implementation
Custom QWERTY keyboard for kiosk name entry:

- **Layout**: 4-row configuration with Portuguese characters
- **Interaction**: Touch-optimized with visual feedback
- **Validation**: Real-time input length and character restrictions
- **Accessibility**: High contrast and large touch targets

## Data Management System

### Leaderboard Persistence (`data/ranking_manager.py`)
JSON-based storage with atomic write operations:

**Data Structure:**
```json
{
  "scores": [
    {
      "name": "PLAYER_NAME",
      "score": 85.5,
      "timestamp": "2025-10-27T10:30:45"
    }
  ]
}
```

**Storage Management:**
- **Atomic Writes**: Temporary file → rename pattern prevents corruption
- **Date Filtering**: Leaderboard displays only today's scores
- **Backward Compatibility**: Handles legacy data formats
- **Sorted Retrieval**: Automatic ranking by score descending

### Lyric Synchronization (`data/lyrics.json`)
Timestamp-based lyric display with WebVTT-compatible format:

**Synchronization Algorithm:**
```python
def get_context_lines(self, current_time):
    # Sliding window approach for smooth transitions
    # Displays previous, current, and next lines
    # Handles timing gaps and overlaps gracefully
```

**Data Structure:**
```json
{
  "title": "Song Title",
  "duration": 43.979,
  "lines": [
    {
      "start": 4.52,
      "end": 6.752,
      "text": "Lyrical content with timing"
    }
  ]
}
```

## Testing Infrastructure

### Core Module Integration (`tests/test_core_modules.py`)
Comprehensive testing of audio processing pipeline:

**Test Coverage:**
- AudioRouter functionality validation
- SimpleAudioPlayer integration verification
- LyricDisplay synchronization testing
- Full system integration scenarios

### Hardware Audio Routing (`tests/test_audio_routing.py`)
Device-specific testing with verbose logging:

**Validation Areas:**
- Device enumeration and selection
- Simultaneous multi-device playback
- Thread synchronization verification
- Hardware-specific routing confirmation

**Test Results:**
- Device 8 (Speakers): Realtek audio output confirmed
- Device 9 (Headphones): USB audio device validated
- Dual playback: Synchronized timing achieved
- Latency: ~30ms acceptable for karaoke applications

## Performance Characteristics

### Audio Processing Performance
- **Latency**: ~30ms audio delay (acceptable for live karaoke)
- **Sample Rate**: 44.1 kHz standard audio quality
- **Buffer Size**: 2048 frames for stable playback
- **Threading**: Non-blocking streams prevent UI freezes

### Memory Management
- **Audio Data**: Loaded once, cached in memory
- **RMS Values**: Bounded deque (5000 entries, ~2 minutes)
- **Cleanup**: Automatic resource release on screen transitions

### Scalability Considerations
- **Screen Transitions**: O(1) navigation between cached screens
- **Audio Loading**: Single load operation per session
- **Leaderboard**: Efficient sorted retrieval with limited display (15 entries)

## Security Considerations

### Input Validation
- Name entry sanitization (3-20 character limit)
- Audio file path validation
- JSON parsing with error handling
- Thread-safe operation preventing race conditions

### Resource Protection
- Atomic file operations preventing corruption
- Cleanup handlers for audio streams
- Emergency reset button for system recovery
- Exception handling with graceful degradation

## Development Guidelines

### Code Standards
- **PEP 8 Compliance**: Consistent formatting and naming
- **Type Hints**: Explicit parameter and return type declarations
- **Documentation**: Comprehensive docstrings for all public methods
- **Separation of Concerns**: Clear module boundaries and responsibilities

### Testing Strategy
- **Unit Testing**: Individual component validation
- **Integration Testing**: Cross-module functionality verification
- **Hardware Testing**: Real device validation with logging
- **User Flow Testing**: Complete experience validation

## Deployment Architecture

### Production Configuration
```python
FULLSCREEN = True
BORDERLESS = True
DEBUG_MODE = False
```

### File Organization
```
IBP-KaraokeLive/
├── config/              # Application configuration
├── data/               # Persistent data storage
├── modules/            # Core functionality modules
├── ui/                 # User interface components
├── tests/              # Test suite
├── assets/             # Media files (audio, images, video)
└── main.py            # Application entry point
```

### Asset Management
- **Audio Files**: WAV format for lossless quality
- **Images**: PNG format with transparency support
- **Video**: MP4 format for background content
- **Lyrics**: JSON format with millisecond precision

## Troubleshooting Guide

### Common Issues

**Audio Routing Failures:**
1. Verify device IDs in audio routing tests
2. Check Windows sound device priorities
3. Validate sounddevice installation
4. Confirm hardware connectivity

**Performance Degradation:**
1. Monitor CPU usage during audio processing
2. Verify adequate RAM availability
3. Check for audio buffer overruns
4. Validate screen transition cleanup

**UI Responsiveness:**
1. Confirm non-blocking audio operations
2. Verify thread safety in audio callbacks
3. Check for memory leaks in screen transitions
4. Validate virtual keyboard cleanup

### Debug Configuration
Enable verbose logging through test utilities:
```bash
python tests/test_audio_routing.py
python tests/test_core_modules.py
```

## Future Enhancement Opportunities

### Technical Improvements
- **Pitch Detection**: Integration of aubio for note-level analysis
- **Machine Learning**: Pattern recognition for scoring accuracy
- **Network Integration**: Remote leaderboard synchronization
- **Multi-language**: Internationalization support

### Infrastructure Scalability
- **Database Migration**: SQLite for improved query performance
- **Caching Layer**: Redis for high-frequency operations
- **API Framework**: RESTful services for external integration
- **Monitoring**: Application performance monitoring integration

## Conclusion

The IBP Karaoke Live system demonstrates a robust architecture combining real-time audio processing, interactive user interfaces, and reliable data persistence. The modular design enables maintainability while the hardware-specific optimizations ensure consistent performance in production environments. The comprehensive testing infrastructure validates functionality across all system components, providing confidence for live deployment scenarios.