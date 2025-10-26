"""
Integration tests for core karaoke modules.

Tests the integration of audio_player, audio_router, and lyric_display
modules to ensure they work together correctly for the karaoke system.
"""
import sys
import time
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules.audio_router import AudioRouter
from modules.audio_player import SimpleAudioPlayer
from modules.lyric_display import LyricDisplay
from config.app_config import AUDIO_FILE, LYRICS_FILE


def test_audio_router_basic():
    """Test basic AudioRouter functionality."""
    print("\n" + "="*60)
    print("TEST 1: AudioRouter Basic Functionality")
    print("="*60)

    router = AudioRouter()

    # Test mode switching
    print("\n1. Testing mode switching...")
    router.set_rehearsal_mode()
    assert router.mode == 'headphone', "Should be in headphone mode"
    print("✅ Rehearsal mode set correctly")

    router.set_performance_mode()
    assert router.mode == 'both', "Should be in both mode"
    print("✅ Performance mode set correctly")

    # Test audio loading
    print("\n2. Testing audio loading...")
    test_audio = Path('assets/audio/Ibp - Energia da Revolucao.wav')

    if test_audio.exists():
        success = router.load_audio(str(test_audio))
        assert success, "Audio should load successfully"
        assert router.is_loaded, "Router should be marked as loaded"
        print(f"✅ Audio loaded: {test_audio.name}")
    else:
        print(f"⚠️ Test audio not found: {test_audio}")
        print("   Skipping audio load test")

    print("\n✅ AudioRouter basic tests passed")


def test_simple_audio_player():
    """Test SimpleAudioPlayer integration with AudioRouter."""
    print("\n" + "="*60)
    print("TEST 2: SimpleAudioPlayer Integration")
    print("="*60)

    test_audio = Path('assets/audio/Ibp - Energia da Revolucao.wav')

    if not test_audio.exists():
        print(f"⚠️ Test audio not found: {test_audio}")
        print("   Skipping SimpleAudioPlayer test")
        return

    print("\n1. Creating audio player...")
    player = SimpleAudioPlayer(str(test_audio))

    assert player.is_loaded, "Player should have loaded audio"
    print("✅ Audio player initialized")

    print("\n2. Testing duration calculation...")
    duration = player.get_duration()
    assert duration > 0, "Duration should be positive"
    print(f"✅ Audio duration: {duration:.2f} seconds")

    print("\n3. Testing mode switching...")
    player.set_rehearsal_mode()
    assert player.router.mode == 'headphone', "Should be rehearsal mode"
    print("✅ Rehearsal mode set")

    player.set_performance_mode()
    assert player.router.mode == 'both', "Should be performance mode"
    print("✅ Performance mode set")

    print("\n✅ SimpleAudioPlayer tests passed")


def test_lyric_display():
    """Test LyricDisplay functionality."""
    print("\n" + "="*60)
    print("TEST 3: LyricDisplay Functionality")
    print("="*60)

    lyrics_path = Path(LYRICS_FILE)

    if not lyrics_path.exists():
        print(f"⚠️ Lyrics file not found: {lyrics_path}")
        print("   Skipping LyricDisplay test")
        return

    print("\n1. Loading lyrics...")
    display = LyricDisplay(LYRICS_FILE)

    assert len(display.lines) > 0, "Should have loaded lyrics"
    print(f"✅ Loaded {len(display.lines)} lyric lines")

    print("\n2. Testing lyric synchronization...")

    # Test at start (0 seconds)
    current = display.get_current_line(0.5)
    assert current is not None, "Should have lyric at 0.5s"
    print(f"   At 0.5s: '{current.text}'")

    # Test in middle
    current = display.get_current_line(10.0)
    if current:
        print(f"   At 10.0s: '{current.text}'")

    # Test context lines
    print("\n3. Testing context lines...")
    context = display.get_context_lines(7.0)

    assert context['current'] is not None, "Should have current line"
    print(f"   Previous: {context['prev']}")
    print(f"   Current:  {context['current']}")
    print(f"   Next:     {context['next']}")

    print("\n✅ LyricDisplay tests passed")


def test_full_integration():
    """Test full integration of all modules."""
    print("\n" + "="*60)
    print("TEST 4: Full Integration Test")
    print("="*60)

    test_audio = Path('assets/audio/Ibp - Energia da Revolucao.wav')
    lyrics_path = Path(LYRICS_FILE)

    if not test_audio.exists():
        print(f"⚠️ Test audio not found: {test_audio}")
        print("   Skipping full integration test")
        return

    if not lyrics_path.exists():
        print(f"⚠️ Lyrics file not found: {lyrics_path}")
        print("   Skipping full integration test")
        return

    print("\n1. Initializing all modules...")

    # Create shared router
    router = AudioRouter()
    router.set_rehearsal_mode()

    # Create player with shared router
    player = SimpleAudioPlayer(str(test_audio), router=router)

    # Create lyric display
    lyrics = LyricDisplay(LYRICS_FILE)

    assert player.is_loaded, "Player should be loaded"
    assert len(lyrics.lines) > 0, "Lyrics should be loaded"
    print("✅ All modules initialized")

    print("\n2. Simulating karaoke playback...")
    print("   (Testing without actual audio playback)")

    # Simulate time progression
    test_times = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0]

    for t in test_times:
        context = lyrics.get_context_lines(t)
        if context['current']:
            print(f"   {t:5.1f}s: {context['current']}")

    print("\n3. Testing mode transitions...")

    # Rehearsal -> Performance transition
    router.set_rehearsal_mode()
    assert router.mode == 'headphone', "Should be rehearsal mode"
    print("✅ Rehearsal mode active (headphones only)")

    router.set_performance_mode()
    assert router.mode == 'both', "Should be performance mode"
    print("✅ Performance mode active (headphones + speakers)")

    print("\n✅ Full integration test passed")


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "🎤"*30)
    print("IBP-KaraokeLive - Core Modules Integration Tests")
    print("🎤"*30)

    try:
        test_audio_router_basic()
        test_simple_audio_player()
        test_lyric_display()
        test_full_integration()

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        print("\nCore modules are ready for integration with UI screens.")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()