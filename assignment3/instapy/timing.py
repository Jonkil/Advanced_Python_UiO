"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
import instapy
from . import io
from typing import Callable
import numpy as np
from PIL import Image

def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    call_times = np.zeros(calls)
    
    # run the filter function `calls` times
    for i in range(calls):
        start_time = time.perf_counter()
        result = filter_function(*arguments)
        end_time = time.perf_counter()
        call_times[i] = end_time - start_time
    
    # return the _average_ time of one call
    return call_times.mean()
    


def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    image = np.asarray(Image.open(filename))
    
    # list of text lines to write into the file timing-report.txt
    report_lines=[]
    
    # print the image name, width, height
    s = f"Timing performed using {filename}: {image.shape[0]}x{image.shape[1]}"
    print(s,"\n")
    
    report_lines.append(s)
    
    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"]
    for filter_name in filter_names:
        # get the reference filter function
        reference_filter = "python"
        # time the reference implementation
        filter_function = instapy.get_filter(filter = filter_name, implementation=reference_filter)
        reference_time = time_one(filter_function, image, calls=3)
        
        s = f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        print(s)
        
        report_lines.append('')
        report_lines.append(s)
        
        # iterate through the implementations
        implementations = ("numpy", "numba", "cython")
        for implementation in implementations:
            filter_function = instapy.get_filter(filter = filter_name, implementation=implementation)
            # time the filter
            filter_time = time_one(filter_function, image, calls=3)
            # compare the reference time to the optimized time
            speedup = reference_time/filter_time
            s = f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            print(s)
            report_lines.append(s)
        
        print("\n")        
        
    report_filename = "timing-report.txt"
    with open(report_filename, 'w') as f:
        for line in report_lines:
            f.write(line)
            f.write('\n')
            
    print(f"Report is written into {report_filename}")
        
    
if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
