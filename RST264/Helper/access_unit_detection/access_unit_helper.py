from Helper.NALU_Parsing.slice_header_helper import *

def start_of_new_access_unit(prev_nalu, current_nalu, seq_manager, pic_manager):
    if (prev_nalu is None):
        return False
    elif (start_of_access_unit_by_nalu_types(prev_nalu,current_nalu)):
        return True
    else:
        return beginning_of_pcp(prev_nalu, current_nalu, seq_manager, pic_manager)



def start_of_access_unit_by_nalu_types(prev_nalu, current_nalu):
    # Access unit delimiter(9)
    if (current_nalu.nalu_type == 9):
        return True
    # if the current NALU is a Sequence parameter set(7) and the prev isn't a Access unit delimiter(9)
    elif (prev_nalu.nalu_type != 9 and current_nalu.nalu_type == 7):
        return True
    # if the current NALU is a Picture parameter set(8) and the prev isn't a Sequence parameter set(7) or a Access unit delimiter(9)
    elif (prev_nalu.nalu_type != 9 and prev_nalu.nalu_type != 7 and current_nalu.nalu_type == 8):
        return True
    # if the current NALU is a Supplemental enhancement information(6) and the prev isn't a Picture parameter set(8) or a Sequence parameter set(7) or a Access unit delimiter(9)
    elif (not (7 <= prev_nalu.nalu_type <= 9) and current_nalu.nalu_type == 6):
        return True
    # if the current NALU type is in range 14...18 and the prev isn't a Picture parameter set(8) or a Sequence parameter set(7) or a Access unit delimiter(9) or a Supplemental enhancement information(6)
    elif (not (7 <= prev_nalu.nalu_type <= 9) and  (14 <= current_nalu.nalu_type <= 18)):
        return True
    else:
        return False

# Diese Funktioin findet nur zuverlässig den Beginn eines PCP, wenn ausgeschlosssen ist, dass NALUs vom TYP 3 oder 4 die ersten eines PCP sein können
def beginning_of_pcp(prev_nalu, current_nalu, seq_manager, pic_manager):
    result = False

    if((1 <= current_nalu.nalu_type <= 2 or current_nalu.nalu_type == 5 )
       and (1 <= prev_nalu.nalu_type <= 2 or prev_nalu.nalu_type == 5)):
        prev_slice_header = parse_slice_header(prev_nalu, seq_manager, pic_manager)
        current_slice_header = parse_slice_header(current_nalu, seq_manager, pic_manager)

        result =  check_indicator_1(prev_slice_header,current_slice_header) \
               or check_indicator_2(prev_slice_header,current_slice_header) \
               or check_indicator_3(prev_slice_header,current_slice_header) \
               or check_indicator_4(prev_slice_header,current_slice_header) \
               or check_indicator_5(prev_nalu,current_nalu) \
               or check_indicator_6(prev_slice_header, current_slice_header, seq_manager, pic_manager) \
               or check_indicator_7(prev_slice_header, current_slice_header, seq_manager, pic_manager) \
               or check_indicator_8(prev_nalu,current_nalu) \
               or check_indicator_9(prev_nalu, current_nalu,prev_slice_header, current_slice_header)
    return result

def clac_idrPicFlag(nalu):
    # specified on page 65 in ITU document
    return  nalu.nalu_type == 5

def get_pic_order_cnt_type(current_slice_header, seq_manager, pic_manager):
    seq_param_set = get_sequence_parameter_set_by_slice_header(current_slice_header, seq_manager, pic_manager)
    return seq_param_set.pic_order_cnt_type

def check_indicator_1(prev_slice_header, current_slice_header):
    # frame_num differs in value (slice_header)
    return prev_slice_header.frame_num != current_slice_header.frame_num

def check_indicator_2(prev_slice_header, current_slice_header):
    # pic_parameter_set_id differs in value (slice_header)
    return prev_slice_header.pic_parameter_set_id != current_slice_header.pic_parameter_set_id

def check_indicator_3(prev_slice_header, current_slice_header):
    # field_pic_flag differs in value (slice_header)
    return prev_slice_header.field_pic_flag != current_slice_header.field_pic_flag

def check_indicator_4(prev_slice_header, current_slice_header):
    # bottom_field_flag is present in both and differs in value (slice_header)
    return ((not(prev_slice_header.bottom_field_flag is None))
            and (not(current_slice_header.bottom_field_flag is None))
            and prev_slice_header.bottom_field_flag != current_slice_header.bottom_field_flag)

def check_indicator_5(prev_nalu,current_nalu):
    # nal_ref_idc differs in value with one of the nal_ref_idc values being equal to 0 (NALU_header)
    return ((prev_nalu.nal_ref_idc == 0 or current_nalu.nal_ref_idc == 0)
            and prev_nalu.nal_ref_idc != current_nalu.nal_ref_idc)

def check_indicator_6(prev_slice_header, current_slice_header, seq_manager, pic_manager):
    seq_parameter_set_prev = get_sequence_parameter_set_by_slice_header(prev_slice_header, seq_manager, pic_manager)
    seq_parameter_set_current = get_sequence_parameter_set_by_slice_header(current_slice_header, seq_manager, pic_manager)

    # pic_order_cnt_type (seq_param-set) is equal to 0 for both and either pic_order_cnt_lsb (slice_header)
    # differs in value, or delta_pic_order_cnt_bottom differs in value. (slice_header)

    return seq_parameter_set_prev.pic_order_cnt_type == 0 \
           and seq_parameter_set_current.pic_order_cnt_type == 0 \
           and ((current_slice_header.pic_order_cnt_lsb != prev_slice_header.pic_order_cnt_lsb)
                or (current_slice_header.delta_pic_order_cnt_bottom != prev_slice_header.delta_pic_order_cnt_bottom))

def check_indicator_7(prev_slice_header, current_slice_header, seq_manager, pic_manager):
    # pic_order_cnt_type (seq_param-set) is equal to 1 for both and either delta_pic_order_cnt[ 0 ] (slice_header)
    # differs in value, or delta_pic_order_cnt[ 1 ] (slice_header) differs in value.
    seq_parameter_set_prev = get_sequence_parameter_set_by_slice_header(prev_slice_header, seq_manager, pic_manager)
    seq_parameter_set_current = get_sequence_parameter_set_by_slice_header(current_slice_header, seq_manager, pic_manager)

    return seq_parameter_set_prev.pic_order_cnt_type == 1 \
           and seq_parameter_set_current.pic_order_cnt_type == 1 \
           and ((current_slice_header.delta_pic_order_cnt[0] != prev_slice_header.delta_pic_order_cnt[0])
                or (current_slice_header.delta_pic_order_cnt[1] != prev_slice_header.delta_pic_order_cnt[1]))

def check_indicator_8(prev_nalu, current_nalu):
    # IdrPicFlag differs in value. (berechnung nach Seite 87)
    idrPicFlag_current_nalu = clac_idrPicFlag(current_nalu)
    idrPicFlag_prev_nalu = clac_idrPicFlag(prev_nalu)
    return idrPicFlag_current_nalu != idrPicFlag_prev_nalu

def check_indicator_9(prev_nalu, current_nalu,prev_slice_header, current_slice_header):
    # IdrPicFlag is equal to 1 for both and idr_pic_id differs in value. (berechnung^ bzw. slice_header)
    idrPicFlag_current_nalu = clac_idrPicFlag(current_nalu)
    idrPicFlag_prev_nalu = clac_idrPicFlag(prev_nalu)
    return (idrPicFlag_current_nalu == 1 and idrPicFlag_prev_nalu == 1
            and current_slice_header.idr_pic_id != prev_slice_header.idr_pic_id)


def get_redundant_pic_cnt(nalu, pic_manager, seq_manager):
    slice_header = parse_slice_header(nalu, seq_manager, pic_manager)
    return slice_header.redundant_pic_cnt































