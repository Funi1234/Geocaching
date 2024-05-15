import unittest
from Utils import decode_baudot, encode_baudot, xor_binary, lfsr_backwards

class TestUtils(unittest.TestCase):

    def test_decode_baudot(self):
        # Test decoding a simple Baudot code
        self.assertEqual(decode_baudot('00100 10000'), ' E')
        self.assertEqual(decode_baudot('00100 11011 10101 11111 10000'), " 6E")

    def test_encode_baudot(self):
        # Test encoding a simple message to Baudot code
        self.assertEqual(encode_baudot(' E'), '00100 10000 ')
        self.assertEqual(encode_baudot(' 6E'), '00100 11011 10101 11111 10000 ')

    def test_baudot(self):
        msg = "This is 1 test 2."
        encoded = encode_baudot(msg)

        decoded = decode_baudot(encoded)
        # Test encoding a simple message to Baudot code
        self.assertEqual(decoded, decoded)

    def test_xor_binary(self):
        # Test XOR of two binary strings
        self.assertEqual(xor_binary('1010', '0101'), '1111')
        self.assertEqual(xor_binary('1100', '1100'), '0000')

if __name__ == '__main__':
    unittest.main()