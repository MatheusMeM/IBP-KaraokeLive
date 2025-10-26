"""
Audio routing and playback for IBP-KaraokeLive.

This module manages audio playback to specific output devices using
sounddevice for direct hardware control. Supports rehearsal mode
(headphones only) and performance mode (headphones + speakers with
separate audio files).

Based on successful testing documented in AUDIO-ROUTING-TEST-RESULTS.md
"""
import threading
import time
from pathlib import Path
from typing import Optional, Dict

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
        self.audio_data: Dict[str, Optional[np.ndarray]] = {
            'headphone': None,
            'speaker': None
        }
        self.sample_rate: Optional[int] = None
        self.mode = 'rehearsal'  # 'rehearsal' or 'performance'
        self.is_loaded = False
        self.start_time = 0
        self.duration = 0
        self.is_playing_flag = False
        self.streams: Dict[str, Optional[sd.OutputStream]] = {
            'headphone': None,
            'speaker': None
        }

    def load_audio(self, vocal_filepath: str,
                   instrumental_filepath: Optional[str] = None) -> bool:
        """
        Load audio file(s) into memory.

        Args:
            vocal_filepath: Path to vocal track (for headphones)
            instrumental_filepath: Path to instrumental track
                                 (for speakers in performance mode)

        Returns:
            True if loaded successfully, False otherwise
        """
        vocal_path = Path(vocal_filepath)

        if not vocal_path.exists():
            print(f"❌ Vocal audio file not found: {vocal_path}")
            return False

        try:
            # Load vocal track
            data, sr = sf.read(str(vocal_path))
            self.audio_data['headphone'] = data
            self.sample_rate = sr
            self.duration = len(data) / sr
            
            print(
                f"✅ Vocal audio loaded: {vocal_path.name} "
                f"({sr} Hz, {self.duration:.1f}s)"
            )
            
            # Load instrumental track if provided (performance mode)
            if instrumental_filepath:
                inst_path = Path(instrumental_filepath)
                if inst_path.exists():
                    inst_data, inst_sr = sf.read(str(inst_path))
                    if inst_sr != sr:
                        print(
                            f"⚠️ Sample rate mismatch: "
                            f"{inst_sr} vs {sr}"
                        )
                        return False
                    self.audio_data['speaker'] = inst_data
                    print(
                        f"✅ Instrumental audio loaded: "
                        f"{inst_path.name}"
                    )
                else:
                    print(f"⚠️ Instrumental file not found: {inst_path}")
            
            self.is_loaded = True
            return True
        except Exception as e:
            print(f"❌ Error loading audio: {e}")
            self.is_loaded = False
            return False

    def _play_stream(self, device: int, data: np.ndarray,
                     stream_key: str) -> None:
        """
        Play audio stream on specified device.

        Args:
            device: Device ID
            data: Audio data array
            stream_key: Key for storing stream reference
        """
        try:
            # Use blocking playback for complete file playback
            sd.play(data, self.sample_rate, device=device, blocking=True)
        except Exception as e:
            print(f"❌ Error playing on device {device}: {e}")

    def set_rehearsal_mode(self) -> None:
        """
        Switch to rehearsal mode (headphones only).

        In rehearsal mode, audio plays only through headphones,
        allowing the singer to practice without the audience hearing.
        """
        self.mode = 'rehearsal'
        print("🎧 Mode: Rehearsal (headphones only)")

    def set_performance_mode(self) -> None:
        """
        Switch to performance mode (vocal on headphones +
        instrumental on speakers).

        In performance mode:
        - Vocal track plays through headphones (for the singer)
        - Instrumental track plays through speakers (for the audience)
        """
        self.mode = 'performance'
        print("🔊 Mode: Performance (vocal+instrumental)")

    def play(self) -> None:
        """
        Play audio according to current mode.

        Routes to appropriate device(s) based on mode:
        - Rehearsal mode: vocal on headphones only
        - Performance mode: vocal on headphones + instrumental
                           on speakers
        """
        if not self.is_loaded:
            print("⚠️ No audio loaded")
            return

        self.start_time = time.time()
        self.is_playing_flag = True

        if self.mode == 'rehearsal':
            # Rehearsal: vocal on headphones only
            if self.audio_data['headphone'] is not None:
                print(
                    f"🎧 Playing rehearsal on headphones "
                    f"(device {self.DEVICE_HEADPHONE})"
                )
                thread = threading.Thread(
                    target=self._play_stream,
                    args=(
                        self.DEVICE_HEADPHONE,
                        self.audio_data['headphone'],
                        'headphone'
                    )
                )
                thread.daemon = True
                thread.start()
        
        elif self.mode == 'performance':
            # Performance: vocal on headphones + instrumental on speakers
            if (self.audio_data['headphone'] is not None and
                self.audio_data['speaker'] is not None):
                
                print(
                    f"🔊🎧 Playing performance: "
                    f"vocal on {self.DEVICE_HEADPHONE}, "
                    f"instrumental on {self.DEVICE_SPEAKER}"
                )
                
                # Start both streams simultaneously
                headphone_thread = threading.Thread(
                    target=self._play_stream,
                    args=(
                        self.DEVICE_HEADPHONE,
                        self.audio_data['headphone'],
                        'headphone'
                    )
                )
                speaker_thread = threading.Thread(
                    target=self._play_stream,
                    args=(
                        self.DEVICE_SPEAKER,
                        self.audio_data['speaker'],
                        'speaker'
                    )
                )
                
                headphone_thread.daemon = True
                speaker_thread.daemon = True
                
                headphone_thread.start()
                speaker_thread.start()
            else:
                print(
                    "⚠️ Performance mode requires both "
                    "vocal and instrumental tracks"
                )

    def stop(self) -> None:
        """Stop all audio playback on all devices."""
        sd.stop()
        print("⏹️ Playback stopped")

    def get_position(self) -> float:
        """
        Get current playback position based on elapsed time.

        Returns:
            Current position in seconds (0.0 if not playing)
        """
        if not self.is_playing_flag:
            return 0.0
        
        elapsed = time.time() - self.start_time
        return min(elapsed, self.duration)

    def get_duration(self) -> float:
        """
        Get total audio duration.

        Returns:
            Duration in seconds
        """
        return self.duration

    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.

        Returns:
            True if playing, False otherwise
        """
        if not self.is_playing_flag:
            return False
        
        # Check if we've exceeded duration
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            self.is_playing_flag = False
            return False
        
        return True