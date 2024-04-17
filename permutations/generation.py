import numpy as np
from random import randrange
from . import Permutation, identity


def rand(size):
    """generates a random permutation of size {size}"""
    return Permutation(np.random.permutation(np.arange(1, size + 1)))


def invo_count():
    """a generator which yields the number of involutions in a given size.
    used to randomize an involution uniformly."""
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


def mirror(size):
    """returns the involution n,...,1"""
    return Permutation(range(size, 0, -1))


def cycle(size):
    """returns the permutation 2,3,4,...,n-1,n,1"""
    permutation = list(range(2, size + 1))
    permutation.append(1)
    return Permutation(permutation)
