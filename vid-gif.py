import os
import subprocess


# TODO: add user controls
# TODO: package into droplet app

inputFile = "/Users/bbmp03/Desktop/temp/vg-py/logo-anim.mov"


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
    :return:
    """

    if os.path.isfile(mov):
        cmd = ['ffmpeg', '-y', '-i', mov, '-vf',
               'fps={fps},scale={scale}:-1:flags=lanczos,palettegen'.format(fps=fps, scale=width),
               '{}/.palette.png'.format(os.path.dirname(mov))]
        subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')


def gif_conversion(mov, width, fps):
    """
    Uses the previously created palette to generate a gif from the source movie file
    :param mov: source movie file
    :param width: source movie width
    :param fps: source movie fps
    :return:
    """
    if os.path.isfile(mov):
        cmd = ['ffmpeg', '-i', mov, '-i', '{}/.palette.png'.format(os.path.dirname(mov)),
               '-filter_complex',
               'fps={fps},scale={scale}:-1:flags=lanczos[x];[x][1:v]paletteuse'.format(
                   fps=fps, scale=width),
               '{}.gif'.format(os.path.splitext(mov)[0])]
        subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')


def housekeeping(mov):
    """
    Removes the palette file used for creating the gif
    :param mov: source movie file
    :return:
    """
    if os.path.isdir(os.path.dirname(mov)):
        dir = os.path.dirname(mov)
        palette_file = '.palette.png'
        if os.path.isfile(os.path.join(dir, palette_file)):
            os.remove(os.path.join(dir, palette_file))


def main():
    # get file info
    width, height, fps = get_mov_info(inputFile)
    # generate palette
    palette_gen(inputFile, width, fps)
    # generate gif
    gif_conversion(inputFile, width, fps)
    # remove palette
    housekeeping(inputFile)


if __name__ == "__main__":
    main()
