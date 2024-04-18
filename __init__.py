from permutations import Permutation as Perm
from permutations.generation import mirror
from logic import AlphabetEncrypter as Aenc
# sigma_0
# sigma_1
# sigma_2
# sigma_3
# iota


def calculate_enigma_permutation(k):
    s0 = Perm([2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15, 18, 17, 20, 19, 21, 22, 23, 24, 25, 26])
    t = Perm([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 1])
    s1 = Perm([10, 7, 4, 17, 15, 24, 21, 19, 3, 1, 13, 9, 6, 18, 22, 20, 16, 14, 5, 23, 11, 2, 12, 26, 25, 8])
    s2 = Perm([14, 20, 26, 16, 19, 6, 2, 15, 11, 13, 23, 18, 3, 10, 4, 9, 22, 12, 1, 5, 25, 21, 24, 8, 7, 17])
    s3 = Perm([10, 22, 9, 21, 2, 8, 20, 3, 4, 25, 1, 11, 5, 17, 26, 16, 15, 19, 7, 24, 14, 18, 13, 23, 6, 12])
    i = mirror(26)
    k1 = k // 26
    k2 = k1 // 26
    return (s0 ** -1 * t ** -k * s1 ** -1 * t ** (k - k1) * s2 ** -1 * t ** (k1 - k2) * s3 ** -1 * t ** k2
            * i * t ** -k2 * s3 * t ** (k2-k1) * s2 * t ** (k1 - k) * s1 * t ** k * s0)


def encrypt_character(c, k):
    s = calculate_enigma_permutation(k)
    enc = Aenc('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    n = enc.encrypt_character(c)
    n1 = s.act(n)
    c1 = enc.decrypt_character(n1)
    return c1


def demo():
    k = 0
    while True:
        c = input('Please enter a character (:q to exit): ')
        if c == ':q':
            break
        print('The character in enigma is: ' + encrypt_character(c, k))
        k = k + 1


demo()
