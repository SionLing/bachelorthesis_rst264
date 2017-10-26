from Data.pic_parameter_set_rbsp import *
from Helper.NALU_Parsing.parsing_helper_wrapper import *

import math


def parse_pic_parameter_set_data(bytes):
    pic_parameter_set = Pic_parameter_set_rbsp()

    parser = Parsing_helper_wrapper(bytes)

    pic_parameter_set.pic_parameter_set_id = parser.ue()

    pic_parameter_set.seq_parameter_set_id = parser.ue()

    pic_parameter_set.entropy_coding_mode_flag = parser.u(1)

    pic_parameter_set.bottom_field_pic_order_in_frame_present_flag = parser.u(1)

    pic_parameter_set.num_slice_groups_minus1 = parser.ue()

    if(pic_parameter_set.num_slice_groups_minus1 > 0):
        pic_parameter_set.slice_group_map_type = parser.ue()

        if(pic_parameter_set.slice_group_map_type == 0):
            for i in range(pic_parameter_set.num_slice_groups_minus1):
                pic_parameter_set.run_length_minus1[i] = parser.ue()

        elif(pic_parameter_set.slice_group_map_type == 2):
            for i in range(pic_parameter_set.num_slice_groups_minus1 - 1):
                pic_parameter_set.top_left[i] = parser.ue()
                pic_parameter_set.bottom_right[i] = parser.ue()

        elif (3 <= pic_parameter_set.slice_group_map_type <= 5):
            pic_parameter_set.slice_group_change_direction_flag = parser.u(1)
            pic_parameter_set.slice_group_change_rate_minus1 = parser.ue()

        elif (pic_parameter_set.slice_group_map_type == 6):
            pic_parameter_set.pic_size_in_map_units_minus1 = parser.ue()

            for i in range(pic_parameter_set.pic_size_in_map_units_minus1):
                length_of_slice_group_id = calculate_length_for_slice_group_id(pic_parameter_set.num_slice_groups_minus1)
                pic_parameter_set.slice_group_id[i] = parser.u(length_of_slice_group_id)

    pic_parameter_set.num_ref_idx_l0_default_active_minus1 = parser.ue()

    pic_parameter_set.num_ref_idx_l1_default_active_minus1 = parser.ue()

    pic_parameter_set.weighted_pred_flag = parser.u(1)

    pic_parameter_set.weighted_bipred_idc = parser.u(2)

    pic_parameter_set.pic_init_qp_minus26 = parser.se()

    pic_parameter_set.pic_init_qs_minus26 = parser.se()

    pic_parameter_set.chroma_qp_index_offset = parser.se()

    pic_parameter_set.deblocking_filter_control_present_flag = parser.u(1)

    pic_parameter_set.constrained_intra_pred_flag = parser.u(1)

    pic_parameter_set.redundant_pic_cnt_present_flag = parser.u(1)




    # TODO other fields if important

    return pic_parameter_set


def get_picture_parameter_set_by_slice_header(slice_header, pic_manager):
    pic_param_set_id = slice_header.pic_parameter_set_id
    return pic_manager.get_param_set_by_id(pic_param_set_id)

def calculate_length_for_slice_group_id(num_slice_groups_minus1):
    # The length of the slice_group_id[ i ] syntax element is Ceil( Log2( num_slice_groups_minus1 + 1 ) ) bits.
    math.ceil(math.log2(num_slice_groups_minus1 + 1))

