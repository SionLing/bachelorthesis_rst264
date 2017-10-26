class Seq_parameter_set_data(object):
    profile_idc = None
    constraint_set0_flag = None
    constraint_set1_flag = None
    constraint_set2_flag = None
    constraint_set3_flag = None
    constraint_set4_flag = None
    constraint_set5_flag = None
    # equal to 0
    reserved_zero_2bits = None
    level_idc = None
    seq_parameter_set_id = None

    chroma_format_idc = None

    separate_colour_plane_flag = None

    bit_depth_luma_minus8 = None
    bit_depth_chroma_minus8 = None
    qpprime_y_zero_transform_bypass_flag = None
    seq_scaling_matrix_present_flag = None
    seq_scaling_list_present_flag = []

    log2_max_frame_num_minus4 = None
    pic_order_cnt_type = None

    log2_max_pic_order_cnt_lsb_minus4 = None

    delta_pic_order_always_zero_flag = None
    offset_for_non_ref_pic = None
    offset_for_top_to_bottom_field = None
    num_ref_frames_in_pic_order_cnt_cycle = None
    offset_for_ref_frame = []

    max_num_ref_frames = None
    gaps_in_frame_num_value_allowed_flag = None
    pic_width_in_mbs_minus1 = None
    pic_height_in_map_units_minus1 = None
    frame_mbs_only_flag = None

    mb_adaptive_frame_field_flag = None

    direct_8x8_inference_flag = None
    frame_cropping_flag = None

    frame_crop_left_offset = None
    frame_crop_right_offset = None
    frame_crop_top_offset = None
    frame_crop_bottom_offset = None

    vui_parameters_present_flag = None











