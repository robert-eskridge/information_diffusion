import random

def weight_to_gray(weight):
    try:
        weight = float(weight)
    except (ValueError, TypeError):
        weight = 0.5  # fallback to mid-gray

    # Clamp to [0, 1]
    weight = max(0.0, min(1.0, weight))
    gray_level = int((1 - weight) * 255) #invert weight where 1 is black and 0 is white
    return f'#{gray_level:02x}{gray_level:02x}{gray_level:02x}'

# helper function encoding a tuple in format (r,g,b) to hex value
def encode_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

# helper function decoding hex in format #ffffff to rgb tuple
def decode_from_hex(hex):
    return tuple(int(hex[i:i+2], 16) for i in (1,3,5))

# helper function that mixes colors based on weights. colors is a list of color tuples. 
# weights is a list of weights adding to 1. Use this to mix colors of neighboring nodes, normalizing their influence
# against each other to get a value of 1.
def mix_colors(colors, weights):
    r = sum(c[0] * w for c, w in zip(colors, weights))
    g = sum(c[1] * w for c, w in zip(colors, weights))
    b = sum(c[2] * w for c, w in zip(colors, weights))
    return encode_to_hex((int(r), int(g), int(b)))