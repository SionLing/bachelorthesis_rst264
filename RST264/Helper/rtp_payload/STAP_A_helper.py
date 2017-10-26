from struct import *

from Data.NALU import NAL_unit

CURRENT_NALU_TYPE = 24

FIXED_NALU_HEADER_LENGTH = 1  # in Byte
FIXED_NALU_SIZE_LENGTH = 2  # in Byte

def extract_actual_nalus(nalu):
    assert (nalu.nalu_type == CURRENT_NALU_TYPE)

    payload = nalu.payload.load
    payload_length = len(payload)

    nalu_array = []

    current_start_index = 0
    current_nalu_size = 0

    while(current_start_index < payload_length):
        current_nalu_size_data = payload[current_start_index: current_start_index + FIXED_NALU_SIZE_LENGTH]
        current_nalu_size = unpack('!H', current_nalu_size_data)[0]

        current_start_index += FIXED_NALU_SIZE_LENGTH

        nalu_data = payload[current_start_index: current_start_index + current_nalu_size]
        current_start_index += current_nalu_size

        nalu_array.append(NAL_unit(nalu_data))

    return nalu_array

def put_multiple_nalus_in_stap_a(current_index,access_unit,default_payload_size,size_list):
    if size_list:
        size = size_list.pop(0)
    else:
        size = default_payload_size

    num_of_nalus = get_number_of_nalus_to_fit_in_stap_a(current_index,access_unit,size)

    STAPA_nalu = NAL_unit()

    STAPA_nalu.forbidden_zero = 0
    STAPA_nalu.nal_ref_idc = 0
    STAPA_nalu.nalu_type = 24

    STAPA_nalu.payload = create_payload(num_of_nalus,current_index,access_unit)

    return [STAPA_nalu]

def get_number_of_nalus_to_fit_in_stap_a(current_index,access_unit,size):
    current_nalu_raw = scapy_packet_to_raw_bytes(access_unit[current_index])
    current_length = 0
    number_of_nalus = 0
    while(current_length + len(current_nalu_raw) <= size and (current_index + number_of_nalus) < len(access_unit) - 1):
        current_length += len(current_nalu_raw)
        number_of_nalus += 1
        current_nalu_raw = scapy_packet_to_raw_bytes(access_unit[current_index + number_of_nalus])

    return number_of_nalus

def create_payload(num_of_nalus,current_index,access_unit):
    payload = b''
    for i in range(num_of_nalus):
        nalu = access_unit[current_index + i]
        raw_nalu = scapy_packet_to_raw_bytes(nalu)
        len_nalu = len(raw_nalu)
        payload += (len_nalu).to_bytes(2, byteorder='big')
        payload += raw_nalu
    return payload

def scapy_packet_to_raw_bytes(packet):
    return bytes(packet)

