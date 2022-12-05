"""Tests for our Array class
    by Assem Maratova
    assemm@uio.no
"""

# Task 4:Unit Tests for 1D Arrays (4 points)

from array_class import Array
import pytest

int_array = Array((5,), 1,2,3,4,5)
float_array = Array((5,), 1.5,1.5,2.0,2.5,2.5)
bool_array = Array((5,), True,False,False,True,False)

def test_str_1d():
    """Returns a nicely printable string representation of the array.
    """
    assert int_array.__str__() == '[1,2,3,4,5]'
    assert float_array.__str__() == '[1.5,1.5,2.0,2.5,2.5]'
    assert bool_array.__str__() == '[True,False,False,True,False]'
    with pytest.raises(TypeError):
        Array((3.5,),1,'2',3).__str__()
        Array(3,1,2,3).__str__()
        Array((3,),1,'2',3).__str__()
    with pytest.raises(ValueError):
        Array((3,),1,False,3).__str__()
        Array((3,),1,2,3,4,5).__str__()

def test_add_1d():
    """Element-wise adds Array with another Array or number.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        check that the method supports the given arguments (check for data type and shape of array)
        if the array is a boolean you should return NotImplemented
    """
    assert int_array + int_array == Array((5,),2,4,6,8,10)
    assert int_array + 5  == Array((5,),6,7,8,9,10)
    assert 2 + int_array == Array((5,),3,4,5,6,7)
    with pytest.raises(NotImplementedError):
        bool_array + int_array
        float_array + Array((3,),0,'3',2)
    with pytest.raises(ValueError):
        int_array + Array((3,),0,1,2)

def test_sub_1d():
    """Element-wise subtracts an Array or number from this Array.
    If the method does not support the operation with the supplied arguments
    (specific data type or shape), it should return NotImplemented.
    """
    assert int_array - 2 == Array((5,),-1,0,1,2,3)
    assert int_array - int_array == Array((5,),0,0,0,0,0)
    assert int_array - float_array == Array((5,),-0.5,0.5,1.0,1.5,2.5)
    assert 10 - int_array == Array((5,),9,8,7,6,5)
    assert float_array - float_array  == Array((5,),0.0,0.0,0.0,0.0,0.0)    
    
    with pytest.raises(NotImplementedError):
        bool_array - int_array
        int_array - Array((3,),0,1,2)
        float_array - Array((3,),0,'3',2)

def test_mul_1d():
    """Checks the new array with every element multiplied with `other`.
    If the method does not support the operation with the supplied arguments
    (specific data type or shape), it should return NotImplementedError.
    """
    assert int_array * 2 == Array((5,),2,4,6,8,10)
    assert 5 * int_array  == Array((5,),5,10,15,20,25)
    assert int_array * int_array == Array((5,),1,4,9,16,25)
    assert int_array * float_array == Array((5,),1.5,3.0,6.0,10.0,12.5)

    with pytest.raises(NotImplementedError):
        int_array * bool_array
        bool_array * float_array
        float_array * Array((3,),0,'3',2)

def test_eq_1d():
    """Compares arrays (by ==) returns a correct boolean answear.
    If the two array shapes do not match, it should return False.
    If `other` is an unexpected type, return False.
    """
    assert (int_array == int_array) == True
    assert (float_array == float_array) == True
    assert (bool_array == bool_array) == True
    assert (int_array == Array((5,),2,3,4,5,6)) == False
    assert (int_array == Array((3,),1,2,3)) == False
    assert (int_array == bool_array) == False
    assert (int_array == 'abcde') == False

def test_same_1d():
    """Checks that comparing an Array element-wise to another array through is_equal() 
    returns the correct boolean array.
        If `other` is an Array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an Array or a number, it should return TypeError.
    """
    assert int_array.is_equal(int_array) == Array((5,),True,True,True,True,True) 
    assert float_array.is_equal(float_array)  == Array((5,),True,True,True,True,True)      
    assert bool_array.is_equal(bool_array)  == Array((5,),True,True,True,True,True)
    assert int_array.is_equal(6) == Array((5,),False,False,False,False,False)
    assert int_array.is_equal(3) == Array((5,),False,False,True,False,False)
    assert float_array.is_equal(1.5)  == Array((5,),True,True,False,False,False)
    assert float_array.is_equal(3.0)  == Array((5,),False,False,False,False,False)
    
    with pytest.raises(ValueError):    
        int_array.is_equal(Array((3,),1,2,3))
        
    with pytest.raises(TypeError):
        float_array.is_equal('abcd')


def test_smallest_1d():
    """Tests that the element returned by min_element() is the “smallest” one in the array.
    Only needs to work for type int and float (not boolean).
    Returns:
    float: The value of the smallest element in the array.
    """
    assert int_array.min_element() == 1.0      
    assert float_array.min_element()  == 1.5      
    with pytest.raises(NotImplementedError):
        bool_array.min_element()


def test_mean_1d():
    """Tests the mean value of an array and checks if the mean returns correct answear.
    Only needs to work for type int and float (not boolean).
    Returns:
    float: the mean value
    """ 
    assert int_array.mean_element() == 3.0
    assert float_array.mean_element() == 2.0
    with pytest.raises(NotImplementedError):
        bool_array.mean_element()


# Task 6:Additional tests for 2D Arrays (2 point)

int_array_2d = Array((2,2), 1,2,3,4)
float_array_2d = Array((1,3), 1.5,1.5,2.0)
bool_array_2d = Array((2,3), True,False,False,True,False,False)

def test_add_2d():
    assert int_array_2d + int_array_2d == Array((2,2), 2,4,6,8)
    assert int_array_2d + 1 == Array((2,2), 2,3,4,5)
    assert 2 + int_array_2d == Array((2,2), 3,4,5,6)
    assert float_array_2d + 5  == Array((1,3), 6.5,6.5,7.0)
    with pytest.raises(NotImplementedError):
        bool_array_2d + int_array_2d
        loat_array_2d + int_array_2d
    with pytest.raises(ValueError):
        int_array_2d + float_array_2d


def test_mult_2d():
    assert float_array_2d * 2 == Array((1,3), 3.0,3.0,4.0)
    assert int_array_2d * 5 == Array((2,2), 5,10,15,20)
    assert 5 * int_array_2d  == Array((2,2), 5,10,15,20)
    with pytest.raises(ValueError):
        int_array_2d * float_array_2d
    with pytest.raises(NotImplementedError):
        bool_array_2d * bool_array_2d
        int_array_2d * Array((2,2), 1,'2',3,4)

def test_same_2d():
    assert int_array_2d.is_equal(int_array_2d) == Array((2,2), True,True,True,True) 
    assert float_array_2d.is_equal(float_array_2d)  == Array((1,3), True,True,True)      
    assert bool_array_2d.is_equal(bool_array_2d)  == Array((2,3), True,True,True,True,True,True)

    assert int_array_2d.is_equal(6) == Array((2,2), False,False,False,False)
    assert int_array_2d.is_equal(3) == Array((2,2), False,False,True,False)
    assert float_array_2d.is_equal(1.5)  == Array((1,3), True,True,False)
    assert float_array_2d.is_equal(3.0)  == Array((1,3), False,False,False)
    with pytest.raises(ValueError):    
        int_array_2d.is_equal(Array((3,),1,2,3))
    with pytest.raises(TypeError):
        float_array_2d.is_equal('abc')


def test_mean_2d():
    assert int_array_2d.mean_element() == 2.5
    assert float_array_2d.mean_element() == 5.0/3
    with pytest.raises(NotImplementedError):
        bool_array_2d.mean_element()

if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
