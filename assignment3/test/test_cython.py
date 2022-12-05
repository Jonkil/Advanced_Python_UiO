from instapy.cython_filters import cython_color2gray, cython_color2sepia
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
    """Check that grayscale filter works in cython implementation."""
    gray_image = cython_color2gray(image)
    
    # check that the result has the right shape, type
    assert isinstance(gray_image, np.ndarray)
    assert len(gray_image.shape) == 3
    assert gray_image.dtype == np.uint8
    assert gray_image.shape[2] == 3
    
    # rounding to closest integer may work 
    # differently. Therefore we must allow absolute tolerance to be 1.
    nt.assert_allclose(gray_image, reference_gray, atol=1)


def test_color2sepia(image, reference_sepia):
    """Check that sepia filter works in cython implementation."""
    sepia_image = cython_color2sepia(image)
    
    # check that the result has the right shape, type
    assert isinstance(sepia_image, np.ndarray)
    assert len(sepia_image.shape) == 3
    assert sepia_image.dtype == np.uint8
    assert sepia_image.shape[2] == 3
    
    # rounding to closest integer may work 
    # differently. Therefore we must allow absolute tolerance to be 1.
    nt.assert_allclose(sepia_image, reference_sepia, atol=1)
