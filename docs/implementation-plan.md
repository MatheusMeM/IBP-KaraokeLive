# Implementation Plan: WebVTT to JSON Converter

## Overview
Implement Option 1 (Direct Parse & Convert) to convert WebVTT lyrics to JSON format for the IBP Karaoke Live project.

---

## Implementation Steps

### Step 1: Add WebVTT Dependency
**File**: [`requirements.txt`](../requirements.txt)
**Action**: Add `webvtt-py` library for parsing WebVTT files

```txt
webvtt-py==0.4.6
```

**Why**: Provides robust WebVTT parsing with subtitle timing support

---

### Step 2: Create Converter Script
**File**: `tools/webvtt_to_json.py` (new file)
**Action**: Create complete converter with text cleaning and validation

```python
#!/usr/bin/env python3
"""
WebVTT to JSON Lyrics Converter
Converts WebVTT subtitle files to JSON format compatible with LyricDisplay.
"""
import re
import json
import webvtt
from pathlib import Path
from typing import List, Dict, Optional


def clean_vtt_text(text: str) -> Optional[str]:
    """
    Clean WebVTT text by removing formatting tags and special markers.
    
    Args:
        text: Raw VTT caption text
        
    Returns:
        Cleaned text or None if should be skipped
    """
    # Remove word-level timestamps: <00:00:04.600>
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    
    # Remove formatting tags: <c>, </c>
    text = re.sub(r'</?c>', '', text)
    
    # Remove speaker markers: >>
    text = text.replace('>>', '').strip()
    
    # Skip music markers and empty lines
    if text in ['[Música]', '']:
        return None
        
    return text


def merge_duplicate_lines(lines: List[Dict]) -> List[Dict]:
    """
    Merge consecutive lines with identical text.
    
    WebVTT often has duplicate cues for transitions.
    Keep the first occurrence with earliest timing.
    
    Args:
        lines: List of lyric line dictionaries
        
    Returns:
        Deduplicated list of lines
    """
    if not lines:
        return []
    
    merged = []
    prev_text = None
    
    for line in lines:
        current_text = line['text'].strip()
        
        # Skip if same as previous line (duplicate cue)
        if current_text == prev_text:
            continue
            
        merged.append(line)
        prev_text = current_text
    
    return merged


def convert_webvtt_to_json(
    vtt_file: str,
    output_file: str,
    merge_duplicates: bool = True
) -> Dict:
    """
    Convert WebVTT file to JSON lyrics format.
    
    Args:
        vtt_file: Path to .vtt file
        output_file: Path to output .json file
        merge_duplicates: Whether to merge duplicate consecutive lines
        
    Returns:
        Dictionary with conversion results and statistics
    """
    vtt_path = Path(vtt_file)
    output_path = Path(output_file)
    
    if not vtt_path.exists():
        raise FileNotFoundError(f"VTT file not found: {vtt_file}")
    
    # Parse WebVTT file
    print(f"📖 Parsing {vtt_path.name}...")
    captions = webvtt.read(str(vtt_path))
    
    # Convert to lyric lines
    lines = []
    skipped = 0
    
    for caption in captions:
        # Clean the text
        cleaned_text = clean_vtt_text(caption.text)
        
        if cleaned_text is None:
            skipped += 1
            continue
        
        lines.append({
            'start': caption.start_in_seconds,
            'end': caption.end_in_seconds,
            'text': cleaned_text
        })
    
    # Merge duplicates if requested
    original_count = len(lines)
    if merge_duplicates:
        lines = merge_duplicate_lines(lines)
        duplicates_removed = original_count - len(lines)
    else:
        duplicates_removed = 0
    
    # Create output structure
    output_data = {
        'title': vtt_path.stem,
        'artist': 'IBP',
        'audio_file': f'assets/audio/{vtt_path.stem}.wav',
        'duration': lines[-1]['end'] if lines else 0,
        'lines': lines
    }
    
    # Write JSON file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Return statistics
    stats = {
        'input_file': str(vtt_path),
        'output_file': str(output_path),
        'total_captions': len(captions),
        'skipped_markers': skipped,
        'duplicates_removed': duplicates_removed,
        'final_lines': len(lines),
        'duration': output_data['duration']
    }
    
    return stats


def print_stats(stats: Dict):
    """Print conversion statistics."""
    print("\n" + "=" * 50)
    print("✅ Conversion Complete!")
    print("=" * 50)
    print(f"Input:  {stats['input_file']}")
    print(f"Output: {stats['output_file']}")
    print(f"\nStatistics:")
    print(f"  • Total VTT captions: {stats['total_captions']}")
    print(f"  • Markers skipped:    {stats['skipped_markers']}")
    print(f"  • Duplicates removed: {stats['duplicates_removed']}")
    print(f"  • Final lyric lines:  {stats['final_lines']}")
    print(f"  • Song duration:      {stats['duration']:.2f}s")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    # Default conversion
    VTT_FILE = 'assets/lyrics/Ibp - Energia da Revolucao.vtt'
    JSON_FILE = 'data/lyrics.json'
    
    try:
        stats = convert_webvtt_to_json(VTT_FILE, JSON_FILE)
        print_stats(stats)
        
        print("🎵 To use the new lyrics:")
        print("   1. Verify lyrics.json in data/ folder")
        print("   2. Run the app: python main.py")
        print("   3. Test performance screen\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise
```

**Features**:
- Text cleaning (removes VTT tags)
- Duplicate line merging
- Statistics reporting
- Error handling
- UTF-8 encoding support

---

### Step 3: Test Converter
**Command**: Run the converter script

```bash
# Install dependency
pip install webvtt-py

# Run converter
python tools/webvtt_to_json.py
```

**Expected Output**:
```
📖 Parsing Ibp - Energia da Revolucao.vtt...

==================================================
✅ Conversion Complete!
==================================================
Input:  assets/lyrics/Ibp - Energia da Revolucao.vtt
Output: data/lyrics.json

Statistics:
  • Total VTT captions: 52
  • Markers skipped:    2
  • Duplicates removed: 15
  • Final lyric lines:  35
  • Song duration:      61.96s
==================================================
```

---

### Step 4: Validate Generated JSON
**File**: [`data/lyrics.json`](../data/lyrics.json)
**Action**: Verify the JSON structure matches expected format

**Expected Structure**:
```json
{
  "title": "Ibp - Energia da Revolucao",
  "artist": "IBP",
  "audio_file": "assets/audio/Ibp - Energia da Revolucao.wav",
  "duration": 61.96,
  "lines": [
    {
      "start": 4.52,
      "end": 6.51,
      "text": "No tênis que eu calço, no asfalto que eu"
    },
    {
      "start": 6.52,
      "end": 8.629,
      "text": "piso, tá no fone que eu uso, no corre"
    }
    // ... more lines
  ]
}
```

**Validation Checks**:
- ✅ Valid JSON syntax
- ✅ All required fields present
- ✅ Timestamps are sequential (start < end)
- ✅ No empty text fields
- ✅ UTF-8 encoding preserved (Portuguese characters)

---

### Step 5: Integration Test
**File**: [`ui/screens/performance_screen.py`](../ui/screens/performance_screen.py)
**Action**: Test with existing [`LyricDisplay`](../modules/lyric_display.py:37) class

**Test Steps**:
1. Start application: `python main.py`
2. Navigate to Performance Screen
3. Verify lyrics display correctly
4. Check timing synchronization with audio
5. Confirm all lines appear during playback

**Success Criteria**:
- ✅ Lyrics load without errors
- ✅ Text syncs with audio timing
- ✅ Portuguese characters display correctly
- ✅ No missing or duplicate lines
- ✅ Previous/Current/Next context works

---

### Step 6: Create Usage Documentation
**File**: `docs/webvtt-conversion-guide.md` (new file)
**Action**: Document conversion process for future use

**Contents**:
- How to convert new songs
- Troubleshooting common issues
- Manual editing guidelines
- Re-conversion workflow

---

## Files Modified/Created

### New Files
1. ✨ `tools/webvtt_to_json.py` - Converter script
2. ✨ `docs/implementation-plan.md` - This file
3. ✨ `docs/webvtt-conversion-guide.md` - Usage guide

### Modified Files
1. 📝 [`requirements.txt`](../requirements.txt) - Add `webvtt-py`
2. 📝 [`data/lyrics.json`](../data/lyrics.json) - Regenerated from VTT

### Unchanged Files
- ✅ [`modules/lyric_display.py`](../modules/lyric_display.py) - No changes needed
- ✅ [`ui/screens/performance_screen.py`](../ui/screens/performance_screen.py) - No changes needed
- ✅ All other application code

---

## Rollback Plan

If conversion fails or produces incorrect results:

1. **Keep original JSON**: Backup current [`lyrics.json`](../data/lyrics.json)
   ```bash
   cp data/lyrics.json data/lyrics.json.backup
   ```

2. **Revert if needed**: Restore backup
   ```bash
   cp data/lyrics.json.backup data/lyrics.json
   ```

3. **Manual editing**: Edit JSON directly if automatic conversion has issues

---

## Timeline

| Step | Description | Time Estimate |
|------|-------------|---------------|
| 1 | Add dependency | 5 minutes |
| 2 | Create converter script | 30 minutes |
| 3 | Test converter | 10 minutes |
| 4 | Validate JSON output | 10 minutes |
| 5 | Integration testing | 15 minutes |
| 6 | Documentation | 20 minutes |
| **Total** | | **~1.5 hours** |

---

## Quality Checklist

Before considering the task complete:

- [ ] `webvtt-py` added to [`requirements.txt`](../requirements.txt)
- [ ] `tools/webvtt_to_json.py` created and tested
- [ ] [`data/lyrics.json`](../data/lyrics.json) generated successfully
- [ ] JSON structure validated
- [ ] Portuguese characters preserved (no encoding issues)
- [ ] Integration test passed (app runs without errors)
- [ ] Lyrics sync correctly with audio
- [ ] Documentation created
- [ ] Original VTT file preserved in [`assets/lyrics/`](../assets/lyrics/)

---

## Next Actions

After implementation is approved:

1. **Switch to Code Mode** to create the files
2. **Run converter** to generate JSON
3. **Test application** end-to-end
4. **Document results** in project STATUS.md

---

## Notes

- **Performance**: Conversion takes ~100ms for typical song (negligible)
- **Scalability**: Can easily process multiple VTT files (batch conversion)
- **Future**: If word-level highlighting needed, upgrade to Option 3
- **Maintenance**: Re-run converter if lyrics change in VTT file