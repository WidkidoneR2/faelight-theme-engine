# Phase 1B Research Notes

## pywal Analysis

**Repository:** https://github.com/dylanaraps/pywal  
**Version:** 3.1.0 (2018)

### How it works:
- Supports 5 different color extraction backends
- Generates 16-color ANSI palette
- Supports both light and dark schemes
- Real-time updates to terminals
- Doesn't modify original configs (generates separate files)

### Color Extraction Backends:
1. **pywal (default)** - Built-in extraction
2. **colorz** - https://github.com/metakirby5/colorz (kmeans clustering)
3. **colorthief** - https://github.com/fengsp/color-thief-py
4. **haishoku** - https://github.com/LanceGin/haishoku
5. **schemer2** - https://github.com/thefryscorer/schemer2

### Features I like:
- Multiple backend support (flexibility!)
- Light/dark scheme support
- Saturation adjustment (--saturate 0.0-1.0)
- Non-invasive (doesn't touch original configs

## Color Extraction Library Testing

**Test Image:** Omarchy rainy night wallpaper (pixel art aesthetic)

### colorz Results:
```
1. #69aaa4 (teal)
2. #5381a9 (blue)
3. #3858aa (blue)
4. #5852aa (purple)
5. #8563aa (purple)
6. #a897a4 (mauve)
7. #af6193 (pink)
8. #af3657 (red)
```

**Pros:**
- Vibrant, saturated colors
- Good for themes that need pop
- Ignores dark backgrounds

**Cons:**
- Colors feel "normalized"
- May not represent actual image

---

### colorgram.py Results:
```
1. #191c37 (dark blue - 51.8% of image!)
2. #466377 (blue-grey - 21.2%)
3. #2b172b (dark purple - 6.4%)
4. #6f4a68 (purple - 6.1%)
5. #71b4a0 (teal - 6.0%)
6. #383458 (dark purple - 3.7%)
7. #5a968f (teal - 2.8%)
8. #ca7f99 (pink - 1.9%)
```

**Pros:**
- Accurate color representation
- Shows proportions (useful!)
- Includes actual background colors
- More realistic extraction

**Cons:**
- May need to filter dark backgrounds
- Less vibrant by default

---

### Initial Decision:
**colorgram.py** seems better because:
1. ✅ More accurate extraction
2. ✅ Proportion data (we can use this!)
3. ✅ We can filter/brighten colors if needed
4. ✅ Better for generating realistic themes

We can always add saturation boost later (like pywal's --saturate flag).

## Color Theory & WCAG

### Contrast Ratio Standards:
- **Level AA:** 4.5:1 minimum (normal text)
- **Level AAA:** 7:1 minimum (enhanced - our goal!)
- **Large Text:** 3:1 minimum

**Formula:** (L1 + 0.05) / (L2 + 0.05)
Where L = relative luminance (weighted RGB)

**Key Insight:** Background vs Foreground needs 7:1 minimum for AAA.

---

### ANSI 16-Color Mapping Strategy:

**Structure:**
```
0-7:   Normal colors (black, red, green, yellow, blue, magenta, cyan, white)
8-15:  Bright variants
```

**Mapping Approach:**
1. Darkest color → background (or lightest for light themes)
2. Highest contrast → foreground
3. Map remaining by hue:
   - Find closest red, green, yellow, blue, magenta, cyan
   - Use HSV hue angle for matching
4. Generate bright variants (increase lightness by 20-30%)

**Algorithm Plan:**
1. Extract 8 colors with colorgram.py
2. Sort by brightness
3. Select background (darkest) and foreground (lightest with contrast check)
4. Map remaining 6 colors to ANSI roles by hue
5. Generate bright variants
6. Validate all contrast ratios
7. Auto-adjust if needed
