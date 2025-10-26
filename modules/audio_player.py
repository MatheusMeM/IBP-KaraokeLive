"""
Audio player with device-specific routing support.

This module provides a high-level interface for audio playback with
routing support. It uses AudioRouter internally for device-specific
playback while maintaining a simple play/stop/position interface.
"""
from pathlib import Path
from typing import Optional

from modules.audio_router import AudioRouter


class SimpleAudioPlayer:
    """
    Audio player with routing support.

    Provides a simple interface for playing audio files with automatic
    routing to appropriate output devices (headphones, speakers, or both)
    based on the configured mode.

    Uses AudioRouter internally for device-specific playback control.
    """

    def __init__(self, audio_path: str, router: Optional[AudioRouter] = None):
        """
        Initialize audio player.

        Args:
            audio_path: Path to audio file (relative or absolute)
            router: Optional AudioRouter instance. If None, creates new one
        """
        self.audio_path = Path(audio_path)
        self.router = router if router is not None else AudioRouter()
        self.is_loaded = False

        self._load()

    def _load(self):
        """Load audio file using router."""
        if not self.audio_path.exists():
            print(f"❌ Audio file not found: {self.audio_path}")
            return

        self.is_loaded = self.router.load_audio(str(self.audio_path))

        if self.is_loaded:
            print(f"✅ Audio loaded: {self.audio_path.name}")
        else:
            print(f"❌ Error loading audio: {self.audio_path}")

    def play(self):
        """
        Start audio playback.

        Plays according to router's current mode (headphone or both).
        """
        if self.is_loaded:
            self.router.play()

    def stop(self):
        """Stop audio playback on all devices."""
        self.router.stop()

    def get_position(self) -> float:
        """
        Get current playback position.

        Returns:
            Current position in seconds (0.0 if not playing)

        Note:
            Position tracking with sounddevice requires manual time
            tracking. This is a simplified implementation.
        """
        return self.router.get_position()

    def get_duration(self) -> float:
        """
        Get total audio duration.

        Returns:
            Total duration in seconds (0.0 if not loaded)
        """
        if self.is_loaded and self.router.audio_data is not None:
            # Calculate duration: samples / sample_rate
            return len(self.router.audio_data) / self.router.sample_rate
        return 0.0

    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.

        Returns:
            True if playing, False otherwise
        """
        return self.router.is_playing()

    def set_rehearsal_mode(self):
        """Switch to rehearsal mode (headphones only)."""
        self.router.set_rehearsal_mode()

    def set_performance_mode(self):
        """Switch to performance mode (headphones + speakers)."""
        self.router.set_performance_mode()