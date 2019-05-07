# Picture2Avatar

This project is a simple script that process a
photograph to turn it into an avatar.

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
python3 picture2avatar.py input_picture.jpg pre -o result.jpg -p 10
```

If no output file is given, the picture is displayed on the screen.

If no parameter is given to the algorithm (-p value) the default one is used.

## TODOs

* add tests with pytest
* design a GUI to select the input and the algorithm and see
the result on screen and optionally save it
* package a stable version of the script
