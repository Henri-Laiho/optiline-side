from bitarray import bitarray


def string_to_bitarray(string):
    byteStr = txt.encode(encoding="ascii", errors="backslashreplace")
    bits = bitarray()
    bits.frombytes(byteStr)
    return bits


def string_to_list_of_bits(string):
    return [1 if x else 0 for x in string_to_bitarray(string)]


def bitarray_to_string(bitarr):
    return bitarr.tobytes().decode("ascii")


def list_of_bits_to_string(listOfBits):
    return bitarray(listOfBits).tobytes().decode("ascii")


txt = "Hello World!"
print(bitarray_to_string(string_to_bitarray(txt)))
print(list_of_bits_to_string(string_to_list_of_bits(txt)))
