"""numpy implementation of image filters"""

from typing import Optional
import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    # Hint: use numpy slicing in order to have fast vectorized code
         
    # the filter_weights as np.array()
    filter_weights_arr = np.array([0.21, 0.72, 0.07])
    
    h, w, c = image.shape
    # A simple multiplication of np.array-by-np.array 
    # gives the necessary result.
    # One could also do: image[:,:,:3]*filter_weights.
    
    # we get one array per pixel. The arrays must be 
    # repeated 3 times and reshaped into the image.shape
    gray_image = np.repeat(image@filter_weights_arr,3, axis=1).reshape(h, w, c)
    
    # Return image (make sure it's the right type!)
    
    # Image.fromarray() requires type "uint8". Must revert 
    # the type back to "uint8".
    gray_image = gray_image.astype("uint8")
    
    return gray_image


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    
    sepia_image = image.astype("float32").copy()

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    sepia_matrix = np.array([[ 0.393, 0.769, 0.189],
                             [ 0.349, 0.686, 0.168],
                             [ 0.272, 0.534, 0.131]
                             ])

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter
    sepia_image = np.einsum("sk, ijk", sepia_matrix, sepia_image)

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    sepia_image[sepia_image > 255] = 255    

    # Return image (make sure it's the right type!)
    sepia_image = sepia_image.astype("uint8")
    
    return sepia_image
