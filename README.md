# Image on Terminal

A tiny script to print an image on the terminal.

The idea came from ASCII art and a special greeting from my best friend.

## Usage

    usage: print.py [-h] -i INPUT [-s SCALE] [-g GREY] [-a ANSI]

    options:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
                            The input image
    -s SCALE, --scale SCALE
                            The ratio to the height of the terminal characters and the width of the terminal characters
    -g GREY, --grey GREY  Whether to use greyscale or not [y/n]
    -a ANSI, --ansi ANSI  Whether to use ANSI colours or not [y/n]

## Setup

### Setup venv

```bash
cd image-on-terminal
python3 -m venv ./ 
source ./bin/activate
```

### Install dependencies

```bash
pip install Pillow
```
