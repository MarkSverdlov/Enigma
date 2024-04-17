from permutations.generation import cycle


class AlphabetEncrypter:
    def __init__(self, alphabet):
        self.alphabet = list(alphabet)
        self.size = len(self.alphabet)

    def encrypt_character(self, c):
        for a, i in zip(self.alphabet, range(1, self.size + 1)):
            if a == c:
                return i
        raise KeyError(f'{c} is not in alphabet.')

    def decrypt_character(self, n):
        return self.alphabet[n - 1]

    def encrypt(self, message):
        return [self.encrypt_character(c) for c in message]

    def decrypt(self, message):
        return ''.join([self.decrypt_character(n) for n in message])


class EnigmaLogic:
    def __init__(self, plugboard, rotors, reflector, offsets=None):
        self.plugboard = plugboard
        self.rotors = rotors
        self.reflector = reflector
        if not offsets:
            offsets = [0] * len(rotors)
        self.offsets = offsets
        self.size = self.reflector.size
        self.number_of_rotors = len(self.rotors)
        if not self.is_valid():
            raise ValueError("Enigma parts do not match.")

    def is_valid(self):
        if self.plugboard.size != self.size:
            return False

        for r in self.rotors:
            if r.size != self.size:
                return False

        if self.reflector.size != self.size:
            return False

        for o in self.offsets:
            if o >= self.size or o < 0:
                return False

        if len(self.offsets) != self.number_of_rotors:
            return False

        if len(self.rotors) != self.number_of_rotors:
            return False

        return True

    def _offset_rotor(self, rotor_num=1, n=1):
        o = self.offsets[rotor_num - 1]
        o += n

        # calculates the number of derived rotations for the next rotor.
        if n >= 0:
            derived_rotations = o // self.size
        else:
            derived_rotations = -(-o // self.size + 1)

        # set the new offset
        self.offsets[rotor_num - 1] = o % self.size

        # returns the number of derived rotations for next rotor.
        return derived_rotations

    def push_offset(self, n=1):
        for i in range(1, self.number_of_rotors + 1):
            n = self._offset_rotor(i, n)

    def calculate_permutation(self):
        permutation = self.plugboard
        t = cycle(self.size)
        i = self.reflector
        for r, o in zip(self.rotors, self.offsets):
            permutation = t ** -o * r * t ** o * permutation

        permutation = permutation ** -1 * i * permutation
        return permutation

    def encrypt_character(self, n):
        encrypted_character = self.calculate_permutation().act(n)
        self.push_offset()
        return encrypted_character

    def encrypt(self, message):
        encrypted_message = []
        for n in message:
            encrypted_message.append(self.encrypt_character(n))
        return encrypted_message

    def reset_offset(self):
        self.offsets = [0] * self.size


class Enigma:
    def __init__(self, logic, encrypter):
        self.logic = logic
        self.encrypter = encrypter

    def encrypt(self, message):
        numerical_message = self.encrypter.encrypt(message)
        numerical_message = self.logic.encrypt(numerical_message)
        return self.encrypter.decrypt(numerical_message)

    def reset_offset(self):
        self.logic.reset_offset()
