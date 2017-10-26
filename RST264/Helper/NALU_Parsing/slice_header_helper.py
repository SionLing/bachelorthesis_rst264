import scapy.all as scap

from Helper.NALU_Parsing.seq_parameter_set_helper import *
from Helper.access_unit_detection.access_unit_helper import *
from Data.slice_header import *


def parse_slice_header(nalu, seq_manager, pic_manager):
    slice_header = Slice_header()

    # print(repr(nalu))
    bytes = nalu[scap.Raw].load
    parser = Parsing_helper_wrapper(bytes,500)

    slice_header.first_mb_in_slice = parser.ue()
    slice_header.slice_type = parser.ue()
    slice_header.pic_parameter_set_id = parser.ue()

    seq_param_set = get_sequence_parameter_set_by_slice_header(slice_header, seq_manager, pic_manager)

    # separate_colour_plane_flag can be found in seq_param_set
    if(seq_param_set.separate_colour_plane_flag == 1):
        slice_header.colour_plane_id = parser.u(2)

    frame_num_length = get_frame_num_length(seq_param_set)
    slice_header.frame_num = parser.u(frame_num_length)

    if(seq_param_set.frame_mbs_only_flag != 1):
        slice_header.field_pic_flag = parser.u(1)
        if(slice_header.field_pic_flag == 1):
            slice_header.bottom_field_flag = parser.u(1)

    # if (clac_idrPicFlag(nalu) == 1):
    if (nalu.nalu_type == 5):
            slice_header.idr_pic_id == parser.ue()

    pic_param_set = get_picture_parameter_set_by_slice_header(slice_header, pic_manager)

    if (seq_param_set.pic_order_cnt_type == 0):
        pic_order_cnt_lsb_length = get_pic_order_cnt_lsb_length(seq_param_set)
        slice_header.pic_order_cnt_lsb = parser.u(pic_order_cnt_lsb_length)

        if(pic_param_set.bottom_field_pic_order_in_frame_present_flag == 1 and slice_header.field_pic_flag != 1):
            slice_header.delta_pic_order_cnt_bottom = parser.se()

    if (seq_param_set.pic_order_cnt_type == 1 and seq_param_set.delta_pic_order_always_zero_flag != 1):
        slice_header.delta_pic_order_cnt[0] = parser.se()

        if(pic_param_set.bottom_field_pic_order_in_frame_present_flag == 1 and slice_header.field_pic_flag != 1):
            slice_header.delta_pic_order_cnt[1] = parser.se()

    if (pic_param_set.redundant_pic_cnt_present_flag):
        slice_header.redundant_pic_cnt = parser.ue()




    # TODO further parsing, but for our purpose of finding the beginning and end of a pcp the parsing until this fields suffices
    end_of_parsing = parser.get_bits_size()

    return slice_header


def get_frame_num_length(seq_param_set):
    # frame_num is used as an identifier for pictures and shall be represented
    # by log2_max_frame_num_minus4 + 4 bits in the bitstream
    # (log2_max_frame_num_minus4 is a field of seq_param_set)
    log2_max_frame_num_minus4 = seq_param_set.log2_max_frame_num_minus4
    return log2_max_frame_num_minus4 + 4

def get_pic_order_cnt_lsb_length(seq_param_set):
    # The length of the pic_order_cnt_lsb syntax element
    # is log2_max_pic_order_cnt_lsb_minus4 + 4 bits
    # log2_max_pic_order_cnt_lsb_minus4 is a field of seq_param_set
    log2_max_pic_order_cnt_lsb_minus4 = seq_param_set.log2_max_pic_order_cnt_lsb_minus4
    return log2_max_pic_order_cnt_lsb_minus4 + 4