# WebVTT to JSON Integration Strategy

## WebVTT Analysis

### Current WebVTT Format Characteristics
- **Timing Format**: `HH:MM:SS.mmm --> HH:MM:SS.mmm`
- **Word-level Timestamps**: `<00:00:04.600><c> word</c>` for karaoke-style highlighting
- **Positioning Metadata**: `align:start position:0%`
- **Special Markers**: `[Música]`, `>>` speaker tags
- **Duplicate Lines**: Transition cues with empty or repeated text
- **Language**: Portuguese (`pt`)

### Current JSON Format
```json
{
  "start": 0.0,
  "end": 3.5,
  "text": "Lyric line"
}
```

---

## Strategy Alternatives

### Option 1: Direct Parse & Convert (One-time Conversion)

**Description**: Create a Python script that parses WebVTT and generates [`data/lyrics.json`](data/lyrics.json)

**Implementation**:
```python
# tools/webvtt_converter.py
import webvtt
import json

def convert_webvtt_to_json(vtt_file, json_file):
    captions = webvtt.read(vtt_file)
    lines = []
    
    for caption in captions:
        # Skip empty or music markers
        if caption.text.strip() in ['', '[Música]']:
            continue
            
        lines.append({
            'start': caption.start_in_seconds,
            'end': caption.end_in_seconds,
            'text': clean_text(caption.text)
        })
    
    return lines
```

**Pros**:
- ✅ Simple, one-time conversion
- ✅ Reuses existing [`LyricDisplay`](modules/lyric_display.py:37) class (no code changes)
- ✅ Small JSON output (~2-5KB)
- ✅ Fast runtime performance
- ✅ No new dependencies in production

**Cons**:
- ❌ Manual re-conversion if lyrics change
- ❌ Loses word-level timing data (karaoke highlighting)
- ❌ Requires python-webvtt library (dev dependency)
- ❌ Two sources of truth (VTT + JSON)

**Cost**: **⭐ LOW** - One-time dev effort, no runtime overhead

---

### Option 2: Runtime WebVTT Parser

**Description**: Modify [`LyricDisplay`](modules/lyric_display.py:37) to read WebVTT directly

**Implementation**:
```python
# modules/lyric_display.py
import webvtt

class LyricDisplay:
    def _load_webvtt(self):
        captions = webvtt.read(self.lyrics_file)
        for caption in captions:
            self.lines.append(LyricLine(
                start=caption.start_in_seconds,
                end=caption.end_in_seconds,
                text=self._clean_text(caption.text)
            ))
```

**Pros**:
- ✅ Single source of truth (VTT only)
- ✅ No manual conversion needed
- ✅ WebVTT is industry standard format
- ✅ Future-proof (video subtitles compatibility)

**Cons**:
- ❌ New runtime dependency (python-webvtt ~50KB)
- ❌ Slower parsing at startup (~10-50ms)
- ❌ More complex error handling
- ❌ Still loses word-level timing

**Cost**: **⭐⭐ MEDIUM** - Adds dependency, minimal runtime cost

---

### Option 3: Enhanced JSON with Word Timestamps

**Description**: Convert WebVTT to JSON but preserve word-level timing for karaoke highlighting

**Implementation**:
```python
# Enhanced JSON format
{
  "start": 4.52,
  "end": 6.51,
  "text": "No tênis que eu calço, no asfalto que eu",
  "words": [
    {"start": 4.52, "end": 4.6, "text": "No"},
    {"start": 4.6, "end": 4.96, "text": "tênis"},
    {"start": 4.96, "end": 5.08, "text": "que"},
    // ...
  ]
}
```

**Pros**:
- ✅ Enables karaoke-style word highlighting
- ✅ Professional karaoke experience
- ✅ Fast runtime (JSON parsing)
- ✅ Flexible format for future features

**Cons**:
- ❌ Complex conversion script
- ❌ Larger JSON files (~10-20KB)
- ❌ Requires UI changes for word highlighting
- ❌ More complex [`LyricDisplay`](modules/lyric_display.py:37) logic

**Cost**: **⭐⭐⭐ HIGH** - Complex conversion + UI implementation

---

### Option 4: Hybrid Approach (VTT for Archive, JSON for Runtime)

**Description**: Keep VTT as master source, auto-generate JSON during build/deployment

**Implementation**:
```python
# tools/build_lyrics.py (run during deployment)
# Converts all .vtt files to .json automatically

# Option to run manually or via pre-commit hook
```

**Pros**:
- ✅ VTT as canonical source (versioned)
- ✅ JSON optimized for runtime
- ✅ Automated workflow
- ✅ Best of both worlds

**Cons**:
- ❌ Build step complexity
- ❌ Requires CI/CD integration
- ❌ Two file formats to maintain

**Cost**: **⭐⭐ MEDIUM** - Setup effort, minimal maintenance

---

### Option 5: Keep Current JSON (Manual Sync)

**Description**: Continue using current JSON format, manually sync from VTT when needed

**Pros**:
- ✅ Zero development cost
- ✅ No code changes
- ✅ Proven working solution

**Cons**:
- ❌ Error-prone manual process
- ❌ Potential sync issues
- ❌ Time-consuming for updates

**Cost**: **⭐ LOWEST** - No development, high maintenance

---

## Comparison Matrix

| Strategy | Dev Cost | Runtime Cost | Maintenance | Features | **Total Score** |
|----------|----------|--------------|-------------|----------|-----------------|
| **Option 1: One-time Convert** | Low | None | Medium | Basic | **⭐⭐⭐⭐ BEST** |
| Option 2: Runtime Parser | Medium | Low | Low | Basic | ⭐⭐⭐ |
| Option 3: Enhanced JSON | High | Low | Low | Advanced | ⭐⭐ |
| Option 4: Hybrid Build | Medium | None | Medium | Basic | ⭐⭐⭐ |
| Option 5: Manual Sync | None | None | High | Basic | ⭐⭐ |

---

## Recommended Approach

### 🏆 **OPTION 1: Direct Parse & Convert**

**Rationale**:
1. **Cost-Effective**: Minimal development (~2 hours), zero runtime overhead
2. **Simple**: Leverages existing [`LyricDisplay`](modules/lyric_display.py:37) infrastructure
3. **Proven**: JSON format already tested and working
4. **Practical**: For a karaoke event, lyrics rarely change after finalization
5. **Scalable**: Easy to add more songs by running converter script

**Implementation Steps**:
1. Create `tools/webvtt_to_json.py` converter script
2. Parse WebVTT, clean text, merge duplicate lines
3. Generate optimized JSON matching current format
4. Validate against existing [`LyricDisplay`](modules/lyric_display.py:37)
5. Document conversion process

**When to Reconsider**:
- If lyrics change frequently → Switch to **Option 4 (Hybrid)**
- If word-level highlighting needed → Upgrade to **Option 3 (Enhanced)**
- If many songs added regularly → Consider **Option 2 (Runtime Parser)**

---

## WebVTT Parsing Challenges

### Issues to Handle:
1. **Duplicate Cue Lines**: Multiple cues with same text at different times
   - **Solution**: Merge consecutive duplicates, keep only first occurrence
   
2. **Empty Cues**: Transition markers with no text
   - **Solution**: Skip during parsing

3. **Special Markers**: `[Música]`, `>>`
   - **Solution**: Filter out or map to metadata

4. **Word-level Tags**: `<00:00:04.600><c> word</c>`
   - **Solution**: Strip tags for basic version, parse for enhanced version

5. **Line Continuations**: Text that spans multiple cues
   - **Solution**: Detect and merge based on timing overlap

### Cleaning Algorithm:
```python
def clean_vtt_text(text):
    # Remove word-level timestamps
    text = re.sub(r'<\d+:\d+:\d+\.\d+>', '', text)
    # Remove formatting tags
    text = re.sub(r'</?c>', '', text)
    # Remove speaker markers
    text = text.replace('>>', '').strip()
    # Filter special markers
    if text in ['[Música]', '']:
        return None
    return text
```

---

## Next Steps

1. ✅ **Approve Strategy**: Confirm Option 1 as chosen approach
2. Create converter script (`tools/webvtt_to_json.py`)
3. Test conversion on sample VTT file
4. Generate new [`data/lyrics.json`](data/lyrics.json)
5. Validate with existing [`LyricDisplay`](modules/lyric_display.py:37) implementation
6. Document usage in README

**Estimated Time**: 2-3 hours total
**Risk Level**: Low (no production code changes)