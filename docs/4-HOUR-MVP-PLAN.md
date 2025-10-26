# 4-Hour MVP: Karaoke Scoring Implementation

## 🎯 Simplified Objective
Deliver a working scoring system in **4 hours maximum** with core functionality only.

## ⏱️ Time Budget Breakdown

| Phase | Time | Tasks |
|-------|------|-------|
| **Hour 1** | 60min | Audio capture + basic scoring |
| **Hour 2** | 60min | Performance screen integration |
| **Hour 3** | 60min | Score entry + leaderboard |
| **Hour 4** | 60min | Testing + bug fixes |
| **TOTAL** | **4 hours** | |

---

## 🚀 Hour 1: Audio Capture + Scoring (60min)

### Task 1.1: Install Dependencies (5min)
```bash
pip install pyaudio numpy
```

### Task 1.2: Create Minimal AudioAnalyzer (25min)

**File:** `modules/scoring/audio_analyzer.py`

**Simplified approach:** Just collect RMS energy in real-time, skip complex FFT metrics.

```python
"""Minimal audio analyzer for 4-hour MVP."""
import pyaudio
import numpy as np
from threading import Thread, Event
from collections import deque


class AudioAnalyzer:
    """Simplified real-time audio capture."""
    
    CHUNK = 1024
    RATE = 44100
    SILENCE_THRESHOLD = 500
    
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.rms_values = deque(maxlen=5000)  # ~2 minutes
        self.is_recording = False
        self.stop_event = Event()
        self.thread = None
        
    def start_recording(self):
        """Start mic capture."""
        if self.is_recording:
            return
            
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        self.is_recording = True
        self.stop_event.clear()
        self.thread = Thread(target=self._record_loop, daemon=True)
        self.thread.start()
        
    def stop_recording(self):
        """Stop mic capture."""
        self.is_recording = False
        self.stop_event.set()
        
        if self.thread:
            self.thread.join(timeout=1.0)
            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
    def _record_loop(self):
        """Capture RMS energy only."""
        while self.is_recording:
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                rms = float(np.sqrt(np.mean(audio_data**2)))
                self.rms_values.append(rms)
            except:
                pass
                
    def get_score(self):
        """Calculate simple score from RMS values."""
        if not self.rms_values:
            return 0
            
        # Count chunks above silence threshold
        active_chunks = sum(1 for rms in self.rms_values if rms > self.SILENCE_THRESHOLD)
        total_chunks = len(self.rms_values)
        
        # Coverage percentage
        coverage = (active_chunks / total_chunks * 100) if total_chunks > 0 else 0
        
        # Average RMS of active chunks
        active_rms_values = [rms for rms in self.rms_values if rms > self.SILENCE_THRESHOLD]
        avg_rms = np.mean(active_rms_values) if active_rms_values else 0
        
        # Simple scoring: 50% coverage + 50% energy
        coverage_score = min(coverage / 80.0, 1.0) * 50  # 80% coverage = max
        energy_score = min(avg_rms / 5000.0, 1.0) * 50   # 5000 RMS = max
        
        final_score = int(coverage_score + energy_score)
        return max(0, min(100, final_score))
        
    def clear(self):
        """Clear collected data."""
        self.rms_values.clear()
        
    def cleanup(self):
        """Cleanup resources."""
        self.stop_recording()
        self.p.terminate()
```

**Time:** 25 minutes

### Task 1.3: Test Audio Capture (10min)

Create quick test:

```python
# test_audio.py
from modules.scoring.audio_analyzer import AudioAnalyzer
import time

analyzer = AudioAnalyzer()
print("Recording for 5 seconds... SING!")
analyzer.start_recording()
time.sleep(5)
analyzer.stop_recording()
score = analyzer.get_score()
print(f"Score: {score}/100")
analyzer.cleanup()
```

**Time:** 10 minutes

### Task 1.4: Update RankingManager (20min)

Ensure [`data/ranking_manager.py`](data/ranking_manager.py) properly filters by date.

**Modification needed:**
```python
# In ranking_manager.py - verify get_today_scores() works correctly
def get_today_scores(self) -> List[Dict]:
    """Get TODAY'S scores only for leaderboard display."""
    from datetime import datetime
    
    all_scores = self.load_leaderboard()
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    today_scores = []
    for score in all_scores:
        timestamp_str = score.get('timestamp', '')
        if timestamp_str:
            score_date = timestamp_str.split('T')[0]
            if score_date == current_date:
                today_scores.append(score)
    
    # Sort by score descending
    return sorted(today_scores, key=lambda x: x['score'], reverse=True)
```

**Time:** 20 minutes

**HOUR 1 TOTAL:** 60 minutes ✅

---

## 🎬 Hour 2: Performance Screen Integration (60min)

### Task 2.1: Integrate AudioAnalyzer (30min)

**Modify:** [`ui/screens/performance_screen.py`](ui/screens/performance_screen.py)

**Changes:**

1. Add import:
```python
from modules.scoring.audio_analyzer import AudioAnalyzer
```

2. In `__init__()`:
```python
self.audio_analyzer = AudioAnalyzer()
```

3. In `on_enter()`:
```python
# After existing setup...
self.audio_analyzer.clear()
self.audio_analyzer.start_recording()
print("🎤 Recording started")
```

4. Replace `finish_performance()`:
```python
def finish_performance(self):
    """Calculate score and navigate to score entry."""
    print("🎬 Finishing performance...")
    
    # Stop recording
    self.audio_analyzer.stop_recording()
    
    # Calculate score
    score = self.audio_analyzer.get_score()
    print(f"🎯 Score: {score}/100")
    
    # Cleanup
    if self.update_event:
        self.update_event.cancel()
        self.update_event = None
    
    self.audio_router.stop()
    self.video.state = 'stop'
    self.video.opacity = 0
    
    # Navigate to score entry (will create next)
    score_entry = self.manager.get_screen('score_entry')
    score_entry.set_score(score)
    self.manager.current = 'score_entry'
```

5. In `on_leave()`:
```python
# Add at the end
if hasattr(self, 'audio_analyzer'):
    self.audio_analyzer.stop_recording()
```

**Time:** 30 minutes

### Task 2.2: Test Integration (15min)

Run app, complete performance, verify:
- Microphone captures audio
- Score is calculated
- No crashes

**Time:** 15 minutes

### Task 2.3: Create config for scoring (15min)

**File:** `data/scoring_config.json`

```json
{
  "silence_threshold": 500,
  "min_rms_good": 1000,
  "max_rms_cap": 5000,
  "min_coverage_percent": 80
}
```

**Time:** 15 minutes

**HOUR 2 TOTAL:** 60 minutes ✅

---

## 📝 Hour 3: Score Entry + Leaderboard (60min)

### Task 3.1: Create Simple Score Entry Screen (25min)

**File:** `ui/screens/score_entry_screen.py`

```python
"""Simple score entry screen - text input only (no fancy keyboard)."""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

from data.ranking_manager import RankingManager


class ScoreEntryScreen(Screen):
    """Display score and collect player name."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.ranking = RankingManager()
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # Background
        with main_layout.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=lambda *args: setattr(self.bg_rect, 'pos', main_layout.pos))
        main_layout.bind(size=lambda *args: setattr(self.bg_rect, 'size', main_layout.size))
        
        # Score display
        self.score_label = Label(
            text='YOUR SCORE: 0',
            font_size='80sp',
            bold=True,
            color=(1, 0.84, 0, 1),  # Gold
            size_hint_y=0.3
        )
        main_layout.add_widget(self.score_label)
        
        # Stars display
        self.stars_label = Label(
            text='★ ★ ★ ★ ★',
            font_size='60sp',
            color=(1, 0.84, 0, 1),
            size_hint_y=0.2
        )
        main_layout.add_widget(self.stars_label)
        
        # Name input
        name_label = Label(
            text='Enter Your Name:',
            font_size='40sp',
            size_hint_y=0.1
        )
        main_layout.add_widget(name_label)
        
        self.name_input = TextInput(
            text='',
            multiline=False,
            font_size='50sp',
            size_hint=(0.8, 0.15),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(self.name_input)
        
        # Submit button
        submit_btn = Button(
            text='SUBMIT SCORE',
            font_size='40sp',
            size_hint=(0.6, 0.15),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0.5, 0, 1)
        )
        submit_btn.bind(on_press=self.submit_score)
        main_layout.add_widget(submit_btn)
        
        self.add_widget(main_layout)
        
    def set_score(self, score: int):
        """Set score to display."""
        self.score = score
        self.score_label.text = f'YOUR SCORE: {score}'
        
        # Star rating (0-5 stars)
        stars = min(5, max(0, int(score / 20)))
        self.stars_label.text = '★ ' * stars + '☆ ' * (5 - stars)
        
    def on_enter(self):
        """Clear input when entering."""
        self.name_input.text = ''
        self.name_input.focus = True
        
    def submit_score(self, instance):
        """Submit score to leaderboard."""
        name = self.name_input.text.strip()
        
        if not name:
            print("❌ Name required")
            return
            
        if len(name) < 3:
            print("❌ Name too short (min 3 chars)")
            return
            
        # Save to leaderboard
        success = self.ranking.add_score(name, self.score)
        
        if success:
            print(f"✅ Score saved: {name} = {self.score}")
            
            # Navigate to leaderboard
            leaderboard = self.manager.get_screen('leaderboard')
            leaderboard.refresh_leaderboard()
            self.manager.current = 'leaderboard'
        else:
            print("❌ Failed to save score")
```

**Time:** 25 minutes

### Task 3.2: Update Leaderboard Screen (20min)

**Modify:** [`ui/screens/leaderboard_screen.py`](ui/screens/leaderboard_screen.py)

Fix DISCREPANCY #1 - use RankingManager:

```python
def load_leaderboard(self):
    """Load TODAY'S leaderboard using RankingManager."""
    try:
        from data.ranking_manager import RankingManager
        
        ranking = RankingManager()
        today_scores = ranking.get_today_scores()  # Already filtered by date
        
        if not today_scores:
            self.status_text = "Nenhum score hoje.\nSeja o primeiro!"
            self.leaderboard_data = []
        else:
            # Already sorted by RankingManager
            self.leaderboard_data = today_scores[:10]  # Top 10
            self.status_text = f"Top {len(self.leaderboard_data)} de Hoje"
            
    except Exception as e:
        self.status_text = f"Erro: {str(e)}"
        self.leaderboard_data = []
```

**Time:** 20 minutes

### Task 3.3: Register Screen in Main (10min)

**Modify:** [`main.py`](main.py)

Add import:
```python
from ui.screens.score_entry_screen import ScoreEntryScreen
```

Add screen (after line 62):
```python
sm.add_widget(ScoreEntryScreen(name='score_entry'))
```

**Time:** 10 minutes

### Task 3.4: Update Flow (5min)

Verify flow works:
1. Performance completes → score_entry
2. Submit name → leaderboard
3. Leaderboard shows today's top 10

**Time:** 5 minutes

**HOUR 3 TOTAL:** 60 minutes ✅

---

## 🧪 Hour 4: Testing + Polish (60min)

### Task 4.1: End-to-End Testing (20min)

Test complete flow:
1. ✅ Start app → welcome
2. ✅ Instructions → countdown → performance
3. ✅ Sing (verify mic recording works)
4. ✅ Performance ends → score calculated
5. ✅ Score entry → enter name → submit
6. ✅ Leaderboard displays → shows new score
7. ✅ Return to welcome

**Time:** 20 minutes

### Task 4.2: Bug Fixes (25min)

Common issues to fix:
- [ ] Microphone not found error
- [ ] Score always 0 (silence threshold too high)
- [ ] Name input doesn't focus
- [ ] Leaderboard not updating
- [ ] Skip shortcut crashes

**Time:** 25 minutes

### Task 4.3: Minimal Polish (15min)

Quick improvements:
- [ ] Add loading text during mic initialization
- [ ] Add error message if mic fails
- [ ] Ensure score is clamped 0-100
- [ ] Add "Play Again" button on leaderboard

**Time:** 15 minutes

**HOUR 4 TOTAL:** 60 minutes ✅

---

## 📦 Final Deliverables (4 Hours)

### Core Features Working:
- ✅ Real-time microphone capture during performance
- ✅ Simple RMS-based scoring (0-100)
- ✅ Score entry screen (text input)
- ✅ Leaderboard shows today's top 10
- ✅ Scores saved to JSON permanently

### Files Created/Modified:
1. **NEW:** `modules/scoring/audio_analyzer.py` (100 lines)
2. **NEW:** `ui/screens/score_entry_screen.py` (120 lines)
3. **NEW:** `data/scoring_config.json` (8 lines)
4. **MODIFIED:** `ui/screens/performance_screen.py` (+15 lines)
5. **MODIFIED:** `ui/screens/leaderboard_screen.py` (+10 lines)
6. **MODIFIED:** `main.py` (+2 lines)
7. **MODIFIED:** `requirements.txt` (+2 lines)

### Not Included (Future):
- ❌ Virtual keyboard (use system keyboard)
- ❌ Advanced FFT metrics (pitch, spectral centroid)
- ❌ Daily reset scheduler (manual clear if needed)
- ❌ Animations
- ❌ Detailed score breakdown

---

## 🎯 Success Criteria (4-Hour MVP)

| Requirement | Status |
|-------------|--------|
| Microphone captures audio | ✅ |
| Score calculated (0-100) | ✅ |
| Player can enter name | ✅ |
| Score saved to leaderboard | ✅ |
| Leaderboard shows top 10 | ✅ |
| No crashes | ✅ |

---

## 🚀 Quick Start

```bash
# Hour 0: Setup (5min before timer starts)
pip install pyaudio numpy

# Hour 1: Create AudioAnalyzer
# Hour 2: Integrate into performance screen
# Hour 3: Create score entry + update leaderboard
# Hour 4: Test + fix bugs

# Total: 4 hours
```

---

## ⚠️ Known Limitations (MVP)

1. **Scoring is basic:** Only RMS energy + coverage (no pitch analysis)
2. **No virtual keyboard:** Uses system keyboard
3. **No daily reset:** Leaderboard shows all entries from today (manual clear if needed)
4. **No animations:** Minimal UI polish
5. **No rehearsal scoring:** Only performance mode

**These can be enhanced AFTER the 4-hour MVP is working.**

---

**END OF 4-HOUR MVP PLAN**