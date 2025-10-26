#!/usr/bin/env python3
"""
🎤 MICROPHONE DETECTION & TEST SCRIPT
=====================================

Comprehensive audio device detection and testing for IBP-KaraokeLive.

This script will:
1. List all available audio devices
2. Identify input devices (microphones)
3. Test each microphone for functionality
4. Measure audio levels
5. Recommend best device for karaoke

Usage:
    python test_mic_detection.py

Requirements:
    pip install pyaudio numpy

Author: IBP-KaraokeLive Team
Date: 2025
"""

import pyaudio
import numpy as np
import sys
import time
from typing import List, Dict, Optional, Tuple


# ============================================================================
# CONFIGURATION
# ============================================================================

class TestConfig:
    """Configuration for microphone testing."""
    CHUNK_SIZE = 1024
    SAMPLE_RATE = 44100
    TEST_DURATION_SECONDS = 3
    SILENCE_THRESHOLD = 100  # Minimum RMS to consider "active"
    FORMAT = pyaudio.paInt16
    CHANNELS = 1


# ============================================================================
# AUDIO DEVICE DETECTION
# ============================================================================

class MicrophoneDetector:
    """Detect and test microphones using PyAudio."""
    
    def __init__(self):
        """Initialize PyAudio instance."""
        try:
            self.p = pyaudio.PyAudio()
            self.config = TestConfig()
            print("✅ PyAudio initialized successfully\n")
        except Exception as e:
            print(f"❌ Failed to initialize PyAudio: {e}")
            print("\n💡 Try: pip install pyaudio")
            sys.exit(1)
    
    def get_all_devices(self) -> List[Dict]:
        """
        Get information about all audio devices.
        
        Returns:
            List of device info dictionaries
        """
        devices = []
        device_count = self.p.get_device_count()
        
        for i in range(device_count):
            try:
                info = self.p.get_device_info_by_index(i)
                devices.append(info)
            except Exception as e:
                print(f"⚠️ Error reading device {i}: {e}")
        
        return devices
    
    def get_input_devices(self) -> List[Dict]:
        """
        Get only input devices (microphones).
        
        Returns:
            List of input device info dictionaries
        """
        all_devices = self.get_all_devices()
        input_devices = [
            dev for dev in all_devices
            if dev.get('maxInputChannels', 0) > 0
        ]
        return input_devices
    
    def print_device_list(self, devices: List[Dict], title: str = "Audio Devices"):
        """
        Print formatted list of devices.
        
        Args:
            devices: List of device info dicts
            title: Section title
        """
        print(f"\n{'='*70}")
        print(f"{title}")
        print(f"{'='*70}\n")
        
        if not devices:
            print("❌ No devices found!")
            return
        
        for idx, dev in enumerate(devices):
            device_index = dev.get('index', idx)
            name = dev.get('name', 'Unknown')
            max_inputs = dev.get('maxInputChannels', 0)
            max_outputs = dev.get('maxOutputChannels', 0)
            default_rate = dev.get('defaultSampleRate', 0)
            host_api = self.p.get_host_api_info_by_index(dev.get('hostApi', 0)).get('name', 'Unknown')
            
            # Device type indicator
            if max_inputs > 0 and max_outputs > 0:
                dev_type = "🎤🔊 INPUT+OUTPUT"
                icon = "🟢"
            elif max_inputs > 0:
                dev_type = "🎤 INPUT ONLY"
                icon = "🟢"
            elif max_outputs > 0:
                dev_type = "🔊 OUTPUT ONLY"
                icon = "🔴"
            else:
                dev_type = "❓ UNKNOWN"
                icon = "⚫"
            
            print(f"{icon} Device {device_index}: {name}")
            print(f"   Type: {dev_type}")
            print(f"   API: {host_api}")
            print(f"   Channels: {max_inputs} in / {max_outputs} out")
            print(f"   Sample Rate: {int(default_rate)} Hz")
            print()
    
    def test_microphone(self, device_index: int, duration: float = 3.0) -> Optional[Dict]:
        """
        Test a specific microphone by recording and analyzing audio.
        
        Args:
            device_index: PyAudio device index
            duration: Test duration in seconds
            
        Returns:
            Dict with test results or None if test failed
        """
        device_info = self.p.get_device_info_by_index(device_index)
        device_name = device_info.get('name', f'Device {device_index}')
        
        print(f"\n{'─'*70}")
        print(f"🧪 Testing: {device_name}")
        print(f"{'─'*70}")
        print(f"Recording for {duration} seconds... SPEAK INTO THE MIC!")
        
        try:
            # Open stream
            stream = self.p.open(
                format=self.config.FORMAT,
                channels=self.config.CHANNELS,
                rate=self.config.SAMPLE_RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.config.CHUNK_SIZE
            )
            
            # Record audio
            rms_values = []
            chunks_recorded = int(duration * self.config.SAMPLE_RATE / self.config.CHUNK_SIZE)
            
            print(f"\n{'▓' * 50}")
            print("RECORDING... ", end='', flush=True)
            
            for i in range(chunks_recorded):
                try:
                    # Read audio data
                    data = stream.read(self.config.CHUNK_SIZE, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    
                    # Calculate RMS
                    rms = float(np.sqrt(np.mean(audio_data.astype(np.float64)**2)))
                    rms_values.append(rms)
                    
                    # Visual feedback every 10 chunks
                    if i % 10 == 0:
                        print("█", end='', flush=True)
                
                except Exception as e:
                    print(f"\n⚠️ Error during recording: {e}")
                    break
            
            print(" DONE!")
            
            # Close stream
            stream.stop_stream()
            stream.close()
            
            # Analyze results
            if not rms_values:
                print("❌ No audio data captured")
                return None
            
            results = self._analyze_audio_data(rms_values)
            self._print_test_results(results)
            
            return results
        
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            return None
    
    def _analyze_audio_data(self, rms_values: List[float]) -> Dict:
        """
        Analyze recorded audio data.
        
        Args:
            rms_values: List of RMS values from recording
            
        Returns:
            Dict with analysis results
        """
        rms_array = np.array(rms_values)
        
        # Calculate statistics
        min_rms = float(np.min(rms_array))
        max_rms = float(np.max(rms_array))
        avg_rms = float(np.mean(rms_array))
        std_rms = float(np.std(rms_array))
        
        # Detect activity (above silence threshold)
        active_frames = np.sum(rms_array > self.config.SILENCE_THRESHOLD)
        total_frames = len(rms_array)
        activity_percent = (active_frames / total_frames * 100) if total_frames > 0 else 0
        
        # Detect clipping (signal too loud)
        clipping_threshold = 32000  # Near max for int16
        clipping_frames = np.sum(rms_array > clipping_threshold)
        clipping_percent = (clipping_frames / total_frames * 100) if total_frames > 0 else 0
        
        # Quality assessment
        quality = self._assess_quality(avg_rms, activity_percent, clipping_percent)
        
        return {
            'min_rms': min_rms,
            'max_rms': max_rms,
            'avg_rms': avg_rms,
            'std_rms': std_rms,
            'activity_percent': activity_percent,
            'clipping_percent': clipping_percent,
            'quality': quality,
            'total_frames': total_frames
        }
    
    def _assess_quality(self, avg_rms: float, activity: float, clipping: float) -> str:
        """
        Assess microphone quality based on metrics.
        
        Returns:
            Quality rating: "EXCELLENT", "GOOD", "POOR", or "SILENT"
        """
        if activity < 10:
            return "SILENT"
        elif clipping > 5:
            return "CLIPPING"
        elif avg_rms > 3000 and activity > 50:
            return "EXCELLENT"
        elif avg_rms > 1500 and activity > 30:
            return "GOOD"
        elif avg_rms > 500 and activity > 10:
            return "ACCEPTABLE"
        else:
            return "POOR"
    
    def _print_test_results(self, results: Dict):
        """Print formatted test results."""
        print(f"\n📊 Test Results:")
        print(f"   RMS Range:        {results['min_rms']:.0f} - {results['max_rms']:.0f}")
        print(f"   Average RMS:      {results['avg_rms']:.0f}")
        print(f"   Std Deviation:    {results['std_rms']:.0f}")
        print(f"   Activity:         {results['activity_percent']:.1f}%")
        print(f"   Clipping:         {results['clipping_percent']:.1f}%")
        print(f"   Quality Rating:   {results['quality']}")
        
        # Recommendations
        quality = results['quality']
        if quality == "EXCELLENT":
            print(f"\n   ✅ {self._get_emoji('excellent')} RECOMMENDED FOR KARAOKE!")
        elif quality == "GOOD":
            print(f"\n   ✅ {self._get_emoji('good')} Suitable for karaoke")
        elif quality == "ACCEPTABLE":
            print(f"\n   ⚠️  {self._get_emoji('acceptable')} Usable but not ideal")
        elif quality == "POOR":
            print(f"\n   ❌ {self._get_emoji('poor')} Too quiet for karaoke")
        elif quality == "SILENT":
            print(f"\n   ❌ {self._get_emoji('silent')} No audio detected!")
        elif quality == "CLIPPING":
            print(f"\n   ⚠️  {self._get_emoji('clipping')} Reduce microphone volume!")
    
    def _get_emoji(self, quality: str) -> str:
        """Get emoji for quality level."""
        emojis = {
            'excellent': '⭐⭐⭐⭐⭐',
            'good': '⭐⭐⭐⭐☆',
            'acceptable': '⭐⭐⭐☆☆',
            'poor': '⭐⭐☆☆☆',
            'silent': '☆☆☆☆☆',
            'clipping': '⚠️⚠️⚠️⚠️⚠️'
        }
        return emojis.get(quality, '❓')
    
    def test_all_microphones(self) -> List[Tuple[int, Dict]]:
        """
        Test all available input devices.
        
        Returns:
            List of (device_index, results) tuples
        """
        input_devices = self.get_input_devices()
        
        if not input_devices:
            print("\n❌ No input devices found!")
            return []
        
        print(f"\n🔍 Found {len(input_devices)} input device(s)")
        print("Testing each device (speak when prompted)...\n")
        
        all_results = []
        
        for device in input_devices:
            device_index = device['index']
            results = self.test_microphone(device_index, duration=3.0)
            
            if results:
                all_results.append((device_index, results))
            
            time.sleep(0.5)  # Brief pause between tests
        
        return all_results
    
    def recommend_best_device(self, test_results: List[Tuple[int, Dict]]) -> Optional[int]:
        """
        Recommend the best microphone based on test results.
        
        Args:
            test_results: List of (device_index, results) tuples
            
        Returns:
            Device index of best microphone or None
        """
        if not test_results:
            return None
        
        # Quality scores
        quality_scores = {
            'EXCELLENT': 5,
            'GOOD': 4,
            'ACCEPTABLE': 3,
            'POOR': 2,
            'SILENT': 1,
            'CLIPPING': 0
        }
        
        # Find best device
        best_device = None
        best_score = -1
        
        for device_index, results in test_results:
            quality = results.get('quality', 'POOR')
            score = quality_scores.get(quality, 0)
            
            # Tie-breaker: higher average RMS
            if score == best_score:
                if results['avg_rms'] > test_results[best_device][1]['avg_rms']:
                    best_device = device_index
            elif score > best_score:
                best_score = score
                best_device = device_index
        
        return best_device
    
    def cleanup(self):
        """Cleanup PyAudio resources."""
        try:
            self.p.terminate()
            print("\n✅ PyAudio terminated")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")


# ============================================================================
# INTERACTIVE TESTING
# ============================================================================

def interactive_menu(detector: MicrophoneDetector):
    """Run interactive testing menu."""
    while True:
        print(f"\n{'='*70}")
        print("🎤 MICROPHONE TEST MENU")
        print(f"{'='*70}")
        print("1. List all audio devices")
        print("2. List input devices only")
        print("3. Test specific device")
        print("4. Test all input devices")
        print("5. Get recommendation")
        print("0. Exit")
        print(f"{'─'*70}")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            devices = detector.get_all_devices()
            detector.print_device_list(devices, "All Audio Devices")
        
        elif choice == '2':
            devices = detector.get_input_devices()
            detector.print_device_list(devices, "Input Devices (Microphones)")
        
        elif choice == '3':
            device_index = input("Enter device index: ").strip()
            try:
                device_index = int(device_index)
                detector.test_microphone(device_index, duration=3.0)
            except ValueError:
                print("❌ Invalid device index")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '4':
            results = detector.test_all_microphones()
            
            if results:
                print(f"\n{'='*70}")
                print("📊 SUMMARY OF ALL TESTS")
                print(f"{'='*70}")
                
                for device_index, result in results:
                    device_info = detector.p.get_device_info_by_index(device_index)
                    name = device_info.get('name', f'Device {device_index}')
                    quality = result.get('quality', 'UNKNOWN')
                    avg_rms = result.get('avg_rms', 0)
                    
                    print(f"\nDevice {device_index}: {name}")
                    print(f"   Quality: {quality}")
                    print(f"   Avg RMS: {avg_rms:.0f}")
        
        elif choice == '5':
            results = detector.test_all_microphones()
            best = detector.recommend_best_device(results)
            
            if best is not None:
                device_info = detector.p.get_device_info_by_index(best)
                name = device_info.get('name', f'Device {best}')
                
                print(f"\n{'='*70}")
                print("🏆 RECOMMENDATION")
                print(f"{'='*70}")
                print(f"\n✅ Best microphone: Device {best}")
                print(f"   Name: {name}")
                print(f"\n💡 Use this in your code:")
                print(f"   device_index = {best}")
                print(f"{'='*70}")
            else:
                print("\n❌ Could not determine best device")
        
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")


# ============================================================================
# AUTOMATED TESTING
# ============================================================================

def automated_test():
    """Run automated test and report."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║          🎤 AUTOMATED MICROPHONE DETECTION & TEST 🎤             ║
║                                                                  ║
║  This script will automatically detect and test all              ║
║  microphones connected to your system.                           ║
║                                                                  ║
║  When prompted, SPEAK INTO THE MICROPHONE to test it.           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    detector = MicrophoneDetector()
    
    # Show all devices
    all_devices = detector.get_all_devices()
    detector.print_device_list(all_devices, "All Audio Devices Detected")
    
    # Show input devices
    input_devices = detector.get_input_devices()
    detector.print_device_list(input_devices, "Input Devices (Microphones)")
    
    # Test all microphones
    input(f"\n{'▶'*70}\nPress ENTER to begin testing microphones...")
    results = detector.test_all_microphones()
    
    # Get recommendation
    if results:
        best = detector.recommend_best_device(results)
        
        if best is not None:
            device_info = detector.p.get_device_info_by_index(best)
            name = device_info.get('name', f'Device {best}')
            
            print(f"\n{'='*70}")
            print("🏆 FINAL RECOMMENDATION")
            print(f"{'='*70}")
            print(f"\n✅ Best microphone for karaoke: Device {best}")
            print(f"   Name: {name}")
            print(f"\n💡 Configuration for IBP-KaraokeLive:")
            print(f"   In audio_analyzer.py, add:")
            print(f"   ```python")
            print(f"   self.stream = self.p.open(")
            print(f"       format=pyaudio.paInt16,")
            print(f"       channels=1,")
            print(f"       rate=self.RATE,")
            print(f"       input=True,")
            print(f"       input_device_index={best},  # <-- ADD THIS LINE")
            print(f"       frames_per_buffer=self.CHUNK")
            print(f"   )")
            print(f"   ```")
            print(f"{'='*70}\n")
    
    # Cleanup
    detector.cleanup()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        # Interactive mode
        detector = MicrophoneDetector()
        try:
            interactive_menu(detector)
        finally:
            detector.cleanup()
    else:
        # Automated mode (default)
        automated_test()


if __name__ == '__main__':
    main()