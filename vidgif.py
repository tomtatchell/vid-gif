import sys
import os
import subprocess
import logging

logging.basicConfig(filename='vidgif.log',
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.DEBUG)


def get_info(mov):
    """
    Get the width, height and fps of source movie file
    :param mov: source movie file
    :return: list: file_info: width, height, fps
    """
    logging.info("Getting info on {}".format(os.path.split(mov)[1]))
    file_info = []
    if os.path.isfile(mov):
        cmd = ['ffprobe', '-show_streams', mov]
        runcmd = subprocess.run(cmd,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        result = runcmd.stdout.decode('utf-8').split('\n')
        logging.debug(runcmd.stderr.decode('utf-8'))
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
            if x.startswith("nb_frames"):
                frames = x.split('=')[1]
                file_info.append(frames)

    logging.info("Got info on {}".format(os.path.split(mov)[1]))
    return file_info


def palette_gen(mov, width, fps):
    """
    Generates the palette for the gif to be generated
    :param mov: source movie file
    :param width: source movie width
    :param fps: source movie fps
    :return:
    """
    logging.info("Generating palette")
    if os.path.isfile(mov):
        cmd = ['ffmpeg', '-y', '-i', mov, '-vf',
               'fps={fps},scale={scale}:-1:flags=lanczos,palettegen'.format(fps=fps, scale=width),
               '{}/.palette.png'.format(os.path.dirname(mov))]
        runcmd = subprocess.run(cmd, stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        runcmd.stdout.decode('utf-8')
        logging.debug(runcmd.stderr.decode('utf-8'))
        logging.info("Generated palette file")


def gif_conversion(mov, width, fps):
    """
    Uses the previously created palette to generate a gif from the source movie file
    :param mov: source movie file
    :param width: source movie width
    :param fps: source movie fps
    :return:
    """
    logging.info("Starting conversion")
    if os.path.isfile(mov):
        cmd = ['ffmpeg', '-y', '-i', mov, '-i', '{}/.palette.png'.format(os.path.dirname(mov)),
               '-filter_complex',
               'fps={fps},scale={scale}:-1:flags=lanczos[x];[x][1:v]paletteuse'.format(
                   fps=fps, scale=width),
               '{}.gif'.format(os.path.splitext(mov)[0])]
        runcmd = subprocess.run(cmd, stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        runcmd.stdout.decode('utf-8')
        logging.debug(runcmd.stderr.decode('utf-8'))
        logging.info("Conversion Complete!")


def housekeeping(mov):
    """
    Removes the palette file used for creating the gif
    :param mov: source movie file
    :return:
    """
    logging.info("Looking for palette file to remove")
    if os.path.isdir(os.path.dirname(mov)):
        movdir = os.path.dirname(mov)
        palette_file = '.palette.png'
        if os.path.isfile(os.path.join(movdir, palette_file)):
            os.remove(os.path.join(movdir, palette_file))
            logging.info("removed palette file")
        else:
            logging.info("No palette file to remove")


def main():
    # get file info
    width, height, fps = get_info(inputFile)
    # generate palette
    palette_gen(inputFile, width, fps)
    # generate gif
    gif_conversion(inputFile, width, fps)
    # remove palette
    housekeeping(inputFile)


if __name__ == "__main__":
    inputFile = sys.argv[1]
    main()
