import unittest

from Helper.rtp_payload.STAP_B_helper import *


class STAP_B_helper_TEST(unittest.TestCase):

    def test_extract_actual_nalus1(self):
        bytes = b'\x19\x00\x01\x00\x03\x61\xFF\xFF'

        expectedArray = []
        expectedArray.append((1, NAL_unit(b'\x61\xFF\xFF')))

        array = extract_actual_nalus(NAL_unit(bytes))

        self.assertEqual(expectedArray,array,"Parsing failure while parsing STAP_B")

    def test_extract_actual_nalus2(self):
        bytes = b'\x19\x00\x01\x00\x03\x61\xFF\xFF\x00\x05\x42\xFF\xFF\xFF\xFF'

        expectedArray = []
        expectedArray.append((1, NAL_unit(b'\x61\xFF\xFF')))
        expectedArray.append((2, NAL_unit(b'\x42\xFF\xFF\xFF\xFF')))

        array = extract_actual_nalus(NAL_unit(bytes))

        self.assertEqual(expectedArray, array, "Parsing failure while parsing STAP_B")
