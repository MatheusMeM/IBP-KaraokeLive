# RooCode Task: Karaoke Scoring & Leaderboard System Implementation

## 🎯 Objective
Analyze the IBP-KaraokeLive codebase and design a comprehensive scoring system with functional daily leaderboard, following PEP 8 and Separation of Concerns principles. **UPDATED:** Incorporating real-time FFT-based audio analysis for vocal performance measurement using PyAudio.

## ✅ CONFIRMED DECISIONS

Based on user feedback (2025-10-26):

1. **Storage Backend:** JSON (keep existing [`data/leaderboard.json`](data/leaderboard.json))
2. **Historical Data:** Keep ALL entries permanently, filter by date for display only
3. **Leaderboard Modes:** Single leaderboard for PERFORMANCE mode only (no rehearsal scoring)
4. **Score Display:** Show ONLY final score (e.g., "87/100") - no detailed breakdown
5. **Profanity Filter:** NOT needed

These decisions simplify implementation and maintain existing architecture.

---

## 🔍 Phase 1: Codebase Analysis & Discrepancy Report

### 1.1 Current Architecture Map

**Existing Components:**
```
IBP-KaraokeLive/
├── main.py                           # Entry point, screen registration
├── config/
│   └── app_config.py                 # Configuration constants
├── modules/
│   ├── audio_router.py               # Dual-track audio routing (speakers/headphones)
│   ├── audio_player.py               # Audio playback wrapper
│   └── lyric_display.py              # Lyric synchronization with timestamps
├── ui/
│   ├── app_manager.py                # Screen flow orchestration
│   └── screens/
│       ├── welcome_screen.py
│       ├── instructions_screen.py
│       ├── countdown_screen.py
│       ├── rehearsal_screen.py       # Rehearsal with vocals (headphones only)
│       ├── cta_screen.py             # Call-to-action between modes
│       ├── performance_screen.py     # Performance mode (speakers + headphones)
│       ├── congratulations_screen.py # End screen
│       └── leaderboard_screen.py     # Display leaderboard
├── data/
│   ├── ranking_manager.py            # Leaderboard persistence
│   └── leaderboard.json              # JSON storage (current)
└── tests/
    ├── test_audio_routing.py
    └── test_core_modules.py
```

**Current Screen Flow:**
```
welcome → instructions → countdown → rehearsal → cta → 
performance → congratulations → (back to welcome)
```

**Missing Components (Required for Scoring):**
- ❌ Real-time microphone capture module
- ❌ FFT-based vocal analysis module  
- ❌ Performance metrics tracker
- ❌ Score calculator with weighted metrics
- ❌ Score entry screen (with virtual keyboard)
- ❌ Daily reset scheduler

---

### 1.2 Critical Discrepancies Found

#### **DISCREPANCY #1: Inconsistent Data Access**
**Location:** [`ui/screens/leaderboard_screen.py:30`](ui/screens/leaderboard_screen.py:30)

**Issue:**
```python
# leaderboard_screen.py line 30 - BYPASSES RankingManager
with open('data/leaderboard.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

**Expected:**
```python
# Should use RankingManager for consistency
from data.ranking_manager import RankingManager
self.ranking = RankingManager()
data = self.ranking.load_leaderboard()
```

**Impact:** Violates Separation of Concerns, creates duplicate data access logic

---

#### **DISCREPANCY #2: Missing Scoring Integration**
**Location:** [`ui/screens/performance_screen.py:231`](ui/screens/performance_screen.py:231)

**Current Flow:**
```python
def finish_performance(self):
    """Finalizar e ir para congratulations."""
    # ... cleanup code ...
    self.manager.current = 'congratulations'  # ❌ NO SCORING STEP
```

**Expected Flow with FFT Scoring:**
```python
def finish_performance(self):
    """Finalizar, calcular score, e ir para score entry."""
    # Stop real-time audio analysis
    self.audio_analyzer.stop_recording()
    
    # Get collected performance metrics
    performance_data = self.performance_tracker.get_performance_data()
    
    # Calculate final score from FFT metrics
    score = self.score_calculator.calculate(performance_data)
    
    # Navigate to score entry screen
    score_entry = self.manager.get_screen('score_entry')
    score_entry.set_score(score, mode='performance')
    self.manager.current = 'score_entry'  # ✅ NEW SCREEN
```

**Impact:** No way to collect or calculate scores

---

#### **DISCREPANCY #3: No Microphone Input**
**Location:** Entire codebase

**Current:** No microphone capture or audio analysis
**Required:** Real-time FFT analysis during performance using PyAudio

**New Module Needed:**
```python
# modules/scoring/audio_analyzer.py - NEW FILE
import pyaudio
import numpy as np
from threading import Thread

class AudioAnalyzer:
    """Real-time microphone audio analysis using FFT."""
    
    def __init__(self, chunk_size=1024, sample_rate=44100):
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.metrics = []  # Store real-time metrics
        self.is_recording = False
        
    def start_recording(self):
        """Start microphone capture and FFT analysis."""
        
    def _analyze_chunk(self, audio_data):
        """Compute FFT and extract vocal metrics."""
        # RMS energy, peak frequency, spectral centroid, etc.
```

---

#### **DISCREPANCY #4: RankingManager vs Task Specification**
**Location:** [`data/ranking_manager.py`](data/ranking_manager.py)

**Current Storage:** JSON file-based
**Task Specification:** SQLite database recommended

**Current Schema (JSON):**
```json
{
  "scores": [
    {"name": "PLAYER", "score": 100, "timestamp": "2024-01-01T12:00:00"}
  ]
}
```

**Alternative Schema (SQLite - if migrating):**
```sql
CREATE TABLE leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    performance_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mode TEXT DEFAULT 'performance'
);
```

**RECOMMENDATION:** **Keep JSON for now** (simpler, adequate for single-machine kiosk, already implemented). Migration to SQLite can be future enhancement if needed.

---

#### **DISCREPANCY #5: Missing Daily Reset Mechanism**
**Location:** Entire codebase

**Current:** No automated cleanup mechanism
**Required:** Auto-reset at midnight (00:00)

**Implementation Pattern:**
```python
# modules/leaderboard/daily_reset.py - NEW FILE
from kivy.clock import Clock
from datetime import datetime

class DailyResetScheduler:
    def __init__(self, leaderboard_manager):
        self.manager = leaderboard_manager
        self.last_check_date = datetime.now().date()
        
    def start(self):
        # Check every 60 seconds for date change
        Clock.schedule_interval(self._check_reset, 60)
    
    def _check_reset(self, dt):
        current_date = datetime.now().date()
        if current_date > self.last_check_date:
            print(f"🔄 Daily reset: {self.last_check_date} → {current_date}")
            self.manager.clear_old_entries()
            self.last_check_date = current_date
```

---

### 1.3 Method Call Validation

**Verified Correct Calls:**
- ✅ [`AudioRouter.set_performance_mode()`](modules/audio_router.py) - exists, properly called
- ✅ [`AudioRouter.load_audio()`](modules/audio_router.py) - exists, properly called  
- ✅ [`AudioRouter.play()`](modules/audio_router.py) - exists, properly called
- ✅ [`AudioRouter.get_position()`](modules/audio_router.py) - exists, returns current playback time
- ✅ [`AudioRouter.is_playing()`](modules/audio_router.py) - exists, checks if audio is active
- ✅ [`LyricDisplay.get_context_lines()`](modules/lyric_display.py:98) - exists, returns prev/current/next
- ✅ [`RankingManager.get_today_scores()`](data/ranking_manager.py:126) - exists, filters by date

**Missing Methods (Required for Scoring):**
- ❌ `AudioAnalyzer.start_recording()` - doesn't exist yet
- ❌ `AudioAnalyzer.stop_recording()` - doesn't exist yet
- ❌ `AudioAnalyzer.get_metrics()` - doesn't exist yet
- ❌ `ScoreCalculator.calculate()` - doesn't exist yet
- ❌ `PerformanceTracker.log_timing_event()` - doesn't exist yet
- ❌ `PerformanceTracker.get_performance_data()` - doesn't exist yet
- ❌ `LeaderboardManager.submit_score()` - doesn't exist yet

---

## 📊 Phase 2: Scoring Strategy with Real-Time FFT Analysis

### Strategy: FFT-Based Vocal Metrics (RECOMMENDED)

**Concept:** Use PyAudio + NumPy FFT to capture and analyze microphone input in real-time, computing multiple vocal quality metrics.

**Core Audio Metrics (Based on User's Example):**

1. **RMS Energy** - Overall loudness/vocal strength
   ```python
   rms_energy = np.sqrt(np.mean(audio_data**2))
   ```

2. **Peak Frequency** - Dominant pitch being sung
   ```python
   peak_idx = np.argmax(fft_magnitude)
   peak_freq = fft_freq[peak_idx]
   ```

3. **Spectral Centroid** - Sound brightness/timbre quality
   ```python
   spectral_centroid = np.sum(fft_freq * fft_magnitude) / np.sum(fft_magnitude)
   ```

4. **Peak Magnitude** - Strength of dominant frequency
   ```python
   peak_magnitude = np.max(fft_magnitude)
   ```

**Additional Timing Metrics:**

5. **Timing Accuracy** - How close vocal starts to expected lyric timestamps
6. **Consistency** - Vocal energy consistency throughout performance
7. **Coverage** - Percentage of song actively sung (vs. silent gaps)

---

### Scoring Algorithm Design

**Weighted Composite Score (0-100):**

```python
class ScoreCalculator:
    WEIGHTS = {
        'vocal_strength': 0.25,    # RMS energy consistency
        'pitch_quality': 0.20,      # Peak frequency stability
        'tone_quality': 0.15,       # Spectral centroid consistency
        'timing_accuracy': 0.20,    # Sync with lyric timestamps
        'coverage': 0.15,           # How much of song was sung
        'bonus_streak': 0.05        # Consecutive good chunks
    }
```

**Scoring Breakdown:**

1. **Vocal Strength Score (25%):** 
   - Average RMS energy across performance
   - Higher energy = better score (but cap at realistic maximum)
   - Penalize complete silence

2. **Pitch Quality Score (20%):**
   - Stability of peak frequency (less variation = better)
   - Filter out noise frequencies (< 80 Hz, > 1000 Hz for vocals)

3. **Tone Quality Score (15%):**
   - Spectral centroid consistency
   - Measures vocal timbre quality

4. **Timing Accuracy Score (20%):**
   - Compare RMS energy peaks with expected lyric timestamps
   - Score based on ±1 second window

5. **Coverage Score (15%):**
   - Percentage of song where RMS > silence threshold
   - Penalize long silent gaps

6. **Bonus Streak (5%):**
   - Reward consecutive chunks above quality threshold

---

### Implementation Architecture

```
modules/scoring/
├── __init__.py
├── audio_analyzer.py          # Real-time FFT analysis (PyAudio)
├── performance_tracker.py     # Aggregate metrics over time
├── score_calculator.py        # Weighted scoring algorithm
└── config.py                  # Scoring thresholds/weights

Dataflow:
1. Microphone → AudioAnalyzer (FFT every 1024 samples)
2. FFT metrics → PerformanceTracker (aggregate over time)
3. End of song → ScoreCalculator (compute final score)
4. Score → ScoreEntryScreen → Leaderboard
```

---

## 🏗️ Phase 3: Detailed Technical Specifications

### 3.1 AudioAnalyzer Module

**File:** `modules/scoring/audio_analyzer.py`

```python
"""
Real-time microphone audio analysis using PyAudio and FFT.
Based on minimal FFT example with karaoke-specific enhancements.
"""
import pyaudio
import numpy as np
import time
from threading import Thread, Event
from typing import List, Dict, Optional
from collections import deque


class AudioAnalyzer:
    """
    Captures microphone audio and computes real-time FFT metrics.
    
    Runs in background thread to avoid blocking Kivy UI.
    """
    
    # Audio configuration
    CHUNK = 1024              # Samples per frame
    FORMAT = pyaudio.paInt16  # 16-bit audio
    CHANNELS = 1              # Mono
    RATE = 44100              # Sampling rate (Hz)
    
    # Vocal frequency range for karaoke (Hz)
    MIN_VOCAL_FREQ = 80       # Below this = noise
    MAX_VOCAL_FREQ = 1000     # Above this = harmonics/noise
    
    # Silence threshold
    SILENCE_RMS_THRESHOLD = 500  # Below this = considered silent
    
    def __init__(self):
        """Initialize audio analyzer."""
        self.p = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.metrics_buffer = deque(maxlen=10000)  # Store last ~3min of data
        self.is_recording = False
        self.stop_event = Event()
        self.thread: Optional[Thread] = None
        
    def start_recording(self) -> None:
        """Start microphone capture and FFT analysis in background thread."""
        if self.is_recording:
            print("⚠️ Already recording")
            return
            
        print("🎤 Starting microphone capture...")
        
        # Open audio stream
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        self.is_recording = True
        self.stop_event.clear()
        
        # Start background analysis thread
        self.thread = Thread(target=self._record_loop, daemon=True)
        self.thread.start()
        
    def stop_recording(self) -> None:
        """Stop microphone capture and close stream."""
        if not self.is_recording:
            return
            
        print("🛑 Stopping microphone capture...")
        
        self.is_recording = False
        self.stop_event.set()
        
        if self.thread:
            self.thread.join(timeout=2.0)
            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
    def _record_loop(self) -> None:
        """Background thread: continuously capture and analyze audio."""
        while self.is_recording and not self.stop_event.is_set():
            try:
                # Capture audio chunk
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Compute FFT
                fft_data = np.fft.rfft(audio_data)
                fft_magnitude = np.abs(fft_data)
                fft_freq = np.fft.rfftfreq(self.CHUNK, 1.0 / self.RATE)
                
                # Filter to vocal range
                vocal_mask = (fft_freq >= self.MIN_VOCAL_FREQ) & (fft_freq <= self.MAX_VOCAL_FREQ)
                vocal_fft_magnitude = fft_magnitude[vocal_mask]
                vocal_fft_freq = fft_freq[vocal_mask]
                
                # Compute metrics
                timestamp = time.time()
                
                # 1. RMS Energy (loudness)
                rms_energy = float(np.sqrt(np.mean(audio_data**2)))
                
                # 2. Peak Frequency (pitch) - only in vocal range
                if len(vocal_fft_magnitude) > 0:
                    peak_idx = np.argmax(vocal_fft_magnitude)
                    peak_freq = float(vocal_fft_freq[peak_idx])
                    peak_magnitude = float(vocal_fft_magnitude[peak_idx])
                else:
                    peak_freq = 0.0
                    peak_magnitude = 0.0
                
                # 3. Spectral Centroid (brightness) - vocal range only
                if len(vocal_fft_magnitude) > 0 and np.sum(vocal_fft_magnitude) > 0:
                    spectral_centroid = float(
                        np.sum(vocal_fft_freq * vocal_fft_magnitude) / np.sum(vocal_fft_magnitude)
                    )
                else:
                    spectral_centroid = 0.0
                
                # 4. Is singing? (above silence threshold)
                is_singing = rms_energy > self.SILENCE_RMS_THRESHOLD
                
                # Store metrics
                metric_record = {
                    'timestamp': timestamp,
                    'rms_energy': rms_energy,
                    'peak_freq': peak_freq,
                    'spectral_centroid': spectral_centroid,
                    'peak_magnitude': peak_magnitude,
                    'is_singing': is_singing
                }
                
                self.metrics_buffer.append(metric_record)
                
            except Exception as e:
                print(f"❌ Audio analysis error: {e}")
                
    def get_metrics(self) -> List[Dict]:
        """
        Get all collected metrics.
        
        Returns:
            List of metric dictionaries with timestamp and audio features
        """
        return list(self.metrics_buffer)
    
    def clear_metrics(self) -> None:
        """Clear collected metrics (call before new performance)."""
        self.metrics_buffer.clear()
        
    def cleanup(self) -> None:
        """Clean up PyAudio resources."""
        self.stop_recording()
        self.p.terminate()
```

---

### 3.2 PerformanceTracker Module

**File:** `modules/scoring/performance_tracker.py`

```python
"""
Performance tracking: aggregates audio metrics + timing events.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class PerformanceData:
    """Container for complete performance metrics."""
    
    # Timing info
    start_time: float
    end_time: float
    total_duration: float
    completed: bool
    
    # Audio metrics (from FFT analysis)
    audio_metrics: List[Dict] = field(default_factory=list)
    
    # Lyric timing events
    lyric_events: List[Dict] = field(default_factory=list)
    
    # Aggregate statistics (computed from audio_metrics)
    avg_rms_energy: float = 0.0
    avg_peak_freq: float = 0.0
    avg_spectral_centroid: float = 0.0
    singing_time: float = 0.0  # Seconds spent actively singing
    coverage_percentage: float = 0.0  # % of song sung vs. silent


class PerformanceTracker:
    """
    Tracks complete performance: audio metrics + timing events.
    
    Combines data from AudioAnalyzer and LyricDisplay timing.
    """
    
    def __init__(self):
        """Initialize empty tracker."""
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.completed = False
        self.lyric_events: List[Dict] = []
        
    def start(self) -> None:
        """Mark performance start."""
        self.start_time = datetime.now().timestamp()
        self.completed = False
        self.lyric_events = []
        print(f"📊 Performance tracking started at {self.start_time}")
        
    def log_lyric_event(self, expected_time: float, actual_time: float, 
                       line_text: str) -> None:
        """
        Log when a lyric line appeared vs. when expected.
        
        Used to measure timing accuracy.
        
        Args:
            expected_time: When line should start (from lyrics file)
            actual_time: Current playback time when detected
            line_text: The lyric line text
        """
        event = {
            'expected': expected_time,
            'actual': actual_time,
            'line': line_text,
            'timing_offset': actual_time - expected_time
        }
        self.lyric_events.append(event)
        
    def mark_complete(self) -> None:
        """Mark performance as fully completed (not skipped)."""
        self.completed = True
        self.end_time = datetime.now().timestamp()
        print(f"✅ Performance marked complete at {self.end_time}")
        
    def get_performance_data(self, audio_metrics: List[Dict]) -> PerformanceData:
        """
        Combine all data into PerformanceData object.
        
        Args:
            audio_metrics: FFT metrics from AudioAnalyzer.get_metrics()
            
        Returns:
            Complete performance data for scoring
        """
        if not self.start_time:
            raise ValueError("Performance not started")
            
        end = self.end_time or datetime.now().timestamp()
        duration = end - self.start_time
        
        # Compute aggregate statistics from audio metrics
        if audio_metrics:
            avg_rms = sum(m['rms_energy'] for m in audio_metrics) / len(audio_metrics)
            avg_freq = sum(m['peak_freq'] for m in audio_metrics) / len(audio_metrics)
            avg_centroid = sum(m['spectral_centroid'] for m in audio_metrics) / len(audio_metrics)
            
            # Count chunks where actively singing
            singing_chunks = sum(1 for m in audio_metrics if m['is_singing'])
            # Each chunk is ~0.023 seconds (1024 / 44100)
            chunk_duration = 1024 / 44100
            singing_time = singing_chunks * chunk_duration
            coverage = (singing_time / duration * 100) if duration > 0 else 0.0
        else:
            avg_rms = 0.0
            avg_freq = 0.0
            avg_centroid = 0.0
            singing_time = 0.0
            coverage = 0.0
        
        return PerformanceData(
            start_time=self.start_time,
            end_time=end,
            total_duration=duration,
            completed=self.completed,
            audio_metrics=audio_metrics,
            lyric_events=self.lyric_events,
            avg_rms_energy=avg_rms,
            avg_peak_freq=avg_freq,
            avg_spectral_centroid=avg_centroid,
            singing_time=singing_time,
            coverage_percentage=coverage
        )
    
    def reset(self) -> None:
        """Clear all logged events."""
        self.start_time = None
        self.end_time = None
        self.completed = False
        self.lyric_events = []
```

---

### 3.3 ScoreCalculator Module

**File:** `modules/scoring/score_calculator.py`

```python
"""
Score calculation using weighted multi-factor algorithm.
"""
import json
from pathlib import Path
from typing import Dict
import numpy as np

from modules.scoring.performance_tracker import PerformanceData


class ScoreCalculator:
    """
    Calculate karaoke performance score using weighted metrics.
    
    Combines:
    - FFT audio metrics (RMS, pitch, tone)
    - Timing accuracy (vs. lyric timestamps)
    - Coverage (how much was sung)
    """
    
    # Default weights if config file not found
    DEFAULT_WEIGHTS = {
        'vocal_strength': 0.25,    # RMS energy consistency
        'pitch_quality': 0.20,      # Peak frequency stability
        'tone_quality': 0.15,       # Spectral centroid quality
        'timing_accuracy': 0.20,    # Sync with lyrics
        'coverage': 0.15,           # How much sung
        'bonus_streak': 0.05        # Consecutive good chunks
    }
    
    # Thresholds
    GOOD_RMS_MIN = 1000           # Minimum RMS for "good" singing
    GOOD_RMS_MAX = 15000          # Maximum RMS (cap)
    TIMING_WINDOW_GOOD = 0.5      # ±0.5s = good timing
    TIMING_WINDOW_OK = 1.5        # ±1.5s = acceptable
    MIN_COVERAGE = 50.0           # Minimum coverage % to not penalize heavily
    
    def __init__(self, config_path: str = 'data/scoring_config.json'):
        """
        Initialize score calculator.
        
        Args:
            config_path: Path to JSON config with weights/thresholds
        """
        self.weights = self.DEFAULT_WEIGHTS.copy()
        self._load_config(config_path)
        
    def _load_config(self, config_path: str) -> None:
        """Load scoring weights from config file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                if 'weights' in config:
                    self.weights.update(config['weights'])
                print(f"✅ Loaded scoring config from {config_path}")
        except FileNotFoundError:
            print(f"⚠️ Config not found, using defaults: {config_path}")
        except json.JSONDecodeError as e:
            print(f"⚠️ Invalid config JSON, using defaults: {e}")
    
    def calculate(self, performance_data: PerformanceData) -> int:
        """
        Calculate final score (0-100).
        
        Args:
            performance_data: Complete performance metrics
            
        Returns:
            Score from 0-100
        """
        if not performance_data.completed:
            # Incomplete performance gets heavily penalized
            return int(self._score_coverage(performance_data) * 50)
        
        scores = {
            'vocal_strength': self._score_vocal_strength(performance_data),
            'pitch_quality': self._score_pitch_quality(performance_data),
            'tone_quality': self._score_tone_quality(performance_data),
            'timing_accuracy': self._score_timing_accuracy(performance_data),
            'coverage': self._score_coverage(performance_data),
            'bonus_streak': self._score_bonus_streak(performance_data)
        }
        
        # Weighted sum
        weighted_sum = sum(
            scores[key] * self.weights[key] 
            for key in self.weights
        )
        
        final_score = int(weighted_sum * 100)
        
        # Clamp to 0-100
        return max(0, min(100, final_score))
    
    def _score_vocal_strength(self, data: PerformanceData) -> float:
        """
        Score based on RMS energy (0.0-1.0).
        
        Rewards consistent vocal strength.
        """
        if not data.audio_metrics:
            return 0.0
        
        # Get RMS values
        rms_values = [m['rms_energy'] for m in data.audio_metrics if m['is_singing']]
        
        if not rms_values:
            return 0.0
        
        avg_rms = np.mean(rms_values)
        
        # Normalize to 0-1 scale
        if avg_rms < self.GOOD_RMS_MIN:
            # Too quiet
            score = avg_rms / self.GOOD_RMS_MIN * 0.5
        elif avg_rms > self.GOOD_RMS_MAX:
            # Cap at maximum
            score = 1.0
        else:
            # Good range
            normalized = (avg_rms - self.GOOD_RMS_MIN) / (self.GOOD_RMS_MAX - self.GOOD_RMS_MIN)
            score = 0.5 + normalized * 0.5
        
        return min(1.0, score)
    
    def _score_pitch_quality(self, data: PerformanceData) -> float:
        """
        Score based on pitch stability (0.0-1.0).
        
        Less variation in peak frequency = better.
        """
        if not data.audio_metrics:
            return 0.0
        
        # Get peak frequencies during singing
        freqs = [m['peak_freq'] for m in data.audio_metrics if m['is_singing'] and m['peak_freq'] > 0]
        
        if len(freqs) < 10:
            # Not enough data
            return 0.5
        
        # Calculate coefficient of variation (CV)
        std = np.std(freqs)
        mean = np.mean(freqs)
        
        if mean == 0:
            return 0.0
        
        cv = std / mean
        
        # Lower CV = better (more stable pitch)
        # Typical good CV < 0.2, poor CV > 0.5
        if cv < 0.2:
            score = 1.0
        elif cv > 0.5:
            score = 0.3
        else:
            score = 1.0 - ((cv - 0.2) / 0.3) * 0.7
        
        return score
    
    def _score_tone_quality(self, data: PerformanceData) -> float:
        """
        Score based on spectral centroid consistency (0.0-1.0).
        
        Measures vocal timbre quality.
        """
        if not data.audio_metrics:
            return 0.0
        
        centroids = [m['spectral_centroid'] for m in data.audio_metrics if m['is_singing']]
        
        if len(centroids) < 10:
            return 0.5
        
        # Consistent centroid = better tone
        std = np.std(centroids)
        mean = np.mean(centroids)
        
        if mean == 0:
            return 0.0
        
        cv = std / mean
        
        # Similar to pitch: lower CV = better
        if cv < 0.15:
            score = 1.0
        elif cv > 0.4:
            score = 0.4
        else:
            score = 1.0 - ((cv - 0.15) / 0.25) * 0.6
        
        return score
    
    def _score_timing_accuracy(self, data: PerformanceData) -> float:
        """
        Score based on timing sync with lyrics (0.0-1.0).
        
        Compares when lyrics appeared vs. expected timestamps.
        """
        if not data.lyric_events:
            return 0.5  # Neutral if no timing data
        
        good_timing = 0
        ok_timing = 0
        
        for event in data.lyric_events:
            offset = abs(event['timing_offset'])
            
            if offset <= self.TIMING_WINDOW_GOOD:
                good_timing += 1
            elif offset <= self.TIMING_WINDOW_OK:
                ok_timing += 1
        
        total = len(data.lyric_events)
        
        # Score: good = 1.0, ok = 0.5, bad = 0.0
        score = (good_timing + ok_timing * 0.5) / total
        
        return score
    
    def _score_coverage(self, data: PerformanceData) -> float:
        """
        Score based on how much of song was sung (0.0-1.0).
        
        Penalizes long silent gaps.
        """
        coverage = data.coverage_percentage
        
        if coverage < 30.0:
            # Very low coverage
            score = coverage / 30.0 * 0.3
        elif coverage < self.MIN_COVERAGE:
            # Below minimum
            score = 0.3 + (coverage - 30.0) / (self.MIN_COVERAGE - 30.0) * 0.3
        else:
            # Good coverage
            score = 0.6 + (coverage - self.MIN_COVERAGE) / (100.0 - self.MIN_COVERAGE) * 0.4
        
        return min(1.0, score)
    
    def _score_bonus_streak(self, data: PerformanceData) -> float:
        """
        Bonus for consecutive chunks of good singing (0.0-1.0).
        
        Rewards sustained performance.
        """
        if not data.audio_metrics:
            return 0.0
        
        # Define "good" chunk: singing + decent RMS
        good_chunks = [
            m['is_singing'] and m['rms_energy'] >= self.GOOD_RMS_MIN
            for m in data.audio_metrics
        ]
        
        # Find longest streak
        max_streak = 0
        current_streak = 0
        
        for is_good in good_chunks:
            if is_good:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        # Score based on longest streak
        # 50 chunks = ~1.2 seconds, 200 chunks = ~4.6 seconds
        if max_streak < 50:
            score = max_streak / 50 * 0.5
        elif max_streak < 200:
            score = 0.5 + (max_streak - 50) / 150 * 0.5
        else:
            score = 1.0
        
        return score
```

---

### 3.4 Scoring Configuration

**File:** `data/scoring_config.json`

```json
{
  "weights": {
    "vocal_strength": 0.25,
    "pitch_quality": 0.20,
    "tone_quality": 0.15,
    "timing_accuracy": 0.20,
    "coverage": 0.15,
    "bonus_streak": 0.05
  },
  "thresholds": {
    "good_rms_min": 1000,
    "good_rms_max": 15000,
    "timing_window_good": 0.5,
    "timing_window_ok": 1.5,
    "min_coverage": 50.0,
    "silence_rms_threshold": 500
  },
  "vocal_range": {
    "min_freq_hz": 80,
    "max_freq_hz": 1000
  },
  "audio_config": {
    "chunk_size": 1024,
    "sample_rate": 44100,
    "format": "paInt16",
    "channels": 1
  }
}
```

---

## 📋 Phase 4: Implementation Plan (Week-by-Week)

### WEEK 1: Audio Analysis Foundation

**Task 1.1: Set up PyAudio Environment** (1 hour)
- [ ] Add `pyaudio` and `numpy` to [`requirements.txt`](requirements.txt)
- [ ] Test microphone access on Windows 11
- [ ] Create test script to verify FFT works

**Task 1.2: Create AudioAnalyzer Module** (4-5 hours)
- [ ] Create [`modules/scoring/audio_analyzer.py`](modules/scoring/audio_analyzer.py)
- [ ] Implement real-time FFT analysis in background thread
- [ ] Test with manual recording (save metrics to CSV)
- [ ] Verify vocal frequency filtering works

**Task 1.3: Create PerformanceTracker Module** (2-3 hours)
- [ ] Create [`modules/scoring/performance_tracker.py`](modules/scoring/performance_tracker.py)
- [ ] Implement timing event logging
- [ ] Implement aggregate statistics calculation
- [ ] Write unit tests

**Task 1.4: Create ScoreCalculator Module** (3-4 hours)
- [ ] Create [`modules/scoring/score_calculator.py`](modules/scoring/score_calculator.py)
- [ ] Implement all scoring methods
- [ ] Create [`data/scoring_config.json`](data/scoring_config.json)
- [ ] Write unit tests with mock data

---

### WEEK 2: Integration with Performance Screens

**Task 2.1: Integrate AudioAnalyzer into Performance Screen** (3-4 hours)
- [ ] Modify [`ui/screens/performance_screen.py`](ui/screens/performance_screen.py)
  - Add `self.audio_analyzer = AudioAnalyzer()` in `__init__()`
  - Call `self.audio_analyzer.start_recording()` in `on_enter()`
  - Call `self.audio_analyzer.stop_recording()` in `finish_performance()`
  - Get metrics and calculate score before navigating away

**Integration Code:**
```python
# In performance_screen.py
from modules.scoring.audio_analyzer import AudioAnalyzer
from modules.scoring.performance_tracker import PerformanceTracker
from modules.scoring.score_calculator import ScoreCalculator

class PerformanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ... existing code ...
        
        # NEW: Scoring components
        self.audio_analyzer = AudioAnalyzer()
        self.performance_tracker = PerformanceTracker()
        self.score_calculator = ScoreCalculator()
    
    def on_enter(self):
        # ... existing code ...
        
        # NEW: Start tracking and audio analysis
        self.performance_tracker.start()
        self.audio_analyzer.clear_metrics()
        self.audio_analyzer.start_recording()
    
    def update(self, dt):
        # ... existing code ...
        
        # NEW: Log timing events
        new_current = lines['current'] or ''
        line_changed = new_current != self.last_current_text and new_current != ''
        
        if line_changed and new_current:
            expected_time = self.lyric_display.lines[self.lyric_display.current_index].start
            self.performance_tracker.log_lyric_event(
                expected_time, current_time, new_current
            )
    
    def finish_performance(self):
        # Stop audio analysis
        self.audio_analyzer.stop_recording()
        
        # Get metrics
        audio_metrics = self.audio_analyzer.get_metrics()
        
        # Mark as complete
        self.performance_tracker.mark_complete()
        
        # Get performance data
        performance_data = self.performance_tracker.get_performance_data(audio_metrics)
        
        # Calculate score
        score = self.score_calculator.calculate(performance_data)
        
        print(f"🎯 Final Score: {score}/100")
        
        # Navigate to score entry (to be created)
        score_entry = self.manager.get_screen('score_entry')
        score_entry.set_score(score, mode='performance')
        self.manager.current = 'score_entry'
```

**Task 2.2: Same Integration for Rehearsal Screen** (1-2 hours)
- [ ] Apply same changes to [`ui/screens/rehearsal_screen.py`](ui/screens/rehearsal_screen.py)
- [ ] Set mode='rehearsal' when submitting score

**Task 2.3: Test End-to-End Audio Scoring** (2-3 hours)
- [ ] Run full performance with singing
- [ ] Verify metrics are collected
- [ ] Verify score calculation produces reasonable results (40-100 range)
- [ ] Test with different vocal intensities

---

### WEEK 3: UI Components (Keyboard & Score Entry)

**Task 3.1: Create Virtual Keyboard Widget** (4-5 hours)
- [ ] Create [`modules/input/virtual_keyboard.py`](modules/input/virtual_keyboard.py)
- [ ] Implement QWERTY layout with touch targets
- [ ] Add uppercase/lowercase toggle
- [ ] Add numbers/symbols mode (123)
- [ ] Add backspace and space keys
- [ ] Style to match IBP branding colors
- [ ] Character limit enforcement (3-16)

**Layout:**
```
┌──────────────────────────────┐
│ Q  W  E  R  T  Y  U  I  O  P │
│  A  S  D  F  G  H  J  K  L   │
│ ⇧  Z  X  C  V  B  N  M  ⌫   │
│ 123   [  SPACE  ]      OK    │
└──────────────────────────────┘
```

**Task 3.2: Create Score Entry Screen** (3-4 hours)
- [ ] Create [`ui/screens/score_entry_screen.py`](ui/screens/score_entry_screen.py)
- [ ] Create corresponding `.kv` layout
- [ ] Display score prominently
- [ ] Show star rating (★★★★★ based on score)
- [ ] Integrate VirtualKeyboard
- [ ] Validate name before submit
- [ ] Call LeaderboardManager on submit

**Layout:**
```
┌─────────────────────────────────┐
│       YOUR SCORE: 87            │
│      ★ ★ ★ ★ ☆                  │
│                                 │
│   [___________________]         │
│   Enter Your Name (3-16 chars)  │
│                                 │
│  ┌──────────────────────┐       │
│  │  Virtual Keyboard    │       │
│  └──────────────────────┘       │
│                                 │
│         [SUBMIT SCORE]          │
└─────────────────────────────────┘
```

**Task 3.3: Create Leaderboard Manager** (2-3 hours)
- [ ] Create [`modules/leaderboard/manager.py`](modules/leaderboard/manager.py)
- [ ] Wrap [`RankingManager`](data/ranking_manager.py) with high-level API
- [ ] Implement `submit_score()` returning metadata
- [ ] Calculate rank and check if top 10
- [ ] Write unit tests

---

### WEEK 4: Leaderboard Display & Daily Reset

**Task 4.1: Fix Leaderboard Screen** (2-3 hours)
- [ ] Modify [`ui/screens/leaderboard_screen.py`](ui/screens/leaderboard_screen.py)
- [ ] Fix DISCREPANCY #1: Use RankingManager instead of direct JSON access
- [ ] Add entry highlighting (for new player)
- [ ] Add rank badges (🥇🥈🥉 for top 3)
- [ ] Implement score-to-stars conversion
- [ ] Add "Play Again" and "Main Menu" buttons

**Task 4.2: Implement Daily Reset** (2-3 hours)
- [ ] Create [`modules/leaderboard/daily_reset.py`](modules/leaderboard/daily_reset.py)
- [ ] Implement `DailyResetScheduler` class
- [ ] Integrate into [`main.py`](main.py:98) lifecycle
- [ ] Test with mocked system time

**Task 4.3: Update Screen Flow** (1-2 hours)
- [ ] Add ScoreEntryScreen to [`main.py`](main.py:56)
- [ ] Update flow: performance → score_entry → leaderboard → congratulations
- [ ] Update [`app_manager.py`](ui/app_manager.py) if needed

**Task 4.4: Polish & Testing** (4-5 hours)
- [ ] Add animations: score reveal, leaderboard slide-in
- [ ] Add celebration effects for top 10
- [ ] Run PEP 8 linter (`flake8`)
- [ ] Add missing docstrings and type hints
- [ ] End-to-end testing: full flow multiple times
- [ ] Test edge cases: skip, incomplete, ties

---

## ✅ Phase 5: Acceptance Criteria

### Functional Requirements

- [ ] **Audio Scoring Works:**
  - [ ] Microphone captures audio during performance
  - [ ] FFT analysis runs in background without lag
  - [ ] Score 0-100 generated based on vocal metrics
  - [ ] Score correlates with singing quality (loud/consistent = higher)

- [ ] **Leaderboard Functions:**
  - [ ] Top 10 players displayed after score entry
  - [ ] Ranks calculated correctly
  - [ ] Ties handled (same score sorted by timestamp)
  - [ ] Only today's scores shown

- [ ] **Virtual Keyboard Works:**
  - [ ] All keys functional
  - [ ] Name length enforced (3-16 chars)
  - [ ] Submit navigates to leaderboard
  - [ ] Visual feedback on key press

- [ ] **Daily Reset Works:**
  - [ ] Leaderboard clears at midnight automatically
  - [ ] No manual intervention needed
  - [ ] Reset confirmed visually (empty board next day)

### Technical Requirements

- [ ] **Code Quality:**
  - [ ] PEP 8 compliant (`flake8` passes)
  - [ ] All public APIs documented (Google-style)
  - [ ] Unit test coverage >70%
  - [ ] Type hints on all functions

- [ ] **Performance:**
  - [ ] UI stays at 60 FPS during audio analysis
  - [ ] No audio crackling or dropouts
  - [ ] Background thread doesn't block Kivy

- [ ] **Architecture:**
  - [ ] Separation of Concerns maintained
  - [ ] Consistent data access (use RankingManager)
  - [ ] Proper error handling (mic not available, etc.)

---

## 🎯 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Implementation time | 3-4 weeks | Track actual hours per task |
| Audio latency | <50ms | Test microphone → metric recording delay |
| Score range | 40-100 | Most performances should be 40-100 range |
| PEP 8 compliance | 100% | `flake8 . --count` |
| Test coverage | ≥70% | `pytest --cov=modules/scoring` |
| System stability | Zero crashes | 1 week continuous testing |
| Frame rate | 60 FPS | Monitor during performance |

---

## 📞 Questions for Clarification

1. **Microphone Selection:**
   - Use system default mic or allow selection?
   - Current plan: Use PyAudio default input device

2. **Storage Backend:**
   - **RECOMMENDED:** Keep JSON (simpler, already working)
   - Alternative: Migrate to SQLite (more robust, overkill for single-machine kiosk)
   - **Decision?**

3. **Historical Data:**
   - Keep old leaderboards in archive?
   - Or purge completely after daily reset?

4. **Multiple Modes:**
   - Separate leaderboards for rehearsal vs. performance?
   - Or combined leaderboard?

5. **Score Display:**
   - Show detailed breakdown (vocal strength: 85%, timing: 90%, etc.)?
   - Or just final score?

6. **Profanity Filter:**
   - Needed for player names?
   - If yes, which library/approach?

---

## 🔧 Installation Requirements

**Updated [`requirements.txt`](requirements.txt):**
```txt
# Existing dependencies
kivy==2.3.0
pygame==2.5.2
sounddevice==0.4.7

# NEW: Audio analysis
pyaudio==0.2.14
numpy==1.26.4

# Testing
pytest==8.0.0
pytest-cov==4.1.0
flake8==7.0.0
```

**Windows Installation Notes:**
- PyAudio may require Visual C++ Build Tools
- Alternative: Download precompiled wheel from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

---

## 📄 Summary

This master plan provides:

1. ✅ **Complete codebase analysis** with identified discrepancies
2. ✅ **FFT-based audio scoring** using PyAudio (practical approach)
3. ✅ **Detailed module specifications** with full code examples
4. ✅ **Week-by-week implementation plan** with clear tasks
5. ✅ **Integration points** showing exactly where to modify existing code
6. ✅ **Acceptance criteria** and success metrics

**Next Steps:**
1. Confirm scoring strategy and storage backend choice
2. Answer clarification questions
3. Begin Week 1 implementation (audio analysis modules)
4. Iterate based on testing feedback

---

**END OF MASTER PLAN**