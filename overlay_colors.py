"""Central place for overlay color constants used by the project.

Use names instead of raw RGB tuples so UI colors are consistent and easier
to change from one place.
"""
# BGR color tuples (OpenCV uses BGR ordering)
COLOR_LANDMARK_SMALL_BLUE = (200, 0, 0)
COLOR_BBOX_HAND = (255, 50, 0)
COLOR_BBOX_PALM = (150, 50, 0)

COLOR_POINT_A = (55, 66, 200)
COLOR_POINT_B = (177, 235, 220)
COLOR_LINE = (255, 0, 255)

COLOR_FINGERTIP = (0, 0, 200)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)

__all__ = [
    "COLOR_LANDMARK_SMALL_BLUE",
    "COLOR_BBOX_HAND",
    "COLOR_BBOX_PALM",
    "COLOR_POINT_A",
    "COLOR_POINT_B",
    "COLOR_LINE",
    "COLOR_FINGERTIP",
    "COLOR_GREEN",
    "COLOR_BLUE",
    "COLOR_WHITE",
]
