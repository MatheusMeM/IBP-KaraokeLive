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