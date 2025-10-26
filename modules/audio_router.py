"""
Audio routing and playback for IBP-KaraokeLive.

This module manages audio playback to specific output devices using
sounddevice for direct hardware control. Supports rehearsal mode
(headphones only) and performance mode (headphones + speakers with
separate audio files).

REFACTORED: Improved stop mechanism to ensure both streams stop immediately.
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
        
        # Store actual stream objects for direct control
        self.active_streams: Dict[str, Optional[sd.OutputStream]] = {
            'headphone': None,
            'speaker': None
        }
        
        # Thread management
        self.playback_threads: Dict[str, Optional[threading.Thread]] = {
            'headphone': None,
            'speaker': None
        }
        
        # Stop control
        self.stop_lock = threading.Lock()
        self.should_stop = threading.Event()  # Thread-safe event flag
        self.is_stopping = False  # Prevent duplicate stop calls

    def load_audio(self, vocal_filepath: str,
                   instrumental_filepath: Optional[str] = None) -> bool:
        """
        Load audio file(s) into memory.

        Args:
            vocal_filepath: Path to vocal track (for headphones)
            instrumental_filepath: Path to instrumental track (for speakers)

        Returns:
            True if loaded successfully, False otherwise
        """
        vocal_path = Path(vocal_filepath)

        if not vocal_path.exists():
            print(f"❌ Vocal audio file not found: {vocal_path}")
            return False

        try:
            # Load vocal track
            data, sr = sf.read(str(vocal_path), dtype='float32')
            self.audio_data['headphone'] = data
            self.sample_rate = sr
            self.duration = len(data) / sr
            
            print(
                f"✅ Vocal audio loaded: {vocal_path.name} "
                f"({sr} Hz, {self.duration:.1f}s)"
            )
            
            # Load instrumental track if provided
            if instrumental_filepath:
                inst_path = Path(instrumental_filepath)
                if inst_path.exists():
                    inst_data, inst_sr = sf.read(str(inst_path), dtype='float32')
                    if inst_sr != sr:
                        print(f"⚠️ Sample rate mismatch: {inst_sr} vs {sr}")
                        return False
                    self.audio_data['speaker'] = inst_data
                    print(f"✅ Instrumental audio loaded: {inst_path.name}")
                else:
                    print(f"⚠️ Instrumental file not found: {inst_path}")
            
            self.is_loaded = True
            return True
        except Exception as e:
            print(f"❌ Error loading audio: {e}")
            self.is_loaded = False
            return False

    def _play_stream(self, device: int, data: np.ndarray, stream_key: str) -> None:
        """
        Play audio stream on specified device using callback-based non-blocking approach.

        Args:
            device: Device ID
            data: Audio data array
            stream_key: Key for storing stream reference ('headphone' or 'speaker')
        """
        stream = None
        current_frame = [0]  # Use list to allow modification in callback
        
        def audio_callback(outdata, frames, time_info, status):
            """Callback function for audio playback."""
            try:
                if status:
                    print(f"⚠️ Stream '{stream_key}' status: {status}")
                
                # Check if we should stop
                if self.should_stop.is_set():
                    raise sd.CallbackStop()
                
                # Calculate how much data to write
                start = current_frame[0]
                end = min(start + frames, len(data))
                
                if start >= len(data):
                    # Reached end of audio
                    raise sd.CallbackStop()
                
                # Get the chunk to play
                chunk = data[start:end]
                
                # If chunk is shorter than frames, pad with zeros
                if len(chunk) < frames:
                    needed = frames - len(chunk)
                    if len(data.shape) > 1:
                        # Stereo - pad with zeros matching the channel count
                        padding = np.zeros((needed, data.shape[1]), dtype='float32')
                        chunk = np.concatenate([chunk, padding], axis=0)
                    else:
                        # Mono - pad with zeros
                        padding = np.zeros(needed, dtype='float32')
                        chunk = np.concatenate([chunk, padding])
                
                # Handle shape matching for output
                if len(chunk.shape) == 1 and len(outdata.shape) == 2:
                    # Mono audio but stereo output expected - broadcast to both channels
                    outdata[:, 0] = chunk
                    outdata[:, 1] = chunk
                elif len(chunk.shape) == 2 and len(outdata.shape) == 1:
                    # Stereo audio but mono output - mix down
                    outdata[:] = np.mean(chunk, axis=1)
                else:
                    # Shapes match - direct copy
                    outdata[:] = chunk
                
                current_frame[0] = end
                
            except sd.CallbackStop:
                # Re-raise CallbackStop
                raise
            except Exception as e:
                print(f"❌ Callback error in '{stream_key}': {e}")
                import traceback
                traceback.print_exc()
                raise sd.CallbackStop()
        
        try:
            print(f"🎵 Starting stream '{stream_key}' on device {device}")
            
            # Determine number of channels
            channels = data.shape[1] if len(data.shape) > 1 else 1
            
            # Create output stream with callback (non-blocking)
            stream = sd.OutputStream(
                device=device,
                samplerate=self.sample_rate,
                channels=channels,
                callback=audio_callback,
                blocksize=2048,
                dtype='float32'
            )
            
            # Store stream reference for external control
            with self.stop_lock:
                self.active_streams[stream_key] = stream
            
            # Start stream (non-blocking - callback handles the data)
            stream.start()
            print(f"  ✓ Stream '{stream_key}' started (active={stream.active})")
            
            # Wait for completion or stop signal
            iteration = 0
            while stream.active and not self.should_stop.is_set():
                time.sleep(0.05)
                iteration += 1
                # Log every 2 seconds to monitor progress
                if iteration % 40 == 0:
                    elapsed = current_frame[0] / self.sample_rate
                    print(f"  ⏱️ Stream '{stream_key}': {elapsed:.1f}s / {len(data)/self.sample_rate:.1f}s")
            
            # Check why we exited
            if self.should_stop.is_set():
                print(f"⏹️ Stream '{stream_key}' stopped by signal")
            elif not stream.active:
                print(f"✅ Stream '{stream_key}' completed naturally")
            else:
                print(f"⚠️ Stream '{stream_key}' exited loop unexpectedly")
                
        except sd.CallbackStop:
            # Normal callback stop - not an error
            print(f"✅ Stream '{stream_key}' stopped via callback")
        except Exception as e:
            print(f"❌ Error in stream '{stream_key}' on device {device}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Clean up stream
            if stream is not None:
                try:
                    if stream.active:
                        stream.stop()
                    stream.close()
                except Exception as e:
                    print(f"⚠️ Error closing stream '{stream_key}': {e}")
            
            # Clear stream reference
            with self.stop_lock:
                if self.active_streams.get(stream_key) == stream:
                    self.active_streams[stream_key] = None

    def set_rehearsal_mode(self) -> None:
        """Switch to rehearsal mode (headphones only)."""
        self.mode = 'rehearsal'
        print("🎧 Mode: Rehearsal (headphones only)")

    def set_performance_mode(self) -> None:
        """Switch to performance mode (vocal on headphones + instrumental on speakers)."""
        self.mode = 'performance'
        print("🔊 Mode: Performance (vocal+instrumental)")

    def play(self) -> None:
        """
        Play audio according to current mode.

        Routes to appropriate device(s) based on mode:
        - Rehearsal mode: vocal on headphones only
        - Performance mode: vocal on headphones + instrumental on speakers
        """
        if not self.is_loaded:
            print("⚠️ No audio loaded")
            return
        
        # Prevent multiple simultaneous playbacks
        if self.is_playing_flag:
            print("⚠️ Already playing - ignoring play() call")
            return

        # CRITICAL: Reset stop flag before starting new playback
        self.should_stop.clear()
        
        self.start_time = time.time()
        self.is_playing_flag = True

        if self.mode == 'rehearsal':
            # Rehearsal: vocal on headphones only
            if self.audio_data['headphone'] is not None:
                print(f"🎧 Starting rehearsal on device {self.DEVICE_HEADPHONE}")
                
                thread = threading.Thread(
                    target=self._play_stream,
                    args=(self.DEVICE_HEADPHONE, self.audio_data['headphone'], 'headphone'),
                    daemon=True,
                    name="AudioThread-Headphone"
                )
                
                self.playback_threads['headphone'] = thread
                thread.start()
        
        elif self.mode == 'performance':
            # Performance: vocal on headphones + instrumental on speakers
            if (self.audio_data['headphone'] is not None and
                self.audio_data['speaker'] is not None):
                
                print(f"🔊🎧 Starting performance mode:")
                print(f"  - Vocal on device {self.DEVICE_HEADPHONE}")
                print(f"  - Instrumental on device {self.DEVICE_SPEAKER}")
                
                # Create both threads
                headphone_thread = threading.Thread(
                    target=self._play_stream,
                    args=(self.DEVICE_HEADPHONE, self.audio_data['headphone'], 'headphone'),
                    daemon=True,
                    name="AudioThread-Headphone"
                )
                
                speaker_thread = threading.Thread(
                    target=self._play_stream,
                    args=(self.DEVICE_SPEAKER, self.audio_data['speaker'], 'speaker'),
                    daemon=True,
                    name="AudioThread-Speaker"
                )
                
                # Store references
                self.playback_threads['headphone'] = headphone_thread
                self.playback_threads['speaker'] = speaker_thread
                
                # Start both simultaneously
                headphone_thread.start()
                speaker_thread.start()
            else:
                print("⚠️ Performance mode requires both vocal and instrumental tracks")

    def stop(self) -> None:
        """
        Stop all audio playback immediately and forcefully.
        
        Safe to call multiple times or when not playing.
        
        This method uses multiple strategies to ensure ALL audio stops:
        1. Sets thread-safe stop flag
        2. Stops individual stream objects
        3. Calls global sd.stop() as backup
        4. Waits for threads to terminate
        """
        # If not playing, nothing to do
        if not self.is_playing_flag and not any(self.playback_threads.values()):
            print("ℹ️ No active playback to stop")
            return
        
        print("🛑 STOPPING ALL AUDIO...")
        
        # Mark as not playing
        self.is_playing_flag = False
        
        # Signal all threads to stop (thread-safe)
        self.should_stop.set()
        
        # Small delay to let callbacks see the stop flag
        time.sleep(0.05)
        
        # STRATEGY 1: Stop individual streams directly
        with self.stop_lock:
            for key, stream in list(self.active_streams.items()):
                if stream is not None:
                    try:
                        print(f"  ⏹️ Stopping stream: {key}")
                        if stream.active:
                            stream.stop()
                        stream.close()
                    except Exception as e:
                        print(f"  ⚠️ Error stopping {key}: {e}")
                    finally:
                        self.active_streams[key] = None
        
        # STRATEGY 2: Global sounddevice stop (catches any orphaned streams)
        try:
            sd.stop()
            print("  ✅ Global sd.stop() called")
        except Exception as e:
            print(f"  ⚠️ sd.stop() error: {e}")
        
        # Give audio backend time to actually stop
        time.sleep(0.1)
        
        # STRATEGY 3: Wait for threads to finish
        for key, thread in list(self.playback_threads.items()):
            if thread and thread.is_alive():
                print(f"  ⏳ Waiting for thread '{key}'...")
                thread.join(timeout=0.5)
                if thread.is_alive():
                    print(f"  ⚠️ Thread '{key}' did not stop gracefully (will exit on its own)")
        
        # Clear all references
        self.playback_threads = {'headphone': None, 'speaker': None}
        self.active_streams = {'headphone': None, 'speaker': None}
        
        print("✅ ALL AUDIO STOPPED")

    def get_position(self) -> float:
        """Get current playback position in seconds."""
        if not self.is_playing_flag:
            return 0.0
        
        elapsed = time.time() - self.start_time
        return min(elapsed, self.duration)

    def get_duration(self) -> float:
        """Get total audio duration in seconds."""
        return self.duration

    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        if not self.is_playing_flag:
            return False
        
        # Check if we've exceeded duration
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            self.is_playing_flag = False
            return False
        
        return True