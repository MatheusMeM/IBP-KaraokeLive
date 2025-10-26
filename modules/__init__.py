"""
Core modules package for IBP-KaraokeLive.

This package contains the core business logic for the karaoke application,
separated into distinct modules following separation of concerns principles:

- audio_player: Audio playback operations (play, stop, position tracking)
- audio_router: Audio output routing configuration (headphone vs speakers)
- lyric_display: Lyric synchronization and text retrieval

Each module has a single, well-defined responsibility and operates
independently of the others.
"""