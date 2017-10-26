from Data.seq_parameter_set_data import *
from Helper.NALU_Parsing.pic_parameter_set_helper import *


def parse_seq_parameter_set_data(bytes):
    seq_parameter_set = Seq_parameter_set_data()

    parser = Parsing_helper_wrapper(bytes)

    # parsing profile_idc
    temp = parser.u(8)
    seq_parameter_set.profile_idc = temp

    # parsing constraint_set0_flag
    seq_parameter_set.constraint_set0_flag = parser.u(1)

    # parsing constraint_set1_flag
    seq_parameter_set.constraint_set1_flag = parser.u(1)

    # parsing constraint_set2_flag
    seq_parameter_set.constraint_set2_flag = parser.u(1)

    # parsing constraint_set3_flag
    seq_parameter_set.constraint_set3_flag = parser.u(1)

    # parsing constraint_set4_flag
    seq_parameter_set.constraint_set4_flag = parser.u(1)

    # parsing constraint_set5_flag
    seq_parameter_set.constraint_set5_flag = parser.u(1)

    # parsing reserved_zero_2bits
    seq_parameter_set.reserved_zero_2bits = parser.u(2)
    # should be 0 (see 7.3.2.1.1)
    assert (seq_parameter_set.reserved_zero_2bits == 0)

    # parsing level_idc
    seq_parameter_set.level_idc = parser.u(8)

    # parsing seq_parameter_set_id
    seq_parameter_set.seq_parameter_set_id = parser.ue()

    # if statement copied from 7.3.2.1.1
    if (seq_parameter_set.profile_idc == 100 or seq_parameter_set.profile_idc == 110 or
                seq_parameter_set.profile_idc == 122 or seq_parameter_set.profile_idc == 244 or seq_parameter_set.profile_idc == 44 or
                seq_parameter_set.profile_idc == 83 or seq_parameter_set.profile_idc == 86 or seq_parameter_set.profile_idc == 118 or
                seq_parameter_set.profile_idc == 128 or seq_parameter_set.profile_idc == 138 or seq_parameter_set.profile_idc == 139 or
                seq_parameter_set.profile_idc == 134 or seq_parameter_set.profile_idc == 135):
        seq_parameter_set.chroma_format_idc = parser.ue()

        if(seq_parameter_set.chroma_format_idc == 3):
            seq_parameter_set.separate_colour_plane_flag = parser.u(1)

        seq_parameter_set.bit_depth_luma_minus8 = parser.ue()
        seq_parameter_set.bit_depth_chroma_minus8 = parser.ue()
        seq_parameter_set.qpprime_y_zero_transform_bypass_flag = parser.u(1)
        seq_parameter_set.seq_scaling_matrix_present_flag = parser.u(1)

        if(seq_parameter_set.seq_scaling_matrix_present_flag == 1):
            i = 0
            while i < (8 if (seq_parameter_set.chroma_format_idc != 3) else 12):
                seq_parameter_set.seq_scaling_list_present_flag = parser.u(1)
                i += 1

    # parsing log2_max_frame_num_minus4
    seq_parameter_set.log2_max_frame_num_minus4 = parser.ue()

    # parsing pic_order_cnt_type
    seq_parameter_set.pic_order_cnt_type = parser.ue()

    if (seq_parameter_set.pic_order_cnt_type == 0 ):
        seq_parameter_set.log2_max_pic_order_cnt_lsb_minus4 = parser.ue()
    elif (seq_parameter_set.pic_order_cnt_type == 1 ):
        seq_parameter_set.delta_pic_order_always_zero_flag = parser.u(1)
        seq_parameter_set.offset_for_non_ref_pic = parser.se()
        seq_parameter_set.offset_for_top_to_bottom_field = parser.se()
        seq_parameter_set.num_ref_frames_in_pic_order_cnt_cycle = parser.ue()
        i = 0
        while(i < seq_parameter_set.num_ref_frames_in_pic_order_cnt_cycle):
            seq_parameter_set.offset_for_ref_frame.append(parser.se())
            i += 1

    seq_parameter_set.max_num_ref_frames = parser.ue()
    seq_parameter_set.gaps_in_frame_num_value_allowed_flag = parser.u(1)
    seq_parameter_set.pic_width_in_mbs_minus1 = parser.ue()
    seq_parameter_set.pic_height_in_map_units_minus1 = parser.ue()
    seq_parameter_set.frame_mbs_only_flag = parser.u(1)

    if(seq_parameter_set.frame_mbs_only_flag == 0):
        seq_parameter_set.mb_adaptive_frame_field_flag = parser.u(1)

    seq_parameter_set.direct_8x8_inference_flag = parser.u(1)
    seq_parameter_set.frame_cropping_flag = parser.u(1)

    if(seq_parameter_set.frame_cropping_flag == 1):
        seq_parameter_set.frame_crop_left_offset = parser.ue()
        seq_parameter_set.frame_crop_right_offset = parser.ue()
        seq_parameter_set.frame_crop_top_offset = parser.ue()
        seq_parameter_set.frame_crop_bottom_offset = parser.ue()

    seq_parameter_set.vui_parameters_present_flag = parser.u(1)

    # if(seq_parameter_set.vui_parameters_present_flag == 1):
    #     # TODO parse other fields
    #     assert(False)

    return seq_parameter_set


def get_sequence_parameter_set_by_slice_header(slice_header, seq_manager, pic_manager):
    pic_param_set = get_picture_parameter_set_by_slice_header(slice_header,pic_manager)
    seq_param_set_id = pic_param_set.seq_parameter_set_id
    return seq_manager.get_param_set_by_id(seq_param_set_id)


























