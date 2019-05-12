# Picture2Avatar

This project is a simple script that process a
photograph to simplify the color palette and obtain
an image with less shading.

## Installation

### For those who want to use

Checkout to the release branch and follow the instruction to install
the module with `pip`.

### For those who want to contribute

```sh
git clone ...
pipenv install --dev
```

Then, edit files, add features...

To run unit tests and generate coverage info:
```sh
pipenv run pytest --cov=picture2avatar --cov-report html
```

## Usage

Apply an algorithm to a picture and store the result in a file:

```sh
# Example
python3 picture2avatar.py input_picture.jpg pre -o result.jpg -p 10
# Help
python3 picture2avatar.py -h
```

If no output file is given, the picture is displayed on the screen.

If no parameter is given to the algorithm (-p value) the default one is used.

### List of available algorithms

* _pre_: Performs a threshold on each band of the picture
    * optional parameter: number of 1 in the mask (e.g. 2 gives 0xC0,
    3 gives 0xE0), default value 1
* _grow_: Performs a region growth algorithm on the image
    * optional parameter: maximal difference between the color of two pixel
    of the same region
* _clu_: Performs a clustering on the colors of the image
    * optional parameter: number of colors to keep at the end
* _greed_: Use a greedy algorithm to keep only a given number of colors of
the picture (faster then clustering)
    * optional parameter: number of colors to keep at the end

## TODOs

* design a GUI to select the input and the algorithm and see
the result on screen and optionally save it
