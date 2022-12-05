"""Array class for assignment 2
    by Assem Maratova
    assemm@uio.no
"""

# Implement the Array Class (6 points)
# Adapt your implementation to work with 2D Arrays (3 points)

class Array:

    def __init__(self, shape, *values):
        """Initialize an array of 1- or 2-dimensionality. Elements can only be of type:
        - int
        - float
        - bool
        Make sure the values and shape are of the correct type.
        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """  
        # Check if the values are of valid types
        # - get disticnt types of values into a list = value_types
        # - if len(value_types) != 1 => values are not of one type => ValueError
        # - if value_types[0] not one of int, float or bool => TypeError

        value_types = list(set([type(v) for v in [*values]]))
        if value_types[0] not in (int, float, bool):
            raise TypeError("Values must be of one type: int, float or bool.")
        elif len(value_types) != 1:
            raise ValueError("Array values must be of one type.")
        
        is_bool_array = value_types[0] == bool
        
        if not isinstance(shape, tuple):
                raise TypeError("Argument shape must be of type tuple.")

        shape_types = list(set([type(v) for v in shape]))
        if not shape_types[0] == int:
            raise TypeError("shape value(s) must be of one type: int.")
        elif len(shape_types) != 1:
            raise ValueError("shape value(s) must be of one type: int.")

        is_1D_array = len(shape)==1
        is_2D_array = len(shape)==2

        if is_1D_array:            
            # Check that the amount of values corresponds to the shape
            if not len([*values])==shape[0]:
                raise ValueError("The number of values does not fit with the shape.")
            # Set instance attributes
            array_values = [*values]    
        elif is_2D_array:        
            # Check that the amount of values corresponds to the shape
            if not len([*values])==shape[0]*shape[1]:
                raise ValueError("The number of values does not fit with the shape.")
            
            nrows = shape[0]
            ncols = shape[1]
            array_values = [[*values][i*ncols: (i+1)*ncols] for i in range(nrows)]
        else:
            raise TypeError("Argument shape must be of type tuple and length 1 or 2.")
        
        # Set instance attributes
        self.shape = shape
        self.values = array_values
        self.is_1D_array = is_1D_array # if False it is a 2D array 
        self.is_bool_array = is_bool_array # if False is in an array of numbers


    def __getitem__(self, index):
        """Makes the Array subscriptable.

        Returns:
            The return value. Element of the Array at the given index.

        """
        return self.values[index]
    
    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        if self.is_1D_array:
            return '['+','.join([str(v) for v in self.values])+']'
        else:
            return '['+',\n'.join([str(v) for v in self.values])+']'

    def flatten2d(self):
        """Flattens values of a 2D array. 
        In case of 1D array returns its values without any change.

        Returns:
            list: 1-dimensional list
        """
        if self.is_1D_array:
            return self.values
        
        flat_values = []
        for sublist in self.values:
            flat_values += sublist
        return flat_values

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.
        """
        # check that the method supports the given arguments (check for data type and shape of array)
        # if the array is a boolean you should return NotImplemented
        
        if self.is_bool_array:
            raise NotImplementedError("This method is not implemented for a boolean Array.")
            # return NotImplemented

        if isinstance(other, Array):
            if not other.shape == self.shape:
                raise ValueError("Arrays have different shapes.")
            elif other.is_bool_array:
                raise NotImplementedError("The method does not support given value types.")
                # return NotImplemented
            return Array(self.shape, *[v+w for v,w in zip(self.flatten2d(), other.flatten2d())])
        elif type(other) in (int, float):
            return Array(self.shape, *[v+other for v in self.flatten2d()])
        else:
            raise NotImplementedError("The method does not support given value types.")
            # return NotImplemented

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.
        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.
        """
        if self.is_bool_array:
            raise NotImplementedError("This method is not implemented for a boolean Array.")
            # return NotImplemented

        if isinstance(other, Array):
            if not other.shape == self.shape:
                raise ValueError("Arrays have different shapes.")
            elif other.is_bool_array:
                raise NotImplementedError("The method does not support given value types.")
                # return NotImplemented
            return Array(self.shape, *[v-w for v,w in zip(self.flatten2d(), other.flatten2d())])
        elif type(other) in (int, float):
            return Array(self.shape, *[v-other for v in self.flatten2d()])
        else:
            raise NotImplementedError("The method does not support given value types.")
            # return NotImplemented

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.
        """
        if self.is_bool_array:
            raise NotImplementedError("This method is not implemented for a boolean Array.")
            # return NotImplemented

        if isinstance(other, Array):
            if not other.shape == self.shape:
                raise ValueError("Arrays have different shapes.")
            elif other.is_bool_array:
                raise NotImplementedError("The method does not support given value types.")
                # return NotImplemented
            return Array(self.shape, *[w-v for v,w in zip(self.flatten2d(), other.flatten2d())])
        elif type(other) in (int, float):
            return Array(self.shape, *[other-v for v in self.flatten2d()])
        else:
            raise NotImplementedError("The method does not support given value types.")
            # return NotImplemented

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if self.is_bool_array:
            raise NotImplementedError("This method is not implemented for a boolean Array.")
            # return NotImplemented

        if isinstance(other, Array):
            if not other.shape == self.shape:
                raise ValueError("Arrays have different shapes.")
            elif other.is_bool_array:
                raise NotImplementedError("The method does not support given value types.")
                # return NotImplemented
            return Array(self.shape, *[v*w for v,w in zip(self.flatten2d(), other.flatten2d())])
        elif type(other) in (int, float):
            return Array(self.shape, *[v*other for v in self.flatten2d()])
        else:
            raise NotImplementedError("The method does not support given value types.")
            # return NotImplemented

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.
        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.
        """
                
        if isinstance(other, Array):
            if other.shape == self.shape:
                return self.values == other.values
            else:
                return False
        else:
            return False

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an Array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an Array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An Array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.
        """

        if isinstance(other, Array):
            if not other.shape == self.shape:
                raise ValueError("Arrays have different shapes.")
            return Array(self.shape, *[v == w for v,w in zip(self.flatten2d(), other.flatten2d())])
        elif type(other) in (int, float):
            return Array(self.shape, *[v == other for v in self.flatten2d()])
        else:
            raise TypeError("This type is not supported.")

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.
        """

        if self.is_bool_array:
            raise NotImplementedError("This method is not implemented for a boolean Array.")        
        else:
            return float(min(self.flatten2d()))

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """

        if self.is_bool_array:
            raise NotImplementedError("This method is not implemented for a boolean Array.")        
        else:
            if self.is_1D_array:
                return float(sum(self.values)/self.shape[0])
            else:
                return sum(self.flatten2d())/(self.shape[0]*self.shape[1])