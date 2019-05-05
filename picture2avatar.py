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

from PIL import Image, ImageEnhance, ImageFilter


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
    elif(algorithm == "grow"):
        avatar = region_growth(picture)
    elif(algorithm == "km"):
        pass # TODO: k-means
    else:
        print("Unknown algorithm:", algorithm, file=stderr)
    # Save or display the result
    if(output_path):
        avatar.save(output_path)
    else:
        avatar.show()


def precision_downgrade(img: Image, mask_length: int = 1) -> Image:
    """Removes some least significant bits of RGB components of the image.

    This function mask the RGB values of the image and returns the result.
    It is a thresholding on a component.

    :param img: Image, the input image
    :param mask_length: int, the number of most significant bits to keep
    :return: Image, modified image
    """
    mask = lambda p: p & ((0xFF << (8 - mask_length)) & 0xFF)
    return img.point(mask)


def region_growth(img: Image, maxgap: int = 25) -> Image:
    """Segments img and returns the result

    This function performs the region growth algorithm on the picture given
    in input to segment the image and returns the result.

    :param img: Image, the input image to segment
    :param maxgap: int, the maximum gap between the max and min of a region
    """
    # Inner function to perform the loop
    def grow(zones, i_deb, j_deb, zoneNb):
        i = i_deb
        j = j_deb
        i_old = i
        j_old = j
        stack1 = []
        stack2 = []
        stack3 = []
        min_reg = img.getpixel((i, j))
        max_reg = img.getpixel((i, j))
        while True:
            if((not (0 <= i < img.size[0] and 0 <= j < img.size[1])) or
            zones[i][j] != 0 or
            not all(abs(max(img.getpixel((i, j))[b], max_reg[b]) - min(img.getpixel((i_old, j_old))[b], min_reg[b])) < maxgap for b in range(3))):
                if(not stack1): # stack1 empty
                    if(not stack2):
                        if(not stack3):
                            break
                        else: # stack3 not empty
                            j_old = stack3.pop()
                            i_old = stack3.pop()
                            j = stack3.pop()
                            i = stack3.pop()
                            i_old = i
                            j_old = j
                            j = j + 1
                    else: # stack2 not empty
                        j_old = stack2.pop()
                        i_old = stack2.pop()
                        j = stack2.pop()
                        i = stack2.pop()
                        stack3.extend( (i, j, i_old, j_old) )
                        i_old = i
                        j_old = j
                        j = j - 1
                else: # stack1 not empty
                    j_old = stack1.pop()
                    i_old = stack1.pop()
                    j = stack1.pop()
                    i = stack1.pop()
                    stack2.extend( (i, j, i_old, j_old) )
                    i_old = i
                    j_old = j
                    i = i + 1
            else:
                zones[i][j] = zoneNb
                max_reg = [max(img.getpixel((i, j))[b], max_reg[b]) for b in range(3)]
                min_reg = [min(img.getpixel((i, j))[b], min_reg[b]) for b in range(3)]
                stack1.extend( (i, j, i_old, j_old) )
                i_old = i
                j_old = j
                i = i - 1
    # Beginning of the function
    w, h = img.size
    zones = [[0 for j in range(h)] for i in range(w)]
    zoneNB = 1
    for i in range(w):
        for j in range(h):
            if(zones[i][j] == 0):
                grow(zones, i, j, zoneNB)
                zoneNB += 1
    # Compute the average color of each zone
    sum_color = [ [0, 0, 0] for i in range(zoneNB) ]
    count_color = [ 0 for i in range(zoneNB) ]
    count_color[0] = 1 # avoid ZeroDivisionError
    for i in range(w):
        for j in range(h):
            for b in range(3):
                sum_color[zones[i][j]][b] += img.getpixel((i, j))[b]
            count_color[zones[i][j]] += 1
    avg_color = [ [sum_color[i][b] // count_color[i] for b in range(3) ] \
        for i in range(zoneNB) ]
    # Apply the colors to the result
    result = Image.new("RGB", (w, h))
    for i in range(w):
        for j in range(h):
            result.putpixel((i, j), tuple(avg_color[zones[i][j]]))
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Process an photograph to extract a simple avatar.')
    parser.add_argument("input_path", help="path to the photograph to process")
    parser.add_argument("algorithm", choices=[
                        "pre", "grow", "km"], help="algorithm to apply")
    parser.add_argument("-o", "--output", dest="output_path",
                        help="path to store the resulting picture in"
                            " (display if not provided)")
    args = parser.parse_args()
    main(**vars(args))
