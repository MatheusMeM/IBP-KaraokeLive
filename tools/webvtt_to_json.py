#!/usr/bin/env python3
"""
WebVTT to JSON Lyrics Converter - VERSÃO PARA PROJETO
Preserva timestamps exatos e funciona com paths relativos.
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def parse_timestamp(timestamp_str: str) -> float:
    """
    Parse timestamp string to seconds with millisecond precision.
    
    Formato: HH:MM:SS.mmm
    Exemplo: 00:00:04.520 → 4.520
    """
    timestamp_str = timestamp_str.strip()
    match = re.match(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})', timestamp_str)
    
    if not match:
        raise ValueError(f"Invalid timestamp: {timestamp_str}")
    
    hours, minutes, seconds, milliseconds = match.groups()
    
    total_seconds = (
        int(hours) * 3600 +
        int(minutes) * 60 +
        int(seconds) +
        int(milliseconds) / 1000
    )
    
    return round(total_seconds, 3)


def parse_timestamp_line(line: str) -> Optional[Tuple[float, float]]:
    """
    Parse a VTT timestamp line.
    
    Args:
        line: Line like "00:00:04.520 --> 00:00:06.752"
    
    Returns:
        Tuple of (start_seconds, end_seconds) or None if not a timestamp line
    """
    pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})'
    match = re.match(pattern, line.strip())
    
    if not match:
        return None
    
    start_str, end_str = match.groups()
    start_time = parse_timestamp(start_str)
    end_time = parse_timestamp(end_str)
    
    return (start_time, end_time)


def clean_text(text: str) -> Optional[str]:
    """Clean and validate lyric text."""
    # Remove word-level timestamps
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    
    # Remove formatting tags
    text = re.sub(r'</?c[^>]*>', '', text)
    
    # Remove speaker markers at start
    text = re.sub(r'^>>\s*', '', text)
    
    # Clean whitespace
    text = ' '.join(text.split())
    text = text.strip()
    
    # Skip empty or music-only markers
    if not text or text in ['[Música]', '[MÃºsica]', '♪']:
        return None
    
    return text


def parse_vtt_robust(vtt_file: str) -> List[Dict]:
    """
    Parse VTT file robustly, line by line.
    """
    with open(vtt_file, 'r', encoding='utf-8-sig') as f:
        lines_raw = f.readlines()
    
    lyrics = []
    i = 0
    
    while i < len(lines_raw):
        line = lines_raw[i].strip()
        
        # Try to parse as timestamp line
        timestamps = parse_timestamp_line(line)
        
        if timestamps:
            start_time, end_time = timestamps
            
            # Collect text lines until empty line or next timestamp
            text_lines = []
            i += 1
            
            while i < len(lines_raw):
                next_line = lines_raw[i].strip()
                
                # Stop at empty line or next timestamp
                if not next_line or parse_timestamp_line(next_line):
                    break
                
                text_lines.append(next_line)
                i += 1
            
            # Join and clean text
            full_text = ' '.join(text_lines)
            cleaned = clean_text(full_text)
            
            # Only add if we have valid text
            if cleaned:
                lyrics.append({
                    'start': start_time,
                    'end': end_time,
                    'text': cleaned
                })
        else:
            i += 1
    
    return lyrics


def convert_vtt_to_json(vtt_file: str, output_file: str) -> Dict:
    """Convert VTT to JSON with precise timestamps."""
    vtt_path = Path(vtt_file)
    output_path = Path(output_file)
    
    if not vtt_path.exists():
        raise FileNotFoundError(f"VTT file not found: {vtt_file}")
    
    print(f"📖 Parsing {vtt_path.name}...")
    
    lyrics = parse_vtt_robust(str(vtt_path))
    
    if not lyrics:
        raise ValueError("No valid lyrics found")
    
    # Create output
    output_data = {
        'title': vtt_path.stem.replace('_', ' ').replace(' - ', ' - '),
        'artist': 'IBP',
        'audio_file': f'assets/audio/{vtt_path.stem}.wav',
        'duration': lyrics[-1]['end'],
        'lines': lyrics
    }
    
    # Write JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Stats
    return {
        'input_file': str(vtt_path),
        'output_file': str(output_path),
        'total_lines': len(lyrics),
        'duration': output_data['duration'],
        'first_start': lyrics[0]['start'],
        'last_end': lyrics[-1]['end']
    }


def print_stats(stats: Dict):
    """Print conversion statistics."""
    print("\n" + "=" * 60)
    print("✅ CONVERSÃO COMPLETA - TIMESTAMPS PRECISOS!")
    print("=" * 60)
    print(f"Input:  {stats['input_file']}")
    print(f"Output: {stats['output_file']}")
    print(f"\nEstatísticas:")
    print(f"  • Total de linhas:     {stats['total_lines']}")
    print(f"  • Duração da música:   {stats['duration']:.3f}s")
    print(f"  • Primeira linha:      {stats['first_start']:.3f}s")
    print(f"  • Última linha:        {stats['last_end']:.3f}s")
    print("=" * 60)


def show_sample(output_file: str, n: int = 5):
    """Show sample of converted lyrics."""
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n📝 Amostra ({n} primeiras linhas com precisão de ms):\n")
    
    for i, line in enumerate(data['lines'][:n], 1):
        duration = line['end'] - line['start']
        print(f"{i}. [{line['start']:.3f}s → {line['end']:.3f}s] ({duration:.3f}s)")
        text_preview = line['text'][:70] + '...' if len(line['text']) > 70 else line['text']
        print(f"   \"{text_preview}\"")
        print()
    
    print("=" * 60 + "\n")


if __name__ == '__main__':
    # Paths relativos ao projeto
    VTT_FILE = 'assets/lyrics/Ibp - Energia da Revolucao.vtt'
    JSON_FILE = 'data/lyrics.json'
    
    print("=" * 60)
    print("🎵 WebVTT → JSON - PARSER ROBUSTO")
    print("=" * 60)
    print("\n✨ Funcionalidades:")
    print("  • Parsing linha por linha (100% preciso)")
    print("  • Pula blocos vazios automaticamente")
    print("  • Preserva milissegundos (ex: 4.520s)")
    print("  • Não arredonda timestamps")
    print("  • Sincronização perfeita com áudio")
    print("\n" + "─" * 60 + "\n")
    
    try:
        stats = convert_vtt_to_json(VTT_FILE, JSON_FILE)
        print_stats(stats)
        show_sample(JSON_FILE, n=5)
        
        print("🎯 Próximos passos:")
        print("   1. Testar no app: python main.py")
        print("   2. Verificar sincronização das letras")
        print("   3. Conferir que aparecem no momento certo")
        print()
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Certifique-se de executar a partir da raiz do projeto:")
        print("   cd C:\\Users\\MNDS\\Documents\\GitHub\\IBP-KaraokeLive")
        print("   python tools/webvtt_to_json.py")
        print()
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()