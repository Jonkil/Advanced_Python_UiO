from instapy.python_filters import python_color2gray, python_color2sepia
from pathlib import Path

import numpy as np
import numpy.testing as nt
from instapy import io

test_dir = Path(__file__).absolute().parent
image = io.read_image(test_dir.joinpath("rain.jpg"))

def test_color2gray(image):
    """Check that grayscale filter works in Python implementation."""
    # run color2gray
    gray_image = python_color2gray(image=image)
    
    # check that the result has the right shape, type
    assert isinstance(gray_image, np.ndarray)
    assert len(gray_image.shape) == 3
    assert gray_image.dtype == np.uint8
    assert gray_image.shape[2] == 3
    
    # assert uniform r,g,b values
    height, width, channels = gray_image.shape
    
    # choose random 10 pixels and check that RGB values 
    # are equal to the R value
    np.random.seed(1)
    h = np.random.choice(np.arange(height), 10)
    w = np.random.choice(np.arange(width), 10)
    
    for i in h:
        for j in w:
            assert np.allclose(gray_image[i,j],gray_image[i,j,0])


def test_color2sepia(image):
    """Check that sepia filter works in Python implementation."""
    # run color2sepia
    sepia_image = python_color2sepia(image=image)
    
    # check that the result has the right shape, type
    assert isinstance(sepia_image, np.ndarray)
    assert len(sepia_image.shape) == 3
    assert sepia_image.dtype == np.uint8
    assert sepia_image.shape[2] == 3
    
    # verify some individual pixel samples    
    # according to the sepia matrix
    height, width, channels = sepia_image.shape
    sepia_matrix = np.array([[ 0.393, 0.769, 0.189],
                             [ 0.349, 0.686, 0.168],
                             [ 0.272, 0.534, 0.131]
                             ])
    # subsample 10 random pixels,
    # manually apply the sepia_matrix to them 
    # and check that RGB values im sepia_image
    # coinside with the sepia_test_image
    np.random.seed(1)
    h = np.random.choice(np.arange(height), 10)
    w = np.random.choice(np.arange(width), 10)
    
    test_image = image[h,w].astype("float32").copy()
    sepia_test_image = np.einsum("sk, ik", sepia_matrix, test_image)
    sepia_test_image[sepia_test_image > 255] = 255    
    sepia_test_image = sepia_test_image.astype("uint8")
    
    nt.assert_allclose(sepia_image[h,w], sepia_test_image)
