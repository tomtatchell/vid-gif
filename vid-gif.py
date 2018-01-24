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

# TODO: run terminal command to generate gif using palette and input file
# TODO: cleanup by removing palette file
# TODO: add user controls
# TODO: package into droplet app

inputFile = "/Users/bbmp03/Desktop/temp/vg-py/logo-anim.mov"

if os.path.isfile(inputFile):
    print(os.path.dirname(inputFile))


def get_mov_info(mov):
    """
    Get the width, height and fps of source movie file
    :param mov: source movie file
    :return: list: file_info: width, height, fps
    """
    file_info = []
    if os.path.isfile(mov):
        # TODO: get info from video file
        # TODO: get output of shell command
        cmd = ['ffprobe', '-show_streams', mov]
        result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
        for x in result:
            if x.startswith("width"):
                width = x.split('=')[1]
                file_info.append(width)
            if x.startswith("height"):
                height = x.split('=')[1]
                file_info.append(height)
            if x.startswith("avg_frame_rate"):
                fps_raw = x.split('=')[1]
                fps = fps_raw.split('/')[0]
                file_info.append(fps)

    return file_info


def palette_gen(mov, width, fps):
    """
    Generates the palette for the gif to be generated
    :param mov: source movie file
    :param width: source movie width
    :param fps: source movie fps
    :return: None
    """

    if os.path.isfile(mov):
        cmd = ['ffmpeg', '-y', '-i', mov, '-vf',
               'fps={fps},scale={scale}:-1:flags=lanczos,palettegen'.format(fps=fps, scale=width),
               '{}/.palette.png'.format(os.path.dirname(mov))]
        result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        return result


def main():
    width, height, fps = get_mov_info(inputFile)
    palette_gen(inputFile, width, fps)


if __name__ == "__main__":
    main()
