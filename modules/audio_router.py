"""
Audio routing and playback for IBP-KaraokeLive.

This module manages audio playback to specific output devices using
sounddevice for direct hardware control. Supports rehearsal mode
(headphones only) and performance mode (headphones + speakers).

Based on successful testing documented in AUDIO-ROUTING-TEST-RESULTS.md
"""
import threading
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioRouter:
    """
    Audio router with device-specific playback control.

    Manages audio playback to specific output devices identified during
    testing. Uses sounddevice for low-latency, direct hardware access.

    Device IDs (from AUDIO-ROUTING-TEST-RESULTS.md):
        - Device 8: Speakers (Realtek) - Public/audience
        - Device 9: Speakers (USB Audio Device) - Singer/headphones

    Note:
        Device IDs may change if hardware is reconnected. For production,
        consider detecting devices by name rather than hardcoded IDs.
    """

    # Device IDs identified in audio routing tests
    DEVICE_SPEAKER = 8  # Native speakers (public)
    DEVICE_HEADPHONE = 9  # USB headphones (singer)

    def __init__(self):
        """Initialize audio router."""
        self.audio_data: Optional[np.ndarray] = None
        self.sample_rate: Optional[int] = None
        self.mode = 'headphone'  # 'headphone' or 'both'
        self.is_loaded = False

    def load_audio(self, filepath: str) -> bool:
        """
        Load audio file into memory.

        Args:
            filepath: Path to audio file (WAV format recommended)

        Returns:
            True if loaded successfully, False otherwise
        """
        audio_path = Path(filepath)

        if not audio_path.exists():
            print(f"❌ Audio file not found: {audio_path}")
            return False

        try:
            self.audio_data, self.sample_rate = sf.read(str(audio_path))
            self.is_loaded = True
            print(
                f"✅ Audio loaded: {audio_path.name} "
                f"({self.sample_rate} Hz)"
            )
            return True
        except Exception as e:
            print(f"❌ Error loading audio: {e}")
            self.is_loaded = False
            return False

    def play_on_speaker(self) -> None:
        """
        Play audio on speakers (public/audience output).

        Plays on device 8 (Realtek native speakers).
        """
        if not self.is_loaded or self.audio_data is None:
            print("⚠️ No audio loaded")
            return

        try:
            sd.play(
                self.audio_data,
                self.sample_rate,
                device=self.DEVICE_SPEAKER
            )
            print(f"🔊 Playing on speakers (device {self.DEVICE_SPEAKER})")
        except Exception as e:
            print(f"❌ Error playing on speakers: {e}")

    def play_on_headphone(self) -> None:
        """
        Play audio on headphones (singer output).

        Plays on device 9 (USB Audio Device headphones).
        """
        if not self.is_loaded or self.audio_data is None:
            print("⚠️ No audio loaded")
            return

        try:
            sd.play(
                self.audio_data,
                self.sample_rate,
                device=self.DEVICE_HEADPHONE
            )
            print(
                f"🎧 Playing on headphones "
                f"(device {self.DEVICE_HEADPHONE})"
            )
        except Exception as e:
            print(f"❌ Error playing on headphones: {e}")

    def play_on_both(self) -> None:
        """
        Play audio on both speakers and headphones simultaneously.

        Uses threading to start playback on both devices at nearly the
        same time. Some minimal desynchronization may occur.
        """
        if not self.is_loaded or self.audio_data is None:
            print("⚠️ No audio loaded")
            return

        try:
            # Start playback on both devices using threads
            speaker_thread = threading.Thread(target=self.play_on_speaker)
            headphone_thread = threading.Thread(
                target=self.play_on_headphone
            )

            speaker_thread.start()
            headphone_thread.start()

            print("🔊🎧 Playing on both devices")
        except Exception as e:
            print(f"❌ Error playing on both devices: {e}")

    def set_rehearsal_mode(self) -> None:
        """
        Switch to rehearsal mode (headphones only).

        In rehearsal mode, audio plays only through headphones,
        allowing the singer to practice without the audience hearing.
        """
        self.mode = 'headphone'
        print("🎧 Mode: Rehearsal (headphones only)")

    def set_performance_mode(self) -> None:
        """
        Switch to performance mode (headphones + speakers).

        In performance mode, audio plays through both headphones
        (for the singer) and speakers (for the audience).
        """
        self.mode = 'both'
        print("🔊 Mode: Performance (headphones + speakers)")

    def play(self) -> None:
        """
        Play audio according to current mode.

        Routes to appropriate device(s) based on mode:
        - Rehearsal mode: headphones only
        - Performance mode: both devices
        """
        if self.mode == 'headphone':
            self.play_on_headphone()
        elif self.mode == 'both':
            self.play_on_both()

    def stop(self) -> None:
        """Stop all audio playback on all devices."""
        sd.stop()
        print("⏹️ Playback stopped")

    def get_position(self) -> float:
        """
        Get current playback position.

        Returns:
            Current position in seconds (0.0 if not playing)

        Note:
            sounddevice doesn't provide direct position tracking.
            Consider using time.time() tracking for position.
        """
        # sounddevice doesn't provide get_pos() like Kivy
        # Position tracking would need to be implemented separately
        return 0.0

    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.

        Returns:
            True if playing, False otherwise

        Note:
            This is a simplified check. For production, implement
            proper state tracking.
        """
        # sounddevice uses callback-based playback
        # This would need proper state management
        return sd.get_stream().active if sd.get_stream() else False