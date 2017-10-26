from Data.NALU import NAL_unit
import scapy.all as scap



def form_one_NALU(nalu_list):
    first_fragment = nalu_list[0]
    last_fragment = nalu_list[-1]

    assert (last_fragment.FU_A_Header_E == 1)
    assert (first_fragment.FU_A_Header_S == 1)
    assert (first_fragment.forbidden_zero == last_fragment.forbidden_zero)
    assert (first_fragment.nal_ref_idc == last_fragment.nal_ref_idc)
    assert (first_fragment.FU_A_Header_actual_nalu_type == last_fragment.FU_A_Header_actual_nalu_type)

    new_nalu_payload = b""
    for current_nalu in nalu_list:
        new_nalu_payload += current_nalu.payload.load

    new_nalu = NAL_unit() / new_nalu_payload
    new_nalu.forbidden_zero = first_fragment.forbidden_zero
    new_nalu.nal_ref_idc = first_fragment.nal_ref_idc
    new_nalu.nalu_type = first_fragment.FU_A_Header_actual_nalu_type
    # print("created new: " + repr(new_nalu))

    return new_nalu

# the size is the size of the nalu payload per FU-A Unit in bytes
def fragment_nalu_into_FUAs_with_specific_size(unfragmented_nalu, default_size, size_list = []):

    actual_nalu_type = unfragmented_nalu.nalu_type
    actual_nalu_f_bit = unfragmented_nalu.forbidden_zero
    actual_nalu_nal_ref_idc = unfragmented_nalu.nal_ref_idc
    actual_nalu_payload = unfragmented_nalu[scap.Raw].load
    actual_nalu_payload_length = len(actual_nalu_payload)

    size = default_size
    if size_list:
        size = size_list[0]

    # to fragment a nalu in at least 2 packtes it has to have a bigger size than the given size for fragmentation:
    assert(size < actual_nalu_payload_length)
    # moreover the size has to be at least 1
    assert (size >= 1)

    FUA_list = []

    start = True
    end = False
    while(not end):
        if size_list:
            size = size_list.pop(0)
        else:
            size = default_size
        if(len(actual_nalu_payload) <= size):
            end = True
        current_payload = actual_nalu_payload[:size]
        actual_nalu_payload = del_first_elems(actual_nalu_payload, size)
        current_FUA = create_FUA_nalu(current_payload, actual_nalu_f_bit, actual_nalu_nal_ref_idc, actual_nalu_type,
                                      start, end)
        FUA_list.append(current_FUA)
        if (start):
            start = False
    return FUA_list

def create_FUA_nalu(payload, fbit, actual_nalu_nal_ref_idc, actual_nalu_type, start, end):
    FUA_nalu = NAL_unit()

    FUA_nalu.forbidden_zero = fbit
    FUA_nalu.nal_ref_idc = actual_nalu_nal_ref_idc
    # FU-A -> nalu-type 28
    FUA_nalu.nalu_type = 28

    FUA_nalu.FU_A_Header_S = 1 if start else 0
    FUA_nalu.FU_A_Header_E = 1 if end else 0
    FUA_nalu.FU_A_Header_R = 0
    FUA_nalu.FU_A_Header_actual_nalu_type = actual_nalu_type

    FUA_nalu.payload = payload

    return FUA_nalu

def del_first_elems(bytes_object, number_of_elems):
    return bytes_object[number_of_elems:]




























