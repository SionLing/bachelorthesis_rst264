import unittest

from Helper.NALU_Parsing.parsing_helper import *


class slice_header_helper_TEST(unittest.TestCase):

    def test_bit_array2int(self):
        self.assertEqual(bit_array2int([0]),0)
        self.assertEqual(bit_array2int([1]),1)
        self.assertEqual(bit_array2int([1,1]),3)
        self.assertEqual(bit_array2int([1,0,1]),5)

        with self.assertRaises(ValueError):
            bit_array2int([1, 5, 1])


    def test_byte_array2bit_array(self):
        self.assertEqual(byte_array2bit_array(b''),[])
        self.assertEqual(byte_array2bit_array(b'\x18'),[0,0,0,1,1,0,0,0])
        self.assertEqual(byte_array2bit_array(b'\x42\x18'),[0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0])
        self.assertEqual(byte_array2bit_array(b'd'),[0,1,1,0,0,1,0,0])
        self.assertEqual(byte_array2bit_array(b'd\x18'),[0,1,1,0,0,1,0,0,0,0,0,1,1,0,0,0])


    def test_reduce_bit_array(self):
        self.assertEqual(reduce_bit_array(3,[1,1,1,0,0,0]),[0,0,0])

    def test_read_bits(self):
        self.assertEqual(read_bits(1,[1,0,1,0,1,0]),(1,[0,1,0,1,0]))
        self.assertEqual(read_bits(3,[1,0,1,0,1,0]),(5,[0,1,0]))

        with self.assertRaises(AssertionError):
            reduce_bit_array(10, [1, 1, 1, 0, 0, 0])

    def test_ue(self):
        self.assertEqual(ue([0, 0, 1, 0, 0, 1, 1]), (3, [1, 1]))
        self.assertEqual(ue([0, 0, 1, 1, 0, 1, 1]), (5, [1, 1]))
        self.assertEqual(ue([0, 0, 1, 1, 1, 1, 1]), (6, [1, 1]))
        self.assertEqual(ue([0, 1, 0, 0, 0, 1, 1]), (1, [0, 0, 1, 1]))
        self.assertEqual(ue([1]), (0, []))

    def test_se(self):
        self.assertEqual(ue([1]), (0, []))
        self.assertEqual(se([0, 0, 1, 0, 0, 1, 1]), (2, [1, 1]))
        self.assertEqual(se([0, 0, 1, 1, 0, 1, 1]), (3, [1, 1]))
        self.assertEqual(se([0, 0, 1, 1, 1, 1, 1]), (-3, [1, 1]))

    def test_remove_duplicates(self):
        input = [7654323455, 7654323451, 7654323451, 7654323451, 7654323453, 7654323454, 7654323454]
        expected = [7654323455, 7654323451, 7654323453, 7654323454]
        output = remove_duplicates(input)
        self.assertEqual(output,expected)


