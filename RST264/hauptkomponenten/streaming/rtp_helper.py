from Helper.rtp_payload.FU_A_helper import *
from Helper.rtp_payload.STAP_A_helper import *

import scapy.all as scap

class RTP_helper(object):

    def __init__(self, rtp_timestamp_list, start_seq_number = 0, start_timestamp = 0, sourcesync = 2642723264):
        self.seq_number = start_seq_number
        self.timestamp = start_timestamp
        self.sourcesync = sourcesync
        self.rtp_timestamp_list = rtp_timestamp_list

    def encapsulate_nalu_in_rtp_packet(self, nalu):

        rtp = scap.RTP() / nalu
        rtp.version = 2
        rtp.padding = 0
        rtp.extension = 0
        rtp.numsync = 0
        rtp.payload_type = 96
        # TODO zufällig setzen
        rtp.sequence = self.seq_number
        # rtp.timestamp = self.timestamp
        rtp.timestamp = self.rtp_timestamp_list[0]
        rtp.sourcesync = self.sourcesync
        rtp.sync = []

        if nalu.nalu_type == 28 and nalu.FU_A_Header_E == 1 or (1 <= nalu.nalu_type <= 23):
            rtp.marker = 1
        else:
            rtp.marker = 0

        return rtp

    def parse_acces_unit_to_payload(self, access_unit, default_payload_size, size_list):
        rtp_payload_data = []
        payload_size = default_payload_size
        # just check if the list is empty one time because it nerver gets filled up
        list_not_empty_flag = True
        i = 0
        while (i<len(access_unit)):
            current_nalu = access_unit[i]
            # getting the max size of packet
            if list_not_empty_flag and size_list:
                payload_size = size_list[0]
            else:
                list_not_empty_flag = False
                payload_size = default_payload_size


            # if the nalus must be fragmented
            if not self.nalu_fits_in_one_packet(current_nalu, payload_size):
                nalu_to_append = fragment_nalu_into_FUAs_with_specific_size(current_nalu, default_payload_size, size_list)
                i  += 1
            elif (get_number_of_nalus_to_fit_in_stap_a(i,access_unit,payload_size) > 1):
                nalu_to_append = put_multiple_nalus_in_stap_a(i,access_unit,default_payload_size,size_list)
                i += get_number_of_nalus_to_fit_in_stap_a(i, access_unit, payload_size)
            else:
                if list_not_empty_flag:
                    size_list.pop(0)
                nalu_to_append = [current_nalu]
                i  += 1
            rtp_payload_data = rtp_payload_data + nalu_to_append
        return rtp_payload_data


    def nalu_fits_in_one_packet(self, nalu, max_payload_size):
        raw_data = self.scapy_packet_to_raw_bytes(nalu)
        # the -1 is because when we do not fragment we save the bytes for the additional FU-A Header
        return len(raw_data) - 1<= max_payload_size

    def set_information_for_new_access_unit(self):
        # self.timestamp += self.timestamp_offset
        self.seq_number += 1
        self.rtp_timestamp_list.pop(0)

    def scapy_packet_to_raw_bytes(self, packet):
        return bytes(packet)
