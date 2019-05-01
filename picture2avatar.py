#!/usr/bin/env python3
# coding: utf8

"""
Picture2Avatar module

A module containing functions to segment a photograph
and turn it into an avatar.
Can be invoked from the command line, see arguments
at the end of the file.
"""

from sys import stderr

from PIL import Image


def main(input_path: str, algorithm: str, output_path: str = None) -> None:
    """Main function of the program.

    This function loads an input image and generates an output
    one using the specified algorithm.
    :param input_path: str, path to the input photograph
    :param algorithm: str, the algorithm to apply to input ("pre", "snm")
    :param output_path: str, path to store the output picture (display if None)
    """
    picture = None
    # Load the picture
    try:
        picture = Image.open(input_path)
    except IOError:
        print(f"The picture {input_path} could not be loaded.", file=stderr)
        return
    # Apply the specified algorithm
    avatar = None
    if(algorithm == "pre"):
        avatar = precision_downgrade(picture)
    elif(algorithm == "snm"):
        pass # TODO
    else:
        print("Unknown algorithm", file=stderr)
    # Save or display the result
    if(output_path):
        avatar.save(output_path)
    else:
        avatar.show()

def precision_downgrade(img: Image, mask_length: int = 1) -> Image:
    """Removes some least significant bits of RGB components of the image.

    This function mask the RGB values of the image and returns the result.
    :param img: Image, the input image
    :param mask_length: int, the number of most significant bits to keep
    :return: Image, modified image

    TODO:
    - add parameter to enable/disable mean colors computation
    - add parameter to perform opening/closing on the resulting image
    """
    mask = lambda p: p & ((0xFF << (8 - mask_length)) & 0xFF)
    return img.point(mask)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process an photograph to extract a simple avatar.')
    parser.add_argument("input_path", help="path to the photograph to process")
    parser.add_argument("algorithm", choices=["pre", "snm"], help="algorithm to apply")
    parser.add_argument("-o", "--output", dest="output_path", help="path to store the resulting picture in (display if not provided)")
    args = parser.parse_args()
    main(**vars(args))
