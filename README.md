# VID-GIF converter

A simple script to convert a movie file to a gif

## Getting Started

This will get the script up and running on your machine

### Prerequisites

This script uses ffmpeg to convert the files  
I recommend install it with homebrew  
To install homebrew, go to https://brew.sh/  
Or enter the following command from terminal:

```commandline
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Once done, install ffmpeg:

```commandline
brew install ffmpeg
```

## Running the script

Run the script from terminal:

```commandline
python3 vid-gif.py /path/to/your/movie/file.mov
```

It will then handle the rest, outputting a gif the same resolution and frame rate of the source