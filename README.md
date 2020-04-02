# Image segmentation with Python

This project is a simple script that process a
picture to simplify its color palette and obtain
an image with less shading.

It is only an experiment, not a ready-to-use software.

## Installation

### For those who want to use

Go to the
[release page](https://github.com/ThomasCluzel/python-image-segmentation/releases)
and follow the instructions to download and to install the module with `pip`.

Then, you will be able to type in a terminal:
* `python -m picture2avatar [args...]` to run the command line tool
* `picture2avatar` to launch the gui

You will also be able to use the module in other projects:
```python
import picture2avatar
help(picture2avatar)
```

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

To package the module:
```sh
pipenv run python setup.py sdist bdist_wheel
```

## Usage

Apply an algorithm to a picture and store the result in a file:
```sh
# Example
pipenv run python picture2avatar.py input_picture.jpg pre -o result.jpg -p 10
# Help
pipenv run python picture2avatar.py -h
# GUI
pipenv run python guipicture2avatar.pyw
```
* If no output file is given, the picture is displayed on the screen.
* If no parameter is given to the algorithm ("-p value") the default one is used.

### List of available algorithms

* _pre_: Performs a threshold on each band of the picture
    * optional parameter: number of 1 in the mask (e.g. 2 gives 0xC0,
    3 gives 0xE0), default value 1
* _grow_: Performs a region growth algorithm on the image
    * optional parameter: maximal difference between the color of two pixel
    of the same region
* _clu_: Performs a clustering on the colors of the image
    * optional parameter: number of colors to keep at the end
    * :warning: it can be very long to process
* _greed_: Use a greedy algorithm to keep only a given number of colors of
the picture (faster than clustering)
    * optional parameter: number of colors to keep at the end
