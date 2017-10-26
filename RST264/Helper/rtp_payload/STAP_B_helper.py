from struct import *

from Data.NALU import NAL_unit

CURRENT_NALU_TYPE = 25

FIXED_NALU_HEADER_LENGTH = 1  # in Byte
FIXED_NALU_SIZE_LENGTH = 2  # in Byte
FIXED_DON_LENGTH = 2  # in Byte


def extract_actual_nalus(nalu):
    assert (nalu.nalu_type == CURRENT_NALU_TYPE)

    payload = nalu.payload.load
    payload_length = len(payload)

    don_value_data = payload[:FIXED_DON_LENGTH]
    don_value = unpack('!H', don_value_data)[0]

    current_don = don_value

    current_nalu_size_data = payload[FIXED_DON_LENGTH:FIXED_NALU_SIZE_LENGTH + FIXED_DON_LENGTH]
    current_nalu_size = unpack('!H', current_nalu_size_data)[0]

    current_start_index = 0

    nalu_array = []

    first_nalu = True

    while (current_start_index + current_nalu_size + FIXED_NALU_SIZE_LENGTH <= payload_length):
        if (first_nalu):
            nalu_size_start_index = current_start_index + FIXED_DON_LENGTH
            first_nalu = not first_nalu
        else:
            nalu_size_start_index = current_start_index
        nalu_header_start_index = nalu_size_start_index + FIXED_NALU_SIZE_LENGTH
        nalu_payload_start_index = nalu_header_start_index + FIXED_NALU_HEADER_LENGTH

        current_nalu_size_data = payload[nalu_size_start_index:nalu_header_start_index]
        current_nalu_size = unpack('!H', current_nalu_size_data)[0]

        nalu_end_index = nalu_header_start_index + current_nalu_size

        nalu_data = payload[nalu_header_start_index:nalu_end_index]
        nalu = NAL_unit(nalu_data)

        nalu_array.append((current_don, nalu))

        current_start_index = nalu_end_index
        current_don = (current_don + 1) % 65536

    return nalu_array
