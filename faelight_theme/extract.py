"""
Color extraction from wallpapers.

This module handles extracting dominant colors from image files.
"""

def extract_colors(image_path: str, num_colors: int = 8) -> list[tuple[int, int, int]]:
    """
    Extract dominant colors from wallpaper.
    
    Args:
        image_path: Path to wallpaper image
        num_colors: Number of colors to extract (default: 8)
    
    Returns:
        List of RGB tuples
        
    TODO: Implement in v2.8.2
    """
    raise NotImplementedError("Coming in v2.8.2!")

def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex string."""
    raise NotImplementedError("Coming in v2.8.2!")
