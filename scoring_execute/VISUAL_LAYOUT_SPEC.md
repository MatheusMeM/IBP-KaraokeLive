# 📐 Visual Layout Specification

## Screen Layout (1920×1080px)

```
┌─────────────────────────────────────────────────────────────────────┐
│ (0, 1080)                                                  (1920, 1080)│
│                                                                      │
│  ╔═══════════════════════════════════════════════════════════════╗ │
│  ║                   CONTENT AREA (70%)                          ║ │
│  ║                   Height: 756px                               ║ │
│  ║                   Y: 324-1080                                 ║ │
│  ╠═══════════════════════════════════════════════════════════════╣ │
│  ║                                                               ║ │
│  ║  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  ║ │
│  ║  ┃  YOUR SCORE: 71                                        ┃  ║ │
│  ║  ┃  Font: 72dp Bold | Color: Gold                         ┃  ║ │
│  ║  ┃  Height: ~151px (14% of screen)                        ┃  ║ │
│  ║  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  ║ │
│  ║                                                               ║ │
│  ║  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  ║ │
│  ║  ┃  ★ ★ ★ ★ ☆                                             ┃  ║ │
│  ║  ┃  Font: 50dp | Color: Gold                              ┃  ║ │
│  ║  ┃  Height: ~113px (10.5% of screen)                      ┃  ║ │
│  ║  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  ║ │
│  ║                                                               ║ │
│  ║  [Spacer: ~108px (10%)]                                       ║ │
│  ║                                                               ║ │
│  ║  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  ║ │
│  ║  ┃  Enter Your Name:                                       ┃  ║ │
│  ║  ┃  Font: 32dp | Color: White                             ┃  ║ │
│  ║  ┃  Height: ~76px (7% of screen)                          ┃  ║ │
│  ║  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  ║ │
│  ║                                                               ║ │
│  ║        ┌─────────────────────────────────────────┐            ║ │
│  ║        │                                         │            ║ │
│  ║        │        NAME APPEARS HERE                │            ║ │
│  ║        │                                         │            ║ │
│  ║        │  Font: 40dp Bold | BG: White            │            ║ │
│  ║        │  Width: 80% | Height: ~151px (14%)      │            ║ │
│  ║        │                                         │            ║ │
│  ║        └─────────────────────────────────────────┘            ║ │
│  ║                                                               ║ │
│  ║  [Spacer: ~54px (5%)]                                         ║ │
│  ║                                                               ║ │
│  ║            ╔════════════════════════════════╗                 ║ │
│  ║            ║     SUBMIT SCORE               ║                 ║ │
│  ║            ║                                ║                 ║ │
│  ║            ║  Font: 36dp Bold               ║                 ║ │
│  ║            ║  BG: Green                     ║                 ║ │
│  ║            ║  Width: 60% | Height: ~151px   ║                 ║ │
│  ║            ║                                ║                 ║ │
│  ║            ╚════════════════════════════════╝                 ║ │
│  ║                                                               ║ │
│  ╚═══════════════════════════════════════════════════════════════╝ │
├─────────────────────────────────────────────────────────────────────┤
│  Y = 324px (30% boundary)                                            │
├─────────────────────────────────────────────────────────────────────┤
│  ╔═══════════════════════════════════════════════════════════════╗ │
│  ║              VIRTUAL KEYBOARD (30%)                           ║ │
│  ║              Height: 324px                                    ║ │
│  ║              Y: 0-324                                         ║ │
│  ╠═══════════════════════════════════════════════════════════════╣ │
│  ║                                                               ║ │
│  ║  ┌───────────────────────────────────────────────────────┐   ║ │
│  ║  │ [1][2][3][4][5][6][7][8][9][0][⌫]                    │   ║ │
│  ║  │ Row Height: ~70px                                     │   ║ │
│  ║  └───────────────────────────────────────────────────────┘   ║ │
│  ║                                                               ║ │
│  ║  ┌───────────────────────────────────────────────────────┐   ║ │
│  ║  │ [Q][W][E][R][T][Y][U][I][O][P]                        │   ║ │
│  ║  │ Row Height: ~70px                                     │   ║ │
│  ║  └───────────────────────────────────────────────────────┘   ║ │
│  ║                                                               ║ │
│  ║  ┌───────────────────────────────────────────────────────┐   ║ │
│  ║  │   [A][S][D][F][G][H][J][K][L]                         │   ║ │
│  ║  │   Row Height: ~70px                                   │   ║ │
│  ║  └───────────────────────────────────────────────────────┘   ║ │
│  ║                                                               ║ │
│  ║  ┌───────────────────────────────────────────────────────┐   ║ │
│  ║  │     [Z][X][C][V][B][N][M][___SPACE___][✓]            │   ║ │
│  ║  │     Row Height: ~70px                                 │   ║ │
│  ║  └───────────────────────────────────────────────────────┘   ║ │
│  ║                                                               ║ │
│  ║  Key Size: ~70px height × ~80px width (each)                 ║ │
│  ║  Spacing: 3px between keys                                   ║ │
│  ║  Padding: 10px (sides), 8px (top/bottom)                     ║ │
│  ║                                                               ║ │
│  ╚═══════════════════════════════════════════════════════════════╝ │
│                                                                      │
│ (0, 0)                                                      (1920, 0) │
└─────────────────────────────────────────────────────────────────────┘

LEGEND:
  ╔═╗ Major section border (70% / 30% division)
  ┏━┓ Widget border
  ┌─┐ Container border
  ║ │ Section padding
```

---

## Component Measurements (1920×1080)

### Content Area (Y: 324-1080, Height: 756px)
```
┌─────────────────────────────────────────────────────┬──────────┬─────────┐
│ Component                                           │ Height   │ % Screen│
├─────────────────────────────────────────────────────┼──────────┼─────────┤
│ Padding Top                                         │  20px    │  1.9%   │
│ Score Label ("YOUR SCORE: 71")                     │ 151px    │ 14.0%   │
│ Stars Label ("★ ★ ★ ★ ☆")                          │ 113px    │ 10.5%   │
│ Spacer                                              │ 108px    │ 10.0%   │
│ Name Label ("Enter Your Name:")                     │  76px    │  7.0%   │
│ Input Display (white box)                           │ 151px    │ 14.0%   │
│ Spacer                                              │  54px    │  5.0%   │
│ Submit Button ("SUBMIT SCORE")                      │ 151px    │ 14.0%   │
│ Padding Bottom                                      │  20px    │  1.9%   │
├─────────────────────────────────────────────────────┼──────────┼─────────┤
│ TOTAL CONTENT AREA                                  │ 756px    │ 70.0%   │
└─────────────────────────────────────────────────────┴──────────┴─────────┘
```

### Keyboard Area (Y: 0-324, Height: 324px)
```
┌─────────────────────────────────────────────────────┬──────────┬─────────┐
│ Component                                           │ Height   │ % Screen│
├─────────────────────────────────────────────────────┼──────────┼─────────┤
│ Padding Top                                         │   8px    │  0.7%   │
│ Keyboard Row 1 (Numbers + Backspace)               │  70px    │  6.5%   │
│ Spacing                                             │   3px    │  0.3%   │
│ Keyboard Row 2 (QWERTY top)                        │  70px    │  6.5%   │
│ Spacing                                             │   3px    │  0.3%   │
│ Keyboard Row 3 (QWERTY middle)                     │  70px    │  6.5%   │
│ Spacing                                             │   3px    │  0.3%   │
│ Keyboard Row 4 (QWERTY bottom + Space + Submit)    │  70px    │  6.5%   │
│ Padding Bottom                                      │   8px    │  0.7%   │
├─────────────────────────────────────────────────────┼──────────┼─────────┤
│ TOTAL KEYBOARD AREA                                 │ 324px    │ 30.0%   │
└─────────────────────────────────────────────────────┴──────────┴─────────┘
```

---

## Touch Target Analysis

### Accessibility Standards
```
Apple Human Interface Guidelines: Minimum 44×44 points
Material Design: Minimum 48×48 dp
Industry Best Practice: 44-48 pixels minimum
```

### Our Implementation
```
┌─────────────────────────────────────────┬───────────┬─────────┬──────────┐
│ Element                                 │ Size      │ Standard│ Status   │
├─────────────────────────────────────────┼───────────┼─────────┼──────────┤
│ Keyboard Keys                           │ 70×80px   │ 44px    │ ✅ PASS  │
│ Submit Button                           │ 151×1152px│ 44px    │ ✅ PASS  │
│ Input Display (clickable for focus)     │ 151×1536px│ 44px    │ ✅ PASS  │
│ Spacebar                                │ 70×160px  │ 44px    │ ✅ PASS  │
│ Submit Key (✓)                          │ 70×80px   │ 44px    │ ✅ PASS  │
└─────────────────────────────────────────┴───────────┴─────────┴──────────┘

All touch targets EXCEED minimum accessibility requirements!
```

---

## Responsive Scaling

### Different Resolutions (maintaining 70/30 ratio)

#### HD (1280×720)
```
Total Height: 720px
├── Content Area: 504px (70%)
│   ├── Score: 100px
│   ├── Stars: 76px
│   ├── Spacer: 72px
│   ├── Label: 50px
│   ├── Input: 100px
│   ├── Spacer: 36px
│   └── Button: 100px
└── Keyboard: 216px (30%)
    └── 4 rows × ~47px each
```

#### FullHD (1920×1080) ← TARGET
```
Total Height: 1080px
├── Content Area: 756px (70%)
│   ├── Score: 151px
│   ├── Stars: 113px
│   ├── Spacer: 108px
│   ├── Label: 76px
│   ├── Input: 151px
│   ├── Spacer: 54px
│   └── Button: 151px
└── Keyboard: 324px (30%)
    └── 4 rows × ~70px each
```

#### 2K (2560×1440)
```
Total Height: 1440px
├── Content Area: 1008px (70%)
│   ├── Score: 201px
│   ├── Stars: 151px
│   ├── Spacer: 144px
│   ├── Label: 101px
│   ├── Input: 201px
│   ├── Spacer: 72px
│   └── Button: 201px
└── Keyboard: 432px (30%)
    └── 4 rows × ~93px each
```

---

## Color Specifications (with Hex Codes)

```
BACKGROUND COLORS
┌────────────────────────────────┬──────────────┬────────────────┐
│ Element                        │ RGBA         │ Hex Code       │
├────────────────────────────────┼──────────────┼────────────────┤
│ Screen Background              │ (0.05, 0.05, │ #0C0C19        │
│                                │  0.1, 1)     │                │
│ Keyboard Background            │ (0.15, 0.15, │ #262626        │
│                                │  0.15, 1)    │                │
│ Input Display Background       │ (1, 1, 1, 1) │ #FFFFFF        │
└────────────────────────────────┴──────────────┴────────────────┘

TEXT COLORS
┌────────────────────────────────┬──────────────┬────────────────┐
│ Element                        │ RGBA         │ Hex Code       │
├────────────────────────────────┼──────────────┼────────────────┤
│ Score Label (Gold)             │ (1, 0.84, 0, │ #FFD700        │
│                                │  1)          │                │
│ Stars (Gold)                   │ (1, 0.84, 0, │ #FFD700        │
│                                │  1)          │                │
│ Name Label (White)             │ (1, 1, 1, 1) │ #FFFFFF        │
│ Input Text (Black)             │ (0, 0, 0, 1) │ #000000        │
│ Keyboard Text (White)          │ (1, 1, 1, 1) │ #FFFFFF        │
└────────────────────────────────┴──────────────┴────────────────┘

BUTTON COLORS
┌────────────────────────────────┬──────────────┬────────────────┐
│ Element                        │ RGBA         │ Hex Code       │
├────────────────────────────────┼──────────────┼────────────────┤
│ Submit Button (Green)          │ (0.2, 0.7,   │ #33B34D        │
│                                │  0.3, 1)     │                │
│ Submit Key ✓ (Green)           │ (0.2, 0.5,   │ #338052        │
│                                │  0.3, 1)     │                │
│ Backspace ⌫ (Red)              │ (0.6, 0.2,   │ #993333        │
│                                │  0.2, 1)     │                │
│ Regular Keys (Gray)            │ (0.3, 0.3,   │ #4D4D4D        │
│                                │  0.3, 1)     │                │
└────────────────────────────────┴──────────────┴────────────────┘
```

---

## Typography Scale

```
FONT SIZES (using dp for proper DPI scaling)
┌────────────────────────────────┬──────────┬────────────┬────────┐
│ Element                        │ Size (dp)│ Weight     │ Color  │
├────────────────────────────────┼──────────┼────────────┼────────┤
│ Score Label                    │    72    │ Bold       │ Gold   │
│ Stars Label                    │    50    │ Regular    │ Gold   │
│ Name Label                     │    32    │ Regular    │ White  │
│ Input Display                  │    40    │ Bold       │ Black  │
│ Submit Button                  │    36    │ Bold       │ White  │
│ Keyboard Keys                  │    24    │ Bold       │ White  │
│ Spacebar Label                 │    16    │ Regular    │ White  │
└────────────────────────────────┴──────────┴────────────┴────────┘

Font Family: System default (Kivy default)
Alternative: 'Roboto' (if available in project)
```

---

## Z-Index / Stacking Order

```
TOP (visible on top)
    ↑
    │ 3. Content Area (BoxLayout)
    │    └── All content widgets
    │
    │ 2. Keyboard (CompactVirtualKeyboard)
    │    └── Always on top of background
    │    └── But below content area
    │
    │ 1. Background (Rectangle)
    │    └── Covers entire screen
    ↓
BOTTOM (behind everything)

Note: Z-index is determined by order of add_widget() calls.
Add background first, keyboard second, content last.
```

---

## Grid Layout Coordinates

```
FloatLayout Coordinate System (Origin: bottom-left)
┌─────────────────────────────────────────────────────────────┐
│ (0, 1)                                              (1, 1)  │
│  Top-Left                                        Top-Right  │
│                                                              │
│                                                              │
│                      CONTENT AREA                           │
│                  pos_hint={'x': 0, 'y': 0.30}               │
│                  size_hint=(1, 0.70)                        │
│                                                              │
│                                                              │
├──────────────────────────────────────────────────────────────┤ Y = 0.30
│                                                              │
│                      KEYBOARD AREA                          │
│                  pos_hint={'x': 0, 'y': 0}                  │
│                  size_hint=(1, 0.30)                        │
│                                                              │
│ (0, 0)                                              (1, 0)  │
│  Bottom-Left                                   Bottom-Right │
└─────────────────────────────────────────────────────────────┘

Key Positioning Values:
• x: 0 to 1 (left to right)
• y: 0 to 1 (bottom to top)
• Keyboard: y=0 (bottom)
• Content: y=0.30 (starts 30% from bottom)
• Boundary: y=0.30 (dividing line)
```

---

## Implementation Measurements Summary

### Quick Reference Card
```
╔════════════════════════════════════════════════════════════════╗
║                    QUICK MEASUREMENTS                          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Screen: 1920×1080px (target)                                 ║
║                                                                ║
║  Keyboard:                                                     ║
║    • Height: 30% (324px)                                      ║
║    • Position: y=0 to y=0.30                                  ║
║    • Rows: 4 × ~70px each                                     ║
║    • Key size: ~70×80px                                       ║
║                                                                ║
║  Content:                                                      ║
║    • Height: 70% (756px)                                      ║
║    • Position: y=0.30 to y=1.0                                ║
║    • Score: 14% (151px, 72dp font)                            ║
║    • Stars: 10.5% (113px, 50dp font)                          ║
║    • Input: 14% (151px, 40dp font)                            ║
║    • Button: 14% (151px, 36dp font)                           ║
║                                                                ║
║  Colors:                                                       ║
║    • Background: #0C0C19                                      ║
║    • Gold: #FFD700                                            ║
║    • Green: #33B34D                                           ║
║    • White: #FFFFFF                                           ║
║                                                                ║
║  Touch Targets: ALL > 70px (EXCELLENT)                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

*This specification ensures pixel-perfect implementation across different screen sizes while maintaining the 70/30 content-to-keyboard ratio.*
