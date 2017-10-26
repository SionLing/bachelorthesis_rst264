import unittest

from Helper.rtp_payload.FU_A_helper import *


def create_test_nalu_array():
    first_nalu = NAL_unit() / b'\xFF\xFF'
    first_nalu.nal_ref_idc = 2
    first_nalu.nalu_type = 28
    first_nalu.FU_A_Header_S = 1
    first_nalu.FU_A_Header_E = 0
    first_nalu.FU_A_Header_R = 0
    first_nalu.FU_A_Header_actual_nalu_type = 1
    # print("created: " + repr(first_nalu))

    second_nalu = NAL_unit() / b'\xFF\xFF'
    second_nalu.nal_ref_idc = 2
    second_nalu.nalu_type = 28
    second_nalu.FU_A_Header_S = 0
    second_nalu.FU_A_Header_E = 0
    second_nalu.FU_A_Header_R = 0
    second_nalu.FU_A_Header_actual_nalu_type = 1
    # print("created: " + repr(second_nalu))

    third_nalu = NAL_unit() / b'\xFF\xFF'
    third_nalu.nal_ref_idc = 2
    third_nalu.nalu_type = 28
    third_nalu.FU_A_Header_S = 0
    third_nalu.FU_A_Header_E = 1
    third_nalu.FU_A_Header_R = 0
    third_nalu.FU_A_Header_actual_nalu_type = 1
    # print("created: " + repr(third_nalu))

    return [first_nalu,second_nalu,third_nalu]

def create_expected_nalu():
    ret = NAL_unit() / b'\xFF\xFF\xFF\xFF\xFF\xFF'
    ret.forbidden_zero = 0
    ret.nal_ref_idc = 2
    ret.nalu_type = 1
    # print("created exp: " + repr(ret))
    return ret

def create_nalu_to_fragment():
    ret = NAL_unit() / b'\xFF\xFF\xAA\xAA\x00\x00\xBB\xBB'
    ret.forbidden_zero = 0
    ret.nal_ref_idc = 2
    ret.nalu_type = 1
    return ret

def create_expected_fu_a_stram_size4():
    ret_list = []

    nalu1 = NAL_unit() / b'\xFF\xFF\xAA\xAA'
    nalu1.forbidden_zero = 0
    nalu1.nal_ref_idc = 2
    # 28 -> FU-A
    nalu1.nalu_type = 28

    nalu1.FU_A_Header_S = 1
    nalu1.FU_A_Header_E = 0
    nalu1.FU_A_Header_R = 0
    nalu1.FU_A_Header_actual_nalu_type = 1
    ret_list.append(nalu1)

    nalu2 = NAL_unit() / b'\x00\x00\xBB\xBB'
    nalu2.forbidden_zero = 0
    nalu2.nal_ref_idc = 2
    # 28 -> FU-A
    nalu2.nalu_type = 28

    nalu2.FU_A_Header_S = 0
    nalu2.FU_A_Header_E = 1
    nalu2.FU_A_Header_R = 0
    nalu2.FU_A_Header_actual_nalu_type = 1
    ret_list.append(nalu2)

    return ret_list

def create_expected_fu_a_stram_size3():
    ret_list = []

    nalu1 = NAL_unit() / b'\xFF\xFF\xAA'
    nalu1.forbidden_zero = 0
    nalu1.nal_ref_idc = 2
    # 28 -> FU-A
    nalu1.nalu_type = 28

    nalu1.FU_A_Header_S = 1
    nalu1.FU_A_Header_E = 0
    nalu1.FU_A_Header_R = 0
    nalu1.FU_A_Header_actual_nalu_type = 1
    ret_list.append(nalu1)

    nalu2 = NAL_unit() / b'\xAA\x00\x00'
    nalu2.forbidden_zero = 0
    nalu2.nal_ref_idc = 2
    # 28 -> FU-A
    nalu2.nalu_type = 28

    nalu2.FU_A_Header_S = 0
    nalu2.FU_A_Header_E = 0
    nalu2.FU_A_Header_R = 0
    nalu2.FU_A_Header_actual_nalu_type = 1
    ret_list.append(nalu2)

    nalu3 = NAL_unit() / b'\xBB\xBB'
    nalu3.forbidden_zero = 0
    nalu3.nal_ref_idc = 2
    # 28 -> FU-A
    nalu3.nalu_type = 28

    nalu3.FU_A_Header_S = 0
    nalu3.FU_A_Header_E = 1
    nalu3.FU_A_Header_R = 0
    nalu3.FU_A_Header_actual_nalu_type = 1
    ret_list.append(nalu3)
    return ret_list

class FU_A_helper_TEST(unittest.TestCase):

    def test_form_nalu(self):
        test_nalus = create_test_nalu_array()
        expected_nalu = create_expected_nalu()
        created_nalu = form_one_NALU(test_nalus)

        self.assertEqual(expected_nalu,created_nalu,"Parsing failure while parsing FU_A")

    def test_fragment_nalu_into_FUAs_with_specific_size_4(self):
        nalu_to_be_fragmented = create_nalu_to_fragment()

        method_result_size4 = fragment_nalu_into_FUAs_with_specific_size(nalu_to_be_fragmented,4)
        expected_result_size4 = create_expected_fu_a_stram_size4()

        self.assertEqual(method_result_size4, expected_result_size4,"The creation of a FU-A Stream does not work correctly")

    def test_fragment_nalu_into_FUAs_with_specific_size_3(self):
        nalu_to_be_fragmented = create_nalu_to_fragment()

        method_result_size3 = fragment_nalu_into_FUAs_with_specific_size(nalu_to_be_fragmented, 3)
        expected_result_size3 = create_expected_fu_a_stram_size3()

        self.assertEqual(method_result_size3, expected_result_size3, "The creation of a FU-A Stream does not work correctly")

    def test_fragment_nalu_into_FUAs_with_specific_size_asserts(self):
        nalu_to_be_fragmented = create_nalu_to_fragment()

        with self.assertRaises(AssertionError):
            fragment_nalu_into_FUAs_with_specific_size(nalu_to_be_fragmented, 10)

        with self.assertRaises(AssertionError):
            fragment_nalu_into_FUAs_with_specific_size(nalu_to_be_fragmented, 0)





























