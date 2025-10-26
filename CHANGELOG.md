## [Unreleased]

### Added
- Fake scoring system with realistic RMS simulation for demo purposes (no microphone required)
- Audio routing between headphone and speaker outputs

### Fixed
- RuntimeWarning in audio_analyzer.py sqrt calculation - converted to float64 to prevent int16 overflow and added NaN/Inf validation

### Changed
- Refactored score calculation for better performance