"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import io

# Edit:
# Filled in the two functions for run_filter() and main()
def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = io.read_image(file)
    if scale != 1:
        # Resize image, if needed
        width, height, channels = np.shape(image)
        width, height = width//scale, height//scale
        image = np.resize(image, (width, height, channels))

    # Apply the filter
    filter_function = instapy.get_filter(filter, implementation)
    filtered = filter_function(image)
    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename")

    # Add required arguments
    parser.add_argument("-g", "--gray", action='store_const', const='color2gray', help="Select gray filter")
    parser.add_argument("-se", "--sepia", action='store_const', const='color2sepia', help="Select sepia filter")
    parser.add_argument("-sc", "--scale", type=int, help="Scale factor to resize image")
    parser.add_argument("-i", "--implementation", choices=["python", "numba", "numpy"], help="The implementation")

    # parse arguments and call run_filter
    args = parser.parse_args()
    out_file = None
    implementation = 'python'
    filter = 'color2gray'
    scale = 1

    # Checks for arguments in the command line
    if args.out:
        out_file = args.out
    if args.implementation:
        implementation = args.implementation
    if args.gray:
        filter = args.gray
        if args.sepia:
            raise TypeError("Can't use sepia and grayscale in one.")
    if args.sepia:
        filter = args.sepia
        if args.gray:
            raise TypeError("Can't use sepia and grayscale in one.")
    if args.scale:
        scale = args.scale
    run_filter(args.file, out_file, implementation, filter, scale)
