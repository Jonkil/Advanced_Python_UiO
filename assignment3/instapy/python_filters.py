"""pure Python implementation of image filters"""

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    # iterate through the pixels, and apply the grayscale transform
    
    # Image.open() has only "read" mode. A copy must be made 
    # to transform the image. Initial type "uint8" rounds numbers after 
    # multiplication with weights. Must change the type to float.
    gray_image = image.astype("float32").copy()
    
    # weights of the filter as given in the assignment description
    filter_weights = [0.21, 0.72, 0.07]
    
    # height, width of pixels will be used in the for cycle
    height, width, channels = image.shape
    
    # looping through each pixel
    for i in range(height):
        for j in range(width):
            gray_color = 0    
            for k in range(channels):
                gray_color += gray_image[i,j,k] *filter_weights[k]
            gray_image[i,j,:] = gray_color
            
    # Image.fromarray() requires type "uint8". Must revert 
    # the type back to "uint8".
    gray_image = gray_image.astype("uint8")
    
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
        
    # Image.open() has only "read" mode. A copy must be made 
    # to transform the image. Initial type "uint8" rounds numbers after 
    # multiplication with weights. Must change the type to float.
    sepia_image = image.astype("float32").copy()
    
    # Iterate through the pixels
    # applying the sepia matrix

    sepia_matrix = np.array([
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131]
        ])

    # height, width of pixels will be used in the for cycle
    height, width, channels = image.shape
    
    """
        To display a source image in sepia we need to average the value of all 
        colour channels and replace the resulting value with sepia color.

        Here is the sepia filter matrix in RGB order you will be using in this task. 
        You can multiply each color value in the corresponding channel of a pixel with 
        the RGB ordered matrix given here:

        sepia_matrix = [
            [ 0.393, 0.769, 0.189],
            [ 0.349, 0.686, 0.168],
            [ 0.272, 0.534, 0.131],
        ]
        Each of the rows represents the weights for the colors RGB in their respective channels.
        Because the input image is read as an array of unsigned 8-bit integers (uint8), 
        adding such values will cause an overflow when the sum exceeds 255. To combat such overflows, 
        one can for example set the maximum value to 255 for each channel.
    """
    
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
    sepia_image = sepia_image.astype("uint8")
    
    return sepia_image
