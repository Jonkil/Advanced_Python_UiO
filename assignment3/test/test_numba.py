from instapy.numba_filters import numba_color2gray, numba_color2sepia
from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

import numpy as np
import numpy.testing as nt
from pathlib import Path
from instapy import io

test_dir = Path(__file__).absolute().parent
image = io.read_image(test_dir.joinpath("rain.jpg"))

# compute reference using numpy
reference_gray = numpy_color2gray(image)
reference_sepia = numpy_color2sepia(image)


def test_color2gray(image, reference_gray):
    """Check that grayscale filter works in numba implementation."""
    gray_image = numba_color2gray(image=image)
    
    # check that the result has the right shape, type
    assert isinstance(gray_image, np.ndarray)
    assert len(gray_image.shape) == 3
    assert gray_image.dtype == np.uint8
    assert gray_image.shape[2] == 3
    
    nt.assert_allclose(gray_image, reference_gray)


def test_color2sepia(image, reference_sepia):
    """Check that sepia filter works in numba implementation."""
    sepia_image = numba_color2sepia(image=image)
    
    # check that the result has the right shape, type
    assert isinstance(sepia_image, np.ndarray)
    assert len(sepia_image.shape) == 3
    assert sepia_image.dtype == np.uint8
    assert sepia_image.shape[2] == 3
    
    nt.assert_allclose(sepia_image, reference_sepia)
