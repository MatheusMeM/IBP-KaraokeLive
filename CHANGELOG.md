## [Unreleased]

### Added
- Fake scoring system with realistic RMS simulation for demo purposes (no microphone required)
- Audio routing between headphone and speaker outputs
- Virtual keyboard support for touchscreen-only kiosks
- Keyboard height configuration (270px/25% of screen to prevent UI blocking)
- ASCII-only input filter to prevent emoji entry in name fields

### Fixed
- **CRITICAL:** Crash when typing on virtual keyboard - `input_filter` parameter must be a callable function, not a string (changed to lambda function)
- RuntimeWarning in audio_analyzer.py sqrt calculation - converted to float64 to prevent int16 overflow and added NaN/Inf validation
- Leaderboard not displaying entries - added _populate_grid() method to create Label widgets from data
- Virtual keyboard blocking submit button and text input field

### Changed
- Refactored score calculation for better performance
- Configured Kivy keyboard mode to 'dock' for touchscreen compatibility
- Enhanced TextInput with keyboard_suggestions=False and input_filter='ascii'