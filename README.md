# VID-GIF converter

A simple script to convert a movie file to a gif

## Getting Started

This will get the script up and running on your machine

### Prerequisites

You will need to have ffmpeg installed in order for this script to work  
To install homebrew, go to the following page and follow the instructions  


https://brew.sh/  
  
Or enter the following command from terminal

```commandline
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Once homebrew is installed, run this command to install ffmpeg

```commandline
brew install ffmpeg
```

### Installing

Simply copy the script to your hard drive and run from terminal
Providing you have used `cd` to get to the same directory as vid-gif.py

```commandline
python3 vid-gif.py /path/to/your/movie/file.mov
```

It will then handle the rest, outputting a gif the same resolution and frame rate of the source