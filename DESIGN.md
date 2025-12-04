# 🎨 Faelight Theme Engine - Design Document

**Version:** 0.1.0  
**Phase:** v2.8.1 Phase 1B Research  
**Date:** December 2025  
**Author:** Christian

---

## Overview

Faelight Theme Engine is a standalone Python package that generates beautiful, accessible color themes from wallpapers. It extracts dominant colors, generates 16-color ANSI palettes, validates contrast ratios, and renders configuration templates.

**Design Philosophy:**
- Standalone and reusable (not tied to dotfiles)
- Accessibility first (WCAG AAA compliance)
- Simple CLI interface
- Template-based rendering (Jinja2)

---

## Architecture
```
Wallpaper (JPG/PNG)
    ↓
Color Extraction (colorgram.py)
    ↓
Palette Generation (16-color ANSI)
    ↓
Contrast Validation (WCAG AAA)
    ↓
Template Rendering (Jinja2)
    ↓
Configuration Files (kitty, waybar, hyprland, etc.)
```

---

## Library Selection

### Color Extraction: colorgram.py ✅

**Why colorgram.py over colorz:**

**Pros:**
- Accurate color extraction with proportions
- Shows actual image color distribution
- Simpler API
- Better maintained
- We can boost saturation if needed

**Cons:**
- May need to filter very dark backgrounds
- Less vibrant by default (but that's more honest!)

**Decision:** Use colorgram.py as primary extraction library.

**Implementation:**
```python
import colorgram

colors = colorgram.extract(image_path, 8)
# Returns list of Color objects with:
# - color.rgb (r, g, b values)
# - color.proportion (0.0-1.0)
```

---

## Palette Structure

### JSON Format:
```json
{
  "source": "/path/to/wallpaper.jpg",
  "timestamp": "2025-12-03T12:00:00Z",
  "theme": "dark",
  "background": "#191c37",
  "foreground": "#e8f0f5",
  "accent": "#71b4a0",
  "colors": {
    "color0":  "#191c37",
    "color1":  "#ca7f99",
    "color2":  "#71b4a0",
    "color3":  "#f5d08a",
    "color4":  "#466377",
    "color5":  "#6f4a68",
    "color6":  "#5a968f",
    "color7":  "#c0c5ce",
    "color8":  "#65737e",
    "color9":  "#ef9faf",
    "color10": "#91d4c0",
    "color11": "#fff5aa",
    "color12": "#6683a7",
    "color13": "#8f6a88",
    "color14": "#7ab6af",
    "color15": "#eff1f5"
  },
  "metadata": {
    "contrast_bg_fg": 10.5,
    "contrast_bg_accent": 4.8,
    "extracted_colors": 8,
    "validation": "passed"
  }
}
```

---

## Algorithm Design

### Phase 1: Color Extraction
```python
def extract_colors(image_path: str, num_colors: int = 8) -> list:
    """
    Extract dominant colors from wallpaper.
    
    Steps:
    1. Load image with colorgram
    2. Extract N colors (default 8)
    3. Return RGB tuples with proportions
    """
    colors = colorgram.extract(image_path, num_colors)
    return [(c.rgb.r, c.rgb.g, c.rgb.b, c.proportion) for c in colors]
```

### Phase 2: Theme Detection
```python
def detect_theme(colors: list) -> str:
    """
    Detect if theme should be dark or light.
    
    Algorithm:
    1. Calculate average brightness of all colors
    2. If avg < 128: dark theme
    3. If avg >= 128: light theme
    """
    avg_brightness = sum(
        0.299*r + 0.587*g + 0.114*b 
        for r,g,b,_ in colors
    ) / len(colors)
    
    return "dark" if avg_brightness < 128 else "light"
```

### Phase 3: Palette Generation
```python
def generate_palette(colors: list, theme: str) -> dict:
    """
    Generate 16-color ANSI palette.
    
    Algorithm:
    1. Sort colors by brightness
    2. Select background and foreground:
       - Dark theme: darkest → bg, lightest → fg
       - Light theme: lightest → bg, darkest → fg
    3. Map remaining colors to ANSI roles by hue:
       - Convert to HSV color space
       - Find closest hue for red, green, yellow, blue, magenta, cyan
    4. Generate bright variants:
       - Increase lightness by 20-30%
       - Maintain hue and saturation
    5. Ensure color0 = background, color15 = white variant
    """
```

**Hue Mapping:**
```
Red:     0° ± 30°   → color1
Yellow:  60° ± 30°  → color3
Green:   120° ± 30° → color2
Cyan:    180° ± 30° → color6
Blue:    240° ± 30° → color4
Magenta: 300° ± 30° → color5
```

### Phase 4: Contrast Validation
```python
def validate_contrast(palette: dict) -> dict:
    """
    Validate WCAG contrast ratios.
    
    Requirements:
    - Background vs Foreground: >= 7:1 (AAA)
    - Background vs Accent colors: >= 4.5:1 (AA)
    
    Formula:
    contrast_ratio = (L1 + 0.05) / (L2 + 0.05)
    Where L = relative luminance
    
    If validation fails:
    - Auto-adjust colors (lighten or darken)
    - Retry validation
    - Max 3 adjustment iterations
    """
```

**Relative Luminance Calculation:**
```python
def relative_luminance(rgb: tuple) -> float:
    """
    Calculate relative luminance (WCAG formula).
    
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    Where R, G, B are gamma-corrected values
    """
```

---

## CLI Interface Design

### Commands:
```bash
# Extract and generate palette
faelight-theme extract <image> [--output FILE]

# Render template
faelight-theme render <palette.json> --target <kitty|waybar|hyprland>
faelight-theme render <palette.json> --all --output-dir <dir>

# Validate palette
faelight-theme validate <palette.json>

# Preview palette (terminal colors)
faelight-theme preview <palette.json>

# List available templates
faelight-theme list-templates
```

### Options:
```bash
--preset <vibrant|muted|pastel>  # Saturation adjustment
--theme <dark|light|auto>        # Force theme type
--num-colors <N>                 # Number of colors to extract
```

---

## Implementation Plan

### v2.8.2: Color Extraction
- Implement extract_colors()
- Implement detect_theme()
- Implement generate_palette()
  - RGB to HSV conversion
  - Hue-based color mapping
  - Bright variant generation
- Implement contrast_ratio()
- Implement validate_palette()
- CLI: extract command
- CLI: validate command
- Unit tests

### v2.8.3: Template Rendering
- Create Jinja2 templates (kitty, waybar, hyprland, mako)
- Implement render_template()
- Implement render_all()
- CLI: render command
- CLI: list-templates command
- CLI: preview command
- Unit tests

### v2.8.4: FCM Integration
- Create theme-from-wallpaper.sh in dotfiles
- Create atomic wallpaper packages
- Integrate with Stow
- Application reload logic
- Documentation

---

## Example Workflow
```bash
# User runs (v2.8.4+):
theme-from-wallpaper.sh ~/wallpaper.jpg

# Behind the scenes:
# 1. Extract colors
palette=$(faelight-theme extract ~/wallpaper.jpg)

# 2. Render configs
faelight-theme render palette.json --all --output-dir /tmp/generated

# 3. Copy to dotfiles atomic packages
cp /tmp/generated/kitty.conf ~/dotfiles/kitty-theme-wallpaper/...

# 4. Apply with Stow
cd ~/dotfiles
stow kitty-theme-wallpaper
stow waybar-theme-wallpaper

# 5. Reload apps
hyprctl reload
killall -SIGUSR1 kitty
```

---

## Edge Cases & Considerations

### Dark/Black Wallpapers:
- May extract all very dark colors
- Solution: Boost brightness/saturation if avg < threshold
- Fallback: Use complementary colors

### Light/White Wallpapers:
- May extract all very light colors
- Solution: Darken colors if needed for contrast
- Ensure foreground is dark enough

### Monochrome/Grayscale:
- May not have enough color variety
- Solution: Generate colors from single hue
- Use different saturations/brightness levels

### Gradient Wallpapers:
- May extract similar colors
- Solution: Increase color distance threshold
- Filter colors too similar (delta E < threshold)

---

## Success Criteria

**v2.8.2 Complete When:**
- ✅ Extracts 8 colors from any wallpaper
- ✅ Generates valid 16-color ANSI palette
- ✅ All contrast ratios meet WCAG AAA
- ✅ CLI commands work (extract, validate)
- ✅ Unit tests pass (>80% coverage)

**v2.8.3 Complete When:**
- ✅ All templates render correctly
- ✅ Generated configs are syntactically valid
- ✅ CLI commands work (render, list, preview)
- ✅ Templates tested with multiple palettes

**v2.8.4 Complete When:**
- ✅ theme-from-wallpaper.sh works end-to-end
- ✅ All applications reload correctly
- ✅ Theme persists across reboots
- ✅ Integration with existing theme system

---

## References

- **pywal:** https://github.com/dylanaraps/pywal
- **colorgram.py:** https://github.com/obskyr/colorgram.py
- **WCAG Contrast:** https://webaim.org/resources/contrastchecker/
- **ANSI Colors:** https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

---

**Design Status:** ✅ Complete  
**Next Phase:** v2.8.2 Implementation  
**Estimated Time:** 4-5 hours
