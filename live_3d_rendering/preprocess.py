import math

from PIL import Image, ImageDraw


def _distance_to_white(image: Image.Image, thresh: int = 180) -> float:
    """Dist from center to white region"""
    cx = image.size[0] // 2
    cy = image.size[1] // 2
    im = image.load()
    lo = 0
    hi = cx
    while lo < hi:
        mid = (lo + hi) // 2
        if im[mid, 0] > thresh:  # white
            lo = mid + 1
        else:  # not white
            hi = mid
    return math.sqrt(cy ** 2 + (cx - lo) ** 2)


def blacken_white_pixels(image: Image.Image, radius: float) -> Image.Image:
    """Blacken all pixels outside of the circular region of interest"""
    cx = image.size[0] // 2
    cy = image.size[1] // 2
    background = Image.new(image.mode, image.size, 0)
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).ellipse(
        (
            (cx - radius, cy - radius),
            (cx + radius, cy + radius),
        ),
        fill=255,
    )
    return Image.composite(image, background, mask)


def preprocess(image: Image.Image, white_treshhold=180):
    if image.mode != "L":
        image = image.convert("L")
    image = blacken_white_pixels(image, _distance_to_white(image, white_treshhold) - 10)
    image = image.point(lambda p: p * (p < white_treshhold))
    return image
