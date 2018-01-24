import os
import subprocess

"""
Generate Palette

-y: Overwirte without asking
-ss: start second
-t: time (length)
-i: input file
-vf: video filter
fps: frames per second
scale: width


ffmpeg -y -ss 30 -t 3 -i input.flv -vf fps=10,scale=320:-1:flags=lanczos,palettegen .palette.png

"""

"""
Generate Gif

-ss: start second
-t: time (length)
-i: input file (2nd -i: palette)
fps: frames per second
scale: width

ffmpeg -ss 30 -t 3 -i input.flv -i palette.png -filter_complex "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
"""

"""
Housekeeping

rm .palette.png
"""

# TODO: get input file + path
# TODO: run terminal command to generate palette based on input file
# TODO: run terminal command to generate gif using palette and input file
# TODO: cleanup by removing palette file
# TODO: add user controls
# TODO: package into droplet app

