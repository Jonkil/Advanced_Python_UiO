# Assignment 3: Package `instapy`.

This package can be used for transforming images by applying `grayscale`and `sepia`filters.

The transformation is implemented using pure `python`, `numpy`, `numba` and `cython`.


Example code for using the package functions:

```
    import numpy as np
    from PIL import Image
    import instapy

    filename = "test/rain.jpg"
    pixels = np.asarray(Image.open(filename))

    gray_filter = instapy.get_filter(filter = "color2gray", implementation='numpy') # can use 'python', 'numba','cython'
    sepia_filter = instapy.get_filter(filter = "color2sepia", implementation='numpy') # can use 'python', 'numba','cython'

    gray_image = gray_filter(pixels)
    sepia_image = sepia_filter(pixels)

    Image.display(gray_image)
    Image.display(sepia_image)

    # in Jupyter notebook just run
    # display(gray_image)
    # display(sepia_image)

    # to save the transformed images run:
    # gray_image.save("rain_gray.jpg")
    # sepia_image.save("rain_sepia.jpg")
```

## Configuring the environment

The installation is done using `conda`.

To set up the environment for the `instapy` package,
navigate to the folder of the package and run in the terminal the following commands:

`conda create -n assignment3 python=3.8 `

`conda activate assignment3`

`python3 -m pip install --upgrade setuptools pip`

Dependancy packages like `numpy`, `Cython` should get installed when installing the `instapy` package. However, this may not work on different systems. Installing dependancies in advance is recommended.

`pip install numpy`

`pip install Cython --install-option="--no-cython-compile"`

To be able tu run Jupyter notebooks in this environment install `ipykernel`:

`conda install ipykernel` 

---
## Task 1 - make the package installable
Navigate to the folder of the package and run in the terminal:

`python3 -m pip install --no-build-isolation .`

Some warnings can be expected due to deprecated things in Numpy API for Cython.

To check that the package is installed the following in the ternminal:

`pip install pytest`

`python3 -m pytest -v test/test_package.py`

---
## Task 9-10 - tests for the filters

To run tests for the `instapy` package, use the following command:
`python3 -m pytest -v test/test_*`

---
## Task 11 - callable from the command line

To run the `instapy` package from the command line, use the following commands:
`python instapy file_name filter implementation scaling out_file`

You can use the following flags:
`-gs` and `-se` for grayscale and sepia respectively (Default = grayscale)
`-i` for implementation (Default = python)
`-sc` for scaling (Default = 1)
`-o` for the filename your filtered image should be saved to. (Default = None, meaning it will just display it.)


