"""numba-optimized filters"""
from numba import jit
import numpy as np


def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    # Image.open() has only "read" mode. A copy must be made 
    # to transform the image. Initial type "uint8" rounds numbers after 
    # multiplication with weights. Must change the type to float.
    gray_image = image.astype("float32").copy()
    # iterate through the pixels, and apply the grayscale transform
        
    # the filter_weights as np.array()
    filter_weights_arr = np.array([0.21, 0.72, 0.07])

    @jit(nopython=True)
    def apply_grayscale(image: np.array, filter_arr: np.array) -> np.array:
        """Computes the multiplication of two numpy arrays.

        Args:
            image (np.array): image in the numpy array form, type float
            filter_arr (np.arrray): numpy array of filter weights

        Returns:
            np.array: gray_image
        """
        # height, width of pixels will be used in the for cycle
        height, width, channels = image.shape
        
        # looping through each pixel
        # implemented similar to Task 2 as instructed 
        # in the assignment description
        
        # looping through each pixel
        for i in range(height):
            for j in range(width):
                gray_color = 0    
                for k in range(channels):
                    gray_color += image[i,j,k]*filter_arr[k]
                image[i,j,:] = gray_color
        
        return image

    gray_image = apply_grayscale(gray_image, filter_weights_arr)
    
    # Image.fromarray() requires type "uint8". Must revert 
    # the type back to "uint8".
    gray_image = gray_image.astype("uint8")
    
    return gray_image



def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    
    # Image.open() has only "read" mode. A copy must be made 
    # to transform the image. Initial type "uint8" rounds numbers after 
    # multiplication with weights. Must change the type to float.
    sepia_image = image.astype("float32").copy()
    # iterate through the pixels, and apply the grayscale transform
        
    # the filter_weights as np.array()
    sepia_matrix = np.array([[ 0.393, 0.769, 0.189],
                             [ 0.349, 0.686, 0.168],
                             [ 0.272, 0.534, 0.131],
                             ])

    @jit(nopython=True)
    def apply_sepia(sepia_image: np.array, filter_matrix: np.array) -> np.array:
        """Computes the multiplication of two numpy arrays.

        Args:
            sepia_image (np.array): image in the numpy array form, type float
            filter_matrix (np.arrray): numpy matrix of sepia filter weights

        Returns:
            np.array: sepia_image
        """
        # height, width of pixels will be used in the for cycle
        height, width, channels = image.shape
        
        # looping through each pixel
        # implemented similar to Task 2 as instructed 
        # in the assignment description
        for i in range(height):
            for j in range(width):
                for k in range(channels): # loop over new RGB values
                    val = 0
                    for m in range(channels): # loop over original RGB values
                        # sum of RGB pixel values multiplied by sepia weights 
                        val += image[i,j,m]*filter_matrix[k][m]
                    sepia_image[i,j,k]= min(val, 255) # highest value must be 255
    
        return sepia_image
    
    sepia_image = apply_sepia(sepia_image, sepia_matrix)
    
    # Image.fromarray() requires type "uint8". Must revert 
    # the type back to "uint8".
    sepia_image = sepia_image.astype("uint8")

    return sepia_image
