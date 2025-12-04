#!/usr/bin/env python3
"""Test colorgram extraction"""

import colorgram

# Extract colors
colors = colorgram.extract("examples/test-wallpaper.jpg", 8)

print("🎨 colorgram.py Results:")
print(f"Extracted {len(colors)} colors:\n")

for i, color in enumerate(colors):
    rgb = color.rgb
    hex_color = f"#{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}"
    print(f"{i+1}. {hex_color}  RGB({rgb.r}, {rgb.g}, {rgb.b})  (proportion: {color.proportion:.3f})")
