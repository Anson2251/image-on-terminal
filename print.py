#! /usr/bin/env python3

import shutil
from PIL import Image
import os;
import math;

# Get the terminal size
size = shutil.get_terminal_size()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="A script to print out an image in the terminal")
    parser.add_argument('-i', '--input', type=str, required=True, help='The input image')
    parser.add_argument('-s', '--scale', type=float, default=2, help='The ratio to the height of the terminal characters and the width of the terminal characters')
    parser.add_argument('-g', '--grey', type=str, default="y", help='Whether to use greyscale or not [y/n]')
    parser.add_argument('-a', '--ansi', type=str, default="n", help='Whether to use ANSI colours or not [y/n]')
    return parser.parse_args()

def rotate_image(image):
    exif_data = image._getexif()

    if exif_data is None:
        return image

    orientation = exif_data.get(274)

    if orientation is not None:
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)

    return image

def rgb_to_ansi_escape(r, g, b):
    return '\033[38;2;{};{};{}m'.format(r, g, b)

ansi_codes = {
    '#000000': '\033[30m',  # Black
    '#800000': '\033[31m',  # Red
    '#008000': '\033[32m',  # Green
    '#808000': '\033[33m',  # Yellow
    '#000080': '\033[34m',  # Blue
    '#800080': '\033[35m',  # Purple
    '#008080': '\033[36m',  # Cyan
    '#c0c0c0': '\033[37m',  # White
    '#808080': '\033[90m',  # Bright black
    '#ff0000': '\033[91m',  # Bright red
    '#00ff00': '\033[92m',  # Bright green
    '#ffff00': '\033[93m',  # Bright yellow
    '#0000ff': '\033[94m',  # Bright blue
    '#ff00ff': '\033[95m',  # Bright purple
    '#00ffff': '\033[96m',  # Bright cyan
    '#ffffff': '\033[97m'   # Bright white
}

def rgb_to_ansi(r, g, b):
    hex_color = f'#{r:02x}{g:02x}{b:02x}'
    
    if hex_color in ansi_codes:
        return ansi_codes[hex_color]
    else:
        # Find the nearest color
        min_distance = float('inf')
        nearest_color = None

        for hex_code, ansi_code in ansi_codes.items():
            # Convert hex color to RGB
            hr, hg, hb = int(hex_code[1:3], 16), int(hex_code[3:5], 16), int(hex_code[5:7], 16)
            # Calculate Euclidean distance
            distance = math.sqrt((r - hr) ** 2 + (g - hg) ** 2 + (b - hb) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_color = ansi_code

        return nearest_color

def reset_ansi():
    return '\033[0m'

# Extract the width
con_width = size.columns
con_height = size.lines - 2

args = get_args()
image = rotate_image(Image.open(args.input))
img_width, img_height = image.size

scale = min(con_width / img_width, con_height / img_height)

fin_width = int(img_width * scale * args.scale)
fin_height = int(img_height * scale)

grey_chars = ' .:-~=+*a!|({8&$#%@'
grey_image = image.resize((fin_width, fin_height)).convert(mode='L', colors=256)
color_image = image.resize((fin_width, fin_height)).convert(mode='RGB', colors=256)

clear_terminal()
for y in range(fin_height):
    for x in range(fin_width):
        grey_scale = grey_image.getpixel((x, y))
        if args.grey == "y":
            pixel = grey_chars[int(grey_scale/256*len(grey_chars))]
        else:
            colour = color_image.getpixel((x, y))
            if(args.ansi == "y"):
                code = rgb_to_ansi(*colour)
            else:
                code = rgb_to_ansi_escape(*colour)
            pixel = f"{code}{"█" if args.ansi == 'n' else grey_chars[round(float(grey_scale/256*len(grey_chars)))]}{reset_ansi()}"
        print(pixel, end='')
    print()
