#!/usr/bin/env python3
# coding: utf8

"""
Picture2Avatar module

A module containing functions to segment a photograph
and turn it into an avatar (more or less).
Can be invoked from the command line, see arguments
at the end of the file (or invoke with -h).
"""

from sys import stderr

from PIL import Image


def main(input_path: str, algorithm: str, output_path: str = None, param: int = None) -> None:
    """Main function of the program.

    This function loads an input image and generates an output
    one using the specified algorithm.

    :param input_path: str, path to the input photograph
    :param algorithm: str, the algorithm to apply to input ("pre", "grow", "clu", "greed")
    :param output_path: str, path to store the output picture (display if None)
    :param param: int, parameter to give to the algorithm
    """
    picture = None
    # Load the picture
    try:
        picture = Image.open(input_path)
    except IOError as e:
        if __name__ == "__main__":
            print(f"The picture {input_path} could not be loaded.", file=stderr)
        else:
            raise e # file cannot be openned
    # Apply the specified algorithm
    avatar = None
    if(algorithm == "pre"):
        avatar = precision_downgrade(picture) if not param else precision_downgrade(picture, param)
    elif(algorithm == "grow"):
        avatar = region_growth(picture) if not param else region_growth(picture, param)
    elif(algorithm == "clu"):
        avatar = clustering(picture) if not param else clustering(picture, param)
    elif(algorithm == "greed"):
        avatar = greedy_algorithm(picture) if not param else greedy_algorithm(picture, param)
    else:
        if __name__ == "__main__":
            print("Unknown algorithm:", algorithm, file=stderr)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    # Save or display the result
    if(output_path):
        avatar.save(output_path)
    else:
        avatar.show()


def precision_downgrade(img: Image.Image, mask_length: int = 1) -> Image.Image:
    """Removes some least significant bits of RGB components of the image.

    This function mask the RGB values of the image and returns the result.
    It is a thresholding on a component.

    :param img: Image, the input image
    :param mask_length: int, the number of most significant bits to keep
    :return: Image, modified image
    """
    def mask(p): return p & ((0xFF << (8 - mask_length)) & 0xFF)
    return img.point(mask)


def region_growth(img: Image.Image, maxgap: int = 25) -> Image.Image:
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
                if(not stack1):  # stack1 empty
                    if(not stack2):
                        if(not stack3):
                            break
                        else:  # stack3 not empty
                            j_old = stack3.pop()
                            i_old = stack3.pop()
                            j = stack3.pop()
                            i = stack3.pop()
                            i_old = i
                            j_old = j
                            j = j + 1
                    else:  # stack2 not empty
                        j_old = stack2.pop()
                        i_old = stack2.pop()
                        j = stack2.pop()
                        i = stack2.pop()
                        stack3.extend((i, j, i_old, j_old))
                        i_old = i
                        j_old = j
                        j = j - 1
                else:  # stack1 not empty
                    j_old = stack1.pop()
                    i_old = stack1.pop()
                    j = stack1.pop()
                    i = stack1.pop()
                    stack2.extend((i, j, i_old, j_old))
                    i_old = i
                    j_old = j
                    i = i + 1
            else:
                zones[i][j] = zoneNb
                max_reg = [max(img.getpixel((i, j))[b], max_reg[b])
                           for b in range(3)]
                min_reg = [min(img.getpixel((i, j))[b], min_reg[b])
                           for b in range(3)]
                stack1.extend((i, j, i_old, j_old))
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
    sum_color = [[0, 0, 0] for i in range(zoneNB)]
    count_color = [0 for i in range(zoneNB)]
    count_color[0] = 1  # avoid ZeroDivisionError
    for i in range(w):
        for j in range(h):
            for b in range(3):
                sum_color[zones[i][j]][b] += img.getpixel((i, j))[b]
            count_color[zones[i][j]] += 1
    avg_color = [[sum_color[i][b] // count_color[i] for b in range(3)]
                 for i in range(zoneNB)]
    # Apply the colors to the result
    result = Image.new("RGB", (w, h))
    for i in range(w):
        for j in range(h):
            result.putpixel((i, j), tuple(avg_color[zones[i][j]]))
    return result


def clustering(img: Image.Image, nb_color_keep: int = 15) -> Image.Image:
    """Performs a clustering on the colors of the image

    This function collect all colors used in the image, then perform an
    ascending clustering to group them (and compute the average), finally
    keeps nb_color_keep colors and apply them to the image to obtain the
    result.

    :param img: Image, the input picture
    :param nb_color_keep: int >1, the number of colors used in the resulting image
    :return: Image, same as img but with nb_color_keep colors
    """
    # Some inner functions
    def d_color(a, b): # "distance" between two colors
        return sum((b[i] - a[i])*(b[i] - a[i]) for i in range(len(a)))
    def get_closest_colors(colors):
        min_d = d_color(colors[0], colors[1])
        a = colors[0]
        b = colors[1]
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                d = d_color(colors[i], colors[j])
                if(d < min_d):
                    min_d = d
                    a = colors[i]
                    b = colors[j]
        return a, b
    def closest_color(color, color_palette):
        closest = color_palette[0]
        d_closest = d_color(color, closest)
        for c in color_palette[1:]:
            d = d_color(color, c)
            if(d < d_closest):
                d_closest = d
                closest = c
        return closest
    ## Beginning of the function
    w, h = img.size
    # List all colors used in the original picture
    original_color_palette = {img.getpixel((i, j)) for j in range(h) for i in range(w)}
    colors = list(original_color_palette)
    # Perform the clustering
    while(len(colors) > nb_color_keep):
        # merge the two closest colors
        a, b = get_closest_colors(colors)
        c = [(aa+bb)/2 for aa,bb in zip(a, b)]
        colors.remove(a)
        colors.remove(b)
        colors.append(c)
    # Apply the new colors to the original picture
    color_map = { original_color: [ round(b) for b in closest_color(original_color, colors) ]
        for original_color in original_color_palette }
    result = Image.new("RGB", (w, h))
    for i in range(w):
        for j in range(h):
            result.putpixel((i, j), tuple(color_map[img.getpixel((i, j))]))
    return result


def greedy_algorithm(img: Image.Image, nb_color_keep: int = 10) -> Image.Image:
    """Reduce the number of colors in the image

    This function try to compute the nb_color_keep average colors of an image
    with a greedy algorithm and then apply this new palette of color to the
    image to generate the output.
    The result is like an overcompressed jpeg image.

    :param img: Image, the input picture
    :param nb_color_keep: int >1, the number of colors used in the resulting image
    :return: Image, same as img but with nb_color_keep colors
    """
    # Inner functions
    def d_color(a, b): # "distance" between two colors
        return sum((b[i] - a[i])*(b[i] - a[i]) for i in range(len(a)))
    def get_closest_color_index(color, color_palette):
        index = 0
        d_closest = d_color(color, color_palette[index])
        for i in range(1, len(color_palette)):
            d = d_color(color, color_palette[i])
            if(d < d_closest):
                d_closest = d
                index = i
        return index
    # Beginning of the function
    w, h = img.size
    # Generate the list of initial colors
    colors = [ [255*i/(nb_color_keep-1) for b in range(3)] for i in range(nb_color_keep) ]
    colors_weight = [ 0 for i in range(nb_color_keep) ]
    for i in range(w):
        for j in range(h):
            c = img.getpixel((i, j))
            index = get_closest_color_index(c, colors)
            colors[index] = [ (colors_weight[index]*colors[index][b] + \
                c[b])/(colors_weight[index] + 1) for b in range(3) ]
            colors_weight[index] += 1
    # round all the colors
    colors = [ tuple([round(band) for band in color]) for color in colors ]
    # Generate the result
    result = Image.new("RGB", (w, h))
    for i in range(w):
        for j in range(h):
            c = img.getpixel((i, j))
            index = get_closest_color_index(c, colors)
            result.putpixel((i, j), colors[index])
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Process an photograph to extract a simple avatar.')
    parser.add_argument("input_path", help="path to the photograph to process")
    parser.add_argument("algorithm",
                        choices=["pre", "grow", "clu", "greed"],
                        help="algorithm to apply")
    parser.add_argument("-o", "--output", dest="output_path",
                        help="path to store the resulting picture in"
                        " (display if not provided)")
    parser.add_argument("-p", "--param", type=int,
                        help="an argument to the algorithm")
    args = parser.parse_args()
    main(**vars(args))
