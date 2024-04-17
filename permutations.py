import numpy as np
from random import randrange


class Permutation:
    # the class get an iterator and initializes an instance which represents
    # the permutation.
    # raises ValueError if the iterator doesn't make sense.
    def __init__(self, iterator):
        self.size = len(iterator)
        self.permutation = np.array(iterator)
        if any(np.logical_or(self.permutation > self.size, self.permutation < 1)):
            raise ValueError("Iterator should contain only numbers between 1 to its length.")
        self.permutation.setflags(write=False)

    def act(self, num):
        if num > self.size or num < 1:
            raise ValueError(f"Permutation can't act on {num}.")
        return self.permutation[num - 1]

    def inverse_act(self, num):
        if num > self.size or num < 1:
            raise ValueError(f"Permutation can't act on {num}.")
        for n, val in enumerate(self.permutation):
            if val == num:
                return n + 1

    def inverse(self):
        return self.__class__(tuple(self.inverse_act(n) for n in range(1, self.size + 1)))

    def __str__(self):
        return self.permutation.__str__()

    def __repr__(self):
        return self.permutation.__repr__()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return all(n == m for n, m in zip(self.permutation, other.permutation))

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.size != other.size:
            raise ValueError('Permutation sizes do not fit')

        return self.__class__(tuple(self.act(other.act(n)) for n in range(1, self.size + 1)))

    def __pow__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        perm = self

        if other < 0:
            perm = perm.inverse()
            other = -other

        returned_value = identity(self.size)
        for i in range(other):
            returned_value = returned_value * perm

        return returned_value

    def is_identity(self):
        return self == identity(self.size)

    def is_involution(self):
        return (self**2).is_identity()


def identity(size):
    return Permutation(range(1, size + 1))


def rand(size):
    return Permutation(np.random.permutation(np.arange(1, size + 1)))


def invo_count():
    a, b = 1, 2
    yield a
    yield b
    n = 3
    while True:
        a, b = b, b + (n - 1) * a
        yield b
        n += 1


def rand_involution(size):
    """Return a random (uniform) involution of size n."""

    # Set up main variables:
    # -- the count of involutions
    _cnt_involutions = [n for n, m in zip(invo_count(), range(size))]
    # -- the result so far as a list
    involution = list(range(1, size + 1))
    # -- the list of indices of unseen (not yet decided) elements.
    #    unseen[0:undecided_count] are unseen/undecided elements, in any order.
    unseen = involution.copy()
    undecided_count = size

    # Make an involution, progressing one or two elements at a time
    while undecided_count > 1:  # if only one element remains, it must be fixed
        # Decide whether current element (index undecided_count-1) is fixed
        if randrange(_cnt_involutions[undecided_count - 1]) < _cnt_involutions[undecided_count - 2]:
            # Leave the current element as fixed and mark it as seen
            undecided_count -= 1
        else:
            # In involution, swap current element with another not yet seen
            id_other = randrange(undecided_count - 1)
            other = unseen[id_other]
            current = unseen[undecided_count - 1]
            involution[current - 1], involution[other - 1] = (
                involution[other - 1], involution[current - 1])
            # Mark both elements as seen by removing from start of unseen[]
            unseen.pop(id_other)
            undecided_count -= 2

    return Permutation(involution)
