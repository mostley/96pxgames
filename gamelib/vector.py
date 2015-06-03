# -*- coding: utf8 -*-
# pylint: disable=no-member, invalid-name

"""vector.py: A simple little Vector class. Enabling basic 2D vector math. """

__author__ = "Sven Hecht"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Sven Hecht"
__email__ = "info@shdev.de"
__status__ = "Production"

from random import *
from math import *


class Vector(object):
    """ The Vector class can represent a direction or a position in 2-dimensional space

    Examples:
        ( Vector(2, 5) + Vector(3, 1.5) ).getNormalized()

    Args:
        x (number/tuple/list/Vector, Optional): Represents the x dimension of the vector.
            If the first argument is a Vector, tuple or list the x and y dimensions will be initialized.
            The default x value is 0
        y (number, Optional): Represents the y dimension of the vector. The default y value is 0
    """

    def __init__(self, x=0, y=0):
        """ Vector() """
        self.x = 0
        self.y = 0
        if isinstance(x, tuple) or isinstance(x, list):
            y = x[1]
            x = x[0]
        elif isinstance(x, Vector):
            y = x.y
            x = x.x

        self.set(x, y)

    @staticmethod
    def random(size=1):
        """ Creates a randomized Vector contained inside a square of the dimensions size x size.

            Args:
                size (number, Optional): Determines the max bounds of the new Random Vector. Default is 1.

            Returns:
                Vector: a new instance of type Vector
        """

        sizex = size
        sizey = size
        if isinstance(size, tuple) or isinstance(size, list):
            sizex = size[0]
            sizey = size[1]
        elif isinstance(size, Vector):
            sizex = size.x
            sizey = size.y
        return Vector(random() * sizex, random() * sizey)

    @staticmethod
    def randomUnitCircle():
        """ Creates a randomized unit Vector that lies on the unit circle (circle of radius 1).

            Returns:
                Vector: a new instance of type Vector
        """

        d = random()*pi
        return Vector(cos(d) * choice([1, -1]), sin(d) * choice([1, -1]))

    @staticmethod
    def distance(a, b):
        """ Calculates the distance between 2 Vectors

            Args:
                a (Vector): the "from" point
                b (Vector): the "to" point

            Returns:
                Number: a number representing the distance between the to vectors (if they represent points in space)
        """

        return (a - b).getLength()

    @staticmethod
    def angle(v1, v2):
        """ Calculates the angle in Radian between 2 Vectors

            Args:
                a (Vector): first vector
                b (Vector): second vector

            Returns:
                Number: a number in radian representing the angle between the to vectors.
        """

        return acos(v1.dotproduct(v2) / (v1.getLength() * v2.getLength()))

    @staticmethod
    def angleDeg(v1, v2):
        """ Calculates the angle in Degree between 2 Vectors

            Args:
                a (Vector): first vector
                b (Vector): second vector

            Returns:
                Number: a number in degree representing the angle between the to vectors.
        """

        return Vector.angle(v1, v2) * 180.0 / pi

    def set(self, x, y):
        """ Updates the dimensions of the Vector.

            Args:
                x (number): the new value for the x dimension
                y (number): the new value for the y dimension
        """

        self.x = x
        self.y = y
    
    def toArr(self):
        """ Creates an array of the form [x, y]

            Returns:
                Array: an array representing the Vector
        """

        return [self.x, self.y]

    def toInt(self):
        """ Casts the dimensions to int

            Returns:
                Vector: a new Vector instance containing integer dimensions
        """

        return Vector(int(self.x), int(self.y))

    def toIntArr(self):
        """ Casts the dimensions to int and creates an array of the form [x, y]

            Returns:
                Vector: an new array of the Vectors dimensions casted to integer
        """

        return self.toInt().toArr()

    def clone(self):
        """ Clones the current Vector

            Returns:
                Vector: A new instance of the Vector
        """

        return Vector(self.x, self.y)

    def getNormalized(self): 
        """ Creates a new normalized instance of the Vector

            Returns:
                Vector: A new instance of type Vector but normalized
        """

        if self.getLength() != 0:
            return self / self.getLength()
        else:
            return Vector(0, 0)

    def modulo(self, other):
        """ Calculates the modulo between this vector and the given value.

            Examples:
                Vector(16, 22).modulo( 5 )            => Vector(1, 2)
                Vector(13, 13).modulo( Vector(7, 5) ) => Vector(6, 3)
                Vector(13, 13).modulo( [7, 5] )       => Vector(6, 3)
                Vector(13, 13).modulo( (7, 5) )       => Vector(6, 3)

            Args:
                other (Vector/tuple/list/number): the value to perform the modulo function with

            Returns:
                Vector: A new Vector instance containing the calculated values
        """

        if isinstance(other, Vector):
            return Vector(self.x % other.x, self.y % other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x % other[0], self.y % other[1])
        else:
            return Vector(self.x % other, self.y % other)

    def dotproduct(self, other):
        """ Calculates the dot product between this vector and the given value.

            Args:
                other (Vector/tuple/list): the value to perform the dot product function with

            Returns:
                Vector: A new Vector instance containing the calculated values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif  isinstance(other, tuple) or isinstance(other, list):
            return self.x * other[0] + self.y * other[1]
        else:
            return NotImplemented

    def __add__(self, other):
        """ Calculates the sum between this vector and the given value.

            Examples:
                Vector(16, 22) + 5            => Vector(21, 27)
                Vector(13, 13) + Vector(7, 5) => Vector(20, 18)
                Vector(13, 13) + [7, 5]       => Vector(20, 18)
                Vector(13, 13) + (7, 5)       => Vector(20, 18)

            Args:
                other (Vector/tuple/list/number): the value to perform the add function with

            Returns:
                Vector: A new Vector instance containing the sum of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x + other[0], self.y + other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        """ Calculates the difference between this vector and the given value.

            Examples:
                Vector(16, 22) - 5            => Vector(11, 17)
                Vector(13, 13) - Vector(7, 5) => Vector( 6,  8)
                Vector(13, 13) - [7, 5]       => Vector( 6,  8)
                Vector(13, 13) - (7, 5)       => Vector( 6,  8)

            Args:
                other (Vector/tuple/list/number): the value to perform the substract function with

            Returns:
                Vector: A new Vector instance containing the difference of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        if  isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x - other[0], self.y - other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x - other, self.y - other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        """ Calculates the difference between the given value and this vector.

            Examples:
                5            - Vector(16, 22) => Vector(-11, -17)
                Vector(7, 5) - Vector(13, 13) => Vector( -6,  -8)
                [7, 5]       - Vector(13, 13) => Vector( -6,  -8)
                (7, 5)       - Vector(13, 13) => Vector( -6,  -8)

            Args:
                other (Vector/tuple/list/number): the value to perform the substract function with

            Returns:
                Vector: A new Vector instance containing the difference of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return Vector(other.x - self.x, other.y - self.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector(other[0] - self.x, other[1] - self.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(other - self.x, other - self.y)
        else:
            return NotImplemented

    def __mul__(self, other):
        """ Calculates the product between this vector and the given value.

            Examples:
                Vector(16, 22) * 5            => Vector(80, 110)
                Vector(13, 13) * Vector(7, 5) => Vector(91,  65)
                Vector(13, 13) * [7, 5]       => Vector(91,  65)
                Vector(13, 13) * (7, 5)       => Vector(91,  65)

            Args:
                other (Vector/tuple/list/number): the value to perform the multiply function with

            Returns:
                Vector: A new Vector instance containing the product of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x * other[0], self.y * other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __div__(self, other):
        """ Calculates the quotient between this vector and the given value.

            Examples:
                Vector(16,   22)   / 5            => Vector(  3,    4)
                Vector(12,   13)   / Vector(6, 5) => Vector(  2,    2)
                Vector(12,   13)   / [6, 5]       => Vector(  2,    2)
                Vector(12,   13)   / (6, 5)       => Vector(  2,    2)
                Vector(12.0, 13.0) / (6, 5)       => Vector(2.0,  2.6)

            Args:
                other (Vector/tuple/list/number): the value to perform the division function with

            Returns:
                Vector: A new Vector instance containing the quotient of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x / other[0], self.y / other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __rdiv__(self, other):
        """ Calculates the quotient between the given value and this vector.

            Examples:
                22.0               / Vector(16, 22) => Vector(1.375,  1.0)
                Vector(22.0, 25.0) / Vector(16,  5) => Vector(1.375,  5.0)
                [22.0, 25.0]       / Vector(16,  5) => Vector(1.375,  5.0)
                (22.0, 25.0)       / Vector(16,  5) => Vector(1.375,  5.0)
                (22, 25)           / Vector(16,  5) => Vector(1,      5)

            Args:
                other (Vector/tuple/list/number): the value to perform the division function with

            Returns:
                Vector: A new Vector instance containing the quotient of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return Vector(other.x / self.x, other.y / self.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector(other[0] / self.x, other[1] / self.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(other / self.x, other / self.y)
        else:
            return NotImplemented

    def __pow__(self, other):
        """ Calculates the power of this vector by the given value.

            Examples:
                Vector(6, 2) ** 5   => Vector(7776,   32)
                Vector(6, 2) ** 5.0 => Vector(7776.0, 32.0)

            Args:
                other (number): the value to perform the exponentiation with

            Returns:
                Vector: A new Vector instance containing the result of the calculation

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x ** other, self.y ** other)
        else:
            return NotImplemented

    def __iadd__(self, other):
        """ Calculates the sum between this vector and the given value in place.

            Examples:
                Vector(16, 22) += 5            => Vector(21, 27)
                Vector(13, 13) += Vector(7, 5) => Vector(20, 18)
                Vector(13, 13) += [7, 5]       => Vector(20, 18)
                Vector(13, 13) += (7, 5)       => Vector(20, 18)

            Args:
                other (Vector/tuple/list/number): the value to perform the add function with

            Returns:
                Vector: itself, containing the sum of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
            return self
        else:
            return NotImplemented

    def __isub__(self, other):
        """ Calculates the difference between this vector and the given value in place.

             Examples:
                Vector(16, 22) -= 5            => Vector(11, 17)
                Vector(13, 13) -= Vector(7, 5) => Vector( 6,  8)
                Vector(13, 13) -= [7, 5]       => Vector( 6,  8)
                Vector(13, 13) -= (7, 5)       => Vector( 6,  8)

            Args:
                other (Vector/tuple/list/number): the value to perform the substract function with

            Returns:
                Vector: itself, containing the difference of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x -= other[0]
            self.y -= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
            return self
        else:
            return NotImplemented

    def __imul__(self, other):
        """ Calculates the product between this vector and the given value in place.

            Examples:
                Vector(16, 22) *= 5            => Vector(80, 110)
                Vector(13, 13) *= Vector(7, 5) => Vector(91,  65)
                Vector(13, 13) *= [7, 5]       => Vector(91,  65)
                Vector(13, 13) *= (7, 5)       => Vector(91,  65)

            Args:
                other (Vector/tuple/list/number): the value to perform the multiply function with

            Returns:
                Vector: itself, containing the product of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x *= other[0]
            self.y *= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            return self
        else:
            return NotImplemented

    def __idiv__(self, other):
        """ Calculates the quotient between this vector and the given value in place.

            Examples:
                Vector(16,   22)   /= 5            => Vector(  3,    4)
                Vector(12,   13)   /= Vector(6, 5) => Vector(  2,    2)
                Vector(12,   13)   /= [6, 5]       => Vector(  2,    2)
                Vector(12,   13)   /= (6, 5)       => Vector(  2,    2)
                Vector(12.0, 13.0) /= (6, 5)       => Vector(2.0,  2.6)

            Args:
                other (Vector/tuple/list/number): the value to perform the division function with

            Returns:
                Vector: itself, containing the quotient of the values

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            self.x /= other.x
            self.y /= other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x /= other[0]
            self.y /= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
            return self
        else:
            return NotImplemented

    def __ipow__(self, other):
        """ Calculates the power of this vector by the given value in place.

            Examples:
                Vector(6, 2) **= 5   => Vector(7776,   32)
                Vector(6, 2) **= 5.0 => Vector(7776.0, 32.0)

            Args:
                other (number): the value to perform the exponentiation with

            Returns:
                Vector: itself, containing the result of the calculation

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, int) or isinstance(other, float):
            self.x **= other
            self.y **= other
            return self
        else:
            return NotImplemented

    def __eq__(self, other):
        """ The Equality comparer.

            Examples:
                Vector(6, 2) == Vector(6, 2) => True
                Vector(6, 2) == Vector(6, 3) => False

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Boolean: a bool representing the result of the comparison

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __ne__(self, other):
        """ The Unequality comparer.

            Examples:
                Vector(6, 2) != Vector(6, 2) => False
                Vector(6, 2) != Vector(6, 3) => True

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Boolean: a bool representing the result of the comparison

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return self.x != other.x or self.y != other.y
        else:
            return NotImplemented

    def __gt__(self, other):
        """ The greater than comparer.

            Examples:
                Vector(6, 2) > Vector(5, 1) => True
                Vector(6, 2) > Vector(7, 3) => False
                Vector(6, 2) > Vector(6, 2) => False

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Boolean: a bool representing the result of the comparison

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return self.getLength() > other.getLength()
        else:
            return NotImplemented

    def __ge__(self, other):
        """ The greater than equals comparer.

            Examples:
                Vector(6, 2) >= Vector(5, 1) => True
                Vector(6, 2) >= Vector(7, 3) => False
                Vector(6, 2) >= Vector(6, 2) => True

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Boolean: a bool representing the result of the comparison

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return self.getLength() >= other.getLength()
        else:
            return NotImplemented

    def __lt__(self, other):
        """ The less than comparer.

            Examples:
                Vector(6, 2) < Vector(5, 1) => False
                Vector(6, 2) < Vector(7, 3) => True
                Vector(6, 2) < Vector(6, 2) => False

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Boolean: a bool representing the result of the comparison

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return self.getLength() < other.getLength()
        else:
            return NotImplemented

    def __le__(self, other):
        """ The less than equals comparer.

            Examples:
                Vector(6, 2) <= Vector(5, 1) => False
                Vector(6, 2) <= Vector(7, 3) => True
                Vector(6, 2) <= Vector(6, 2) => True

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Boolean: a bool representing the result of the comparison

            Raises:
                NotImplemented for arguments of not accepted type
        """

        if isinstance(other, Vector):
            return self.getLength() <= other.getLength()
        else:
            return NotImplemented

    def __len__(self):
        """ Calculates the magnitude of the vector.

            Examples:
                len(Vector(1, 0)) => 1
                len(Vector(0, 2)) => 2

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Number: The magnitude of the vector
        """

        return int(sqrt(self.x**2 + self.y**2))

    def getLength(self):
        """ Calculates the magnitude of the vector.

            Examples:
                Vector(1, 0).getLength() => 1
                Vector(0, 2).getLength() => 2

            Args:
                other (Vector): the other Vector to compare this one to

            Returns:
                Number: The magnitude of the vector
        """

        return sqrt(self.x**2 + self.y**2)

    def __getitem__(self, key):
        if key == "x" or key == "X" or key == 0 or key == "0":
            return self.x
        elif key == "y" or key == "Y" or key == 1 or key == "1":
            return self.y

    def __str__(self):
        return "[x: %(x)f, y: %(y)f]" % self

    def __repr__(self):
        return "{'x': %(x)f, 'y': %(y)f}" % self

    def __neg__(self):
        return Vector(-self.x, -self.y)

