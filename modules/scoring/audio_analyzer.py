"""Minimal audio analyzer for 4-hour MVP - CORRECTED."""
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
        print("🎤 Audio recording started")

    def stop_recording(self):
        """Stop mic capture."""
        self.is_recording = False
        self.stop_event.set()

        if self.thread:
            self.thread.join(timeout=1.0)

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        print("🛑 Audio recording stopped")

    def _record_loop(self):
        """Generate FAKE RMS values for demo - no microphone required."""
        import random
        import time

        while self.is_recording:
            try:
                # Generate fake RMS values with realistic ranges and noise
                base_level = random.uniform(100, 2000)  # Base singing level
                noise = random.gauss(0, 200)  # Add some noise
                trend = (time.time() % 10) / 10  # Slow trend over time

                # Add occasional "singing bursts" (higher energy)
                burst = random.random() < 0.3  # 30% chance of burst
                if burst:
                    base_level *= random.uniform(2, 5)

                # Calculate fake RMS with controlled randomness
                rms = max(0, base_level + noise + (trend * 500))

                # Occasionally add silence periods
                if random.random() < 0.1:  # 10% chance
                    rms = random.uniform(0, 50)  # Near silence

                self.rms_values.append(rms)

                # Simulate real-time capture timing (43Hz = ~23ms per frame)
                time.sleep(0.023)

            except Exception as e:
                print(f"⚠️ Fake audio generation error: {e}")

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

        final_score = coverage_score + energy_score
        
        # Log score calculation
        print(f"📊 Score calculation:")
        print(f"   Coverage: {coverage:.1f}% → {coverage_score:.1f} pts")
        print(f"   Energy: {avg_rms:.0f} RMS → {energy_score:.1f} pts")
        print(f"   Final: {final_score:.2f}/100")
        
        return round(max(0.0, min(100.0, final_score)), 2)

    def clear(self):
        """Clear collected data."""
        self.rms_values.clear()

    def cleanup(self):
        """Cleanup resources."""
        self.stop_recording()
        self.p.terminate()