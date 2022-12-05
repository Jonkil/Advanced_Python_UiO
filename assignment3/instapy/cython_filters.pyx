"""Cython implementation of filter functions"""

"""This implementation follows the guidlines 
    given in the Cython documentation:
    https://cython.readthedocs.io/en/latest/src/tutorial/numpy.html
"""

from email.mime import image
import numpy as np
cimport numpy as np
cimport cython


np.import_array() # for accessing .shape of a Python's numpy array


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def cython_color2gray(np.ndarray[np.uint8_t, ndim=3] image):
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image_uint8
    """
    cdef np.ndarray[np.double_t, ndim=3] gray_image = np.empty_like(image, dtype=np.double)
    cdef np.ndarray[np.double_t, ndim=1] filter_weights = np.array([0.21, 0.72, 0.07], dtype=np.double)
    
    # height, width of pixels will be used in the for cycle
    cdef int height = image.shape[0]
    cdef int width = image.shape[1]
    cdef int channels = image.shape[2]
    cdef int i, j, k
    
    cdef double gray_color = 0
    
    # looping through each pixel
    for i in range(height):
        for j in range(width):
            gray_color = 0
            for k in range(channels):
                gray_color += image[i,j,k]*filter_weights[k]
            for k in range(channels):
                gray_image[i,j,k] = gray_color

    # Image.fromarray() requires type "uint8". Must revert 
    # the type back to "uint8".
    gray_image_uint8 = np.array(gray_image).astype("uint8")
    
    return gray_image_uint8



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def cython_color2sepia(np.ndarray[np.uint8_t, ndim=3] image):
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image_uint8
    """
    
    cdef np.ndarray[np.double_t, ndim=3] sepia_image = np.empty_like(image, dtype=np.double)
    cdef np.ndarray[np.double_t, ndim=2] sepia_matrix = np.array([[ 0.393, 0.769, 0.189],
                                                                  [ 0.349, 0.686, 0.168],
                                                                  [ 0.272, 0.534, 0.131]
                                                                  ], dtype=np.double)
    
    # height, width of pixels will be used in the for cycle
    cdef int height = image.shape[0]
    cdef int width = image.shape[1]
    cdef int channels = image.shape[2]
    cdef int i, j, k
    
    cdef double val = 0
    
    # looping through each pixel
    for i in range(height):
        for j in range(width):
            for k in range(channels): # loop over new RGB values
                val = 0
                for m in range(channels): # loop over original RGB values
                    # sum of RGB pixel values multiplied by sepia weights 
                    val += image[i,j,m]*sepia_matrix[k][m]
                sepia_image[i,j,k]= min(val, 255) # highest value must be 255


    # Image.fromarray() requires type "uint8". Must revert 
    # the type back to "uint8".
    sepia_image_uint8 = np.array(sepia_image).astype("uint8")
    
    return sepia_image_uint8

