from permutations.generation import rand, mirror
from logic import AlphabetEncrypter, EnigmaLogic, Enigma


def mock_enigma():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,!?.'
    size = len(alphabet)
    encrypter = AlphabetEncrypter(alphabet)
    plugboard = rand(size)
    rotor1 = rand(size)
    rotor2 = rand(size)
    rotor3 = rand(size)
    reflector = mirror(size)
    machine = EnigmaLogic(plugboard, (rotor1, rotor2, rotor3), reflector)
    return Enigma(machine, encrypter)


def ui():
    enigma = mock_enigma()
    while True:
        data = input("INPUT (enter :q to exit, :r to reset offset): ")
        if data == ':r':
            enigma.reset_offset()
        elif data == ':q':
            break
        else:
            try:
                output = enigma.encrypt(data)
            except KeyError as e:
                print('Error: ' + e.args[0])
            else:
                print(output)


if __name__ == '__main__':
    ui()
