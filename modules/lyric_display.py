"""
Lyric synchronization and display management.

This module handles loading lyrics from JSON files and synchronizing
them with audio playback based on timestamps. It provides the current
lyric line and context (previous/next lines) for UI display.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional


class LyricLine:
    """
    Represents a single lyric line with timing information.

    Attributes:
        start: Start time in seconds
        end: End time in seconds
        text: Lyric text content
    """

    def __init__(self, start: float, end: float, text: str):
        """
        Initialize lyric line.

        Args:
            start: Start time in seconds
            end: End time in seconds
            text: Lyric text to display
        """
        self.start = start
        self.end = end
        self.text = text


class LyricDisplay:
    """
    Lyric synchronization manager with sliding window context.

    Loads lyrics from JSON file and provides synchronized access to
    lyric lines based on current playback time. Uses a sliding window
    approach to show previous, current, and next lines.
    """

    def __init__(self, lyrics_file: str):
        """
        Initialize lyric display system.

        Args:
            lyrics_file: Path to JSON file containing lyric data
        """
        self.lyrics_file = Path(lyrics_file)
        self.lines: List[LyricLine] = []
        self.current_index = -1  # Start with no active line

        self._load()

    def _load(self):
        """Load and parse lyrics from JSON file."""
        if not self.lyrics_file.exists():
            print(f"❌ Lyrics file not found: {self.lyrics_file}")
            return

        with open(self.lyrics_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert JSON data to LyricLine objects
        for line_data in data['lines']:
            line = LyricLine(
                start=line_data['start'],
                end=line_data['end'],
                text=line_data['text']
            )
            self.lines.append(line)

        print(f"✅ {len(self.lines)} lyric lines loaded")

    def get_current_line(self, current_time: float) -> Optional[LyricLine]:
        """
        Get the lyric line for current playback time.

        Args:
            current_time: Current playback position in seconds

        Returns:
            LyricLine if a line is active at current_time, None otherwise
        """
        for i, line in enumerate(self.lines):
            if line.start <= current_time < line.end:
                self.current_index = i
                return line

        # No line active at this time
        self.current_index = -1
        return None

    def get_context_lines(self, current_time: float) -> Dict[str, Optional[str]]:
        """
        Get previous, current, and next lyric lines using sliding window.

        Provides context for UI display in karaoke style:
        - prev: Line that was just sung (if any)
        - current: Line being sung right now (if any)
        - next: Line coming up next (if any)

        Args:
            current_time: Current playback position in seconds

        Returns:
            Dict with keys 'prev', 'current', 'next' mapping to lyric
            text strings or None if not available
        """
        # Get current active line
        current = self.get_current_line(current_time)

        result = {
            'prev': None,
            'current': None,
            'next': None
        }

        # If no active line, return empty window
        if current is None:
            return result

        # We have an active line at self.current_index
        idx = self.current_index

        # Previous line (the one that was sung before current)
        if idx > 0:
            result['prev'] = self.lines[idx - 1].text

        # Current line (being sung now)
        result['current'] = current.text

        # Next line (coming up after current finishes)
        if idx < len(self.lines) - 1:
            result['next'] = self.lines[idx + 1].text

        return result