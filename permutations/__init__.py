import numpy as np


def identity(size):
    """generates a permutation which is equal to the identity of size {size}"""
    return Permutation(range(1, size + 1))


class Permutation:
    """This class represents a permutation of the numbers 1,...,n when n is
    chosen by the client by instantiation time."""
    def __init__(self, iterator):
        """Initializes the instance via an iterator supplied to it.
        Iterator must yield the numbers 1,...,n for some n in some order, otherwise
        ValueError is raised.
        The attribute which contains the permutation itself is set to be immutable."""
        self.size = len(iterator)
        self.permutation = np.array(iterator)
        if any(np.logical_or(self.permutation > self.size, self.permutation < 1)):
            raise ValueError("Iterator should contain only numbers between 1 to its length.")
        self.permutation.setflags(write=False)

    def act(self, num):
        """The method takes a number from 1,...,n as an argument
        and returns the action of the permutation on it."""
        if num > self.size or num < 1:
            raise ValueError(f"Permutation can't act on {num}.")
        return self.permutation[num - 1]

    def inverse_act(self, num):
        """The method takes a number from 1,...,n as an argument
        and returns the actions of the inverse of the permutation on it."""
        if num > self.size or num < 1:
            raise ValueError(f"Permutation can't act on {num}.")
        for n, val in enumerate(self.permutation):
            if val == num:
                return n + 1

    def inverse(self):
        """Calculate the inverse of the permutation"""
        inverted_permutation = list(self.inverse_act(n)
                                    for n in range(1, self.size + 1))
        return self.__class__(inverted_permutation)

    def __str__(self):
        return self.permutation.__str__()

    __repr__ = __str__

    def __eq__(self, other):
        """Two permutations are equal iff they are mathematically
        equivalent."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.size != other.size:
            raise ValueError('Permutation sizes do not match')

        return all(n == m for n, m in zip(self.permutation, other.permutation))

    def __mul__(self, other):
        """Returns the result of mathematical multiplication of permutations."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.size != other.size:
            raise ValueError('Permutation sizes do not match')

        calculated_permutation = list(self.act(other.act(n))
                                      for n in range(1, self.size + 1))

        return self.__class__(calculated_permutation)

    def __pow__(self, other):
        """Returns the result of mathematical exponentiation of permutations."""
        if not isinstance(other, int):
            return NotImplemented

        perm = self

        # if the exponent is negative, compute the inverse.
        if other < 0:
            perm = perm.inverse()
            other = -other

        calculated_permutation = identity(self.size)
        for i in range(other):
            calculated_permutation = calculated_permutation * perm

        return calculated_permutation

    def is_identity(self):
        """checks if the permutation is equal to the identity permutation."""
        return self == identity(self.size)

    def is_involution(self):
        """checks if the permutation is an involution, i.e. the self**2 is the identity."""
        return (self**2).is_identity()
