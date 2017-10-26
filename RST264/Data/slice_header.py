class Slice_header(object):
    first_mb_in_slice = None
    slice_type = None
    pic_parameter_set_id = None

    colour_plane_id = None

    frame_num = None

    field_pic_flag = None

    bottom_field_flag = None

    idr_pic_id = None

    pic_order_cnt_lsb = None

    delta_pic_order_cnt_bottom = None

    delta_pic_order_cnt = []

    # wenn nicht gesetzt wird, dann nach ITU Standard als 0 zu interpretieren
    redundant_pic_cnt = 0




