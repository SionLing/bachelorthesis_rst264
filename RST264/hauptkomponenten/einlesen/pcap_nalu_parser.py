import scapy.all as scap

from Data.NALU import *
from Exceptions.NALU_type_Exception import *
from Helper.NALU_Parsing.parsing_helper import remove_duplicates
from Helper.rtp_payload.FU_A_helper import form_one_NALU
from Helper.rtp_payload.STAP_A_helper import extract_actual_nalus
from global_variables import *


class Pcap_nalu_parser(object):

    def __init__(self, pcap_filepath, output_mode=False, port = 554):
        self.output_mode = output_mode
        self.pcap_filepath = pcap_filepath
        self.parsed_nalus = []
        self.nalu_buffer = []
        self.rtp_timestamp_list = []
        self.port = port

    def get_number_of_relevant_rtp_packets_in_pcap(self):
        pcap_file = scap.rdpcap(self.pcap_filepath)

        rtp_packets_raw = self.filter_by_port(pcap_file)
        rtp_packets = self.sort_and_form_rtp(rtp_packets_raw)
        return len(rtp_packets)


    def parse_nalus(self):
        # pcap file: logged Network traffic with Wireshark while streaming
        pcap_file = scap.rdpcap(self.pcap_filepath)

        rtp_packets_raw = self.filter_by_port(pcap_file)
        rtp_packets = self.sort_and_form_rtp(rtp_packets_raw)

        i = 1
        for rtp_packet in rtp_packets:
            rtp_payload = rtp_packet[scap.Raw].load
            nalu = NAL_unit(rtp_packet[scap.Raw].load)
            self.handle_nalu(nalu)

            # save rtp timestamp for (re)streaming
            self.rtp_timestamp_list.append(rtp_packet.timestamp)

            print(i)
            i += 1

        # reduce the rtp timestamp list so that there is only  one rtp_timestamp per access_unit
        self.rtp_timestamp_list = remove_duplicates(self.rtp_timestamp_list)

        if self.output_mode:
            filepath = project_path + "output/nalu_types_in_pcap_output.txt"
            self.print_nalu_types_to_textfile(filepath)

        return self.parsed_nalus

    def handle_nalu(self, nalu):
        if (0 <= nalu.nalu_type <= 23):
            self.parsed_nalus.append(nalu)
        elif (nalu.nalu_type == 24):
            self.parse_stap_a(nalu)
        elif (nalu.nalu_type == 28):
            self.handle_fu_a(nalu)
        else:
            raise NALU_type_Exception("The type of the given NALU can't be parsed")

    def parse_stap_a(self, stap_a_nalu):
        # Metthod from STAP_A_helper
        self.parsed_nalus = self.parsed_nalus + extract_actual_nalus(stap_a_nalu)

    def handle_fu_a(self, nalu):
        if nalu.FU_A_Header_S == 1:
            # if the current nalu is a START FU_A NAlU then the buffer should be empty
            assert (not self.nalu_buffer)
            self.nalu_buffer.append(nalu)
        elif (nalu.FU_A_Header_S == 0 and nalu.FU_A_Header_E == 0):
            assert (self.nalu_buffer)
            self.nalu_buffer.append(nalu)
        else:
            assert (nalu.FU_A_Header_E == 1)
            assert (self.nalu_buffer)
            self.nalu_buffer.append(nalu)
            self.parsed_nalus = self.parsed_nalus + [form_one_NALU(self.nalu_buffer)]
            self.nalu_buffer.clear()

    def filter_by_port(self, pcap_file):
        result = []
        for packet in pcap_file:
            if scap.UDP in packet and packet[scap.UDP].dport == self.port:
                result.append(packet)
        return result

    def sort_and_form_rtp(self, rtp_packets_raw):
        result = []
        for packet in rtp_packets_raw:
            rtp_packet = scap.RTP(packet[scap.Raw].load)
            result.append(rtp_packet)
        result.sort(key=lambda x: x.sequence, reverse=False)
        return result

    def print_nalu_types_to_textfile(self, filename):
        text_file = open(filename, "w")
        for nalu in self.parsed_nalus:
            text_file.write(nalu.nalu_type_repr(nalu.nalu_type) + "\n")
        text_file.close()