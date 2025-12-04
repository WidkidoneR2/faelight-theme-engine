#!/usr/bin/env python3
"""Test colorz extraction"""

import colorz

# Extract colors
colors = colorz.colorz("examples/test-wallpaper.jpg", n=8)

print("🎨 colorz Results:")
print(f"Extracted {len(colors)} colors:\n")

for i, color in enumerate(colors):
    # colorz returns ((r, g, b), count) tuples
    rgb = color[0]
    count = color[1] if len(color) > 1 else 0
    hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    print(f"{i+1}. {hex_color}  RGB{rgb}  (count: {count})")
