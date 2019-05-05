# Picture2Avatar

This project is a simple script that process a
photograph to turn it into an avatar usable as
profile picture.

## Installation

### For those who want to use

TODO

### For those who want to contribute

```sh
$ pipenv install --dev
```

Then, edit files, add features...

## Usage

Apply an algorithm to a picture and store the result in a file:

```sh
python3 picture2avatar.py input_picture.jpg pre -o result.jpg
```

If no output file is given, the picture is displayed on the screen.

## TODOs

* add tests with pytest
* design a GUI to select the input and the algorithm and see
the result on screen and optionally save it
* package a stable version of the script

## Ideas

* Get the list of every colors used in the image and perform a K-mean 
