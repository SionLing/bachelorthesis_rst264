import socket as net

from Data.NALU import *


class Socket_sender(object):

    def __init__(self, src_ip, src_port, dst_ip, dst_port, rtp_helper, calc_overhead = False):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.buffer = []
        self.socket_open = False
        self.rtp_helper = rtp_helper
        self.calc_overhead = calc_overhead
        self.overhead = 0
        self.num_packets = 0
        self.udp_data = 0

    def open_socket(self):
        self.sock = net.socket(net.AF_INET, net.SOCK_DGRAM)
        self.sock.bind((self.src_ip, self.src_port))
        self.sock.connect((self.dst_ip, self.dst_port))
        self.socket_open = True

    def close_socket(self):
        self.sock.close()
        self.socket_open = False

    def access_unit_to_buffer(self, access_unit, max_payload_size, size_array=[]):
        rtp_payload_list = self.rtp_helper.parse_acces_unit_to_payload(access_unit, max_payload_size, size_array)

        # calc overhead
        if(self.calc_overhead):
            self.num_packets += len(rtp_payload_list)

        temp = []
        for rtp_payload in rtp_payload_list:
            rtp_packet = self.rtp_helper.encapsulate_nalu_in_rtp_packet(rtp_payload)

            # calc overhead
            if (self.calc_overhead):
                data_to_send = len(bytes(rtp_packet)) + 8 # 8 because of UDP-Header
                self.udp_data += data_to_send
                overhead = data_to_send - len(bytes(rtp_payload))
                self.overhead += overhead

            temp.append(self.rtp_helper.scapy_packet_to_raw_bytes(rtp_packet))
            # self.buffer.append(self.rtp_helper.scapy_packet_to_raw_bytes(rtp_packet))
        self.buffer.append(temp)
        self.rtp_helper.set_information_for_new_access_unit()

    def send_all_packets_without_loss(self):
        self.send_all_packets_and_simulate_loss([],no_loss=True)

    def send_all_packets_and_simulate_loss(self, loss_array, no_loss = False):
        pl_array = loss_array
        i = 0
        send_count = 0
        lost_count = 0

        self.open_socket()

        for access_unit_raw in self.buffer:
            time.sleep(0.03)
            num_packets_in_access_unit = len(access_unit_raw)
            packet_sleep_time = 0.003 / num_packets_in_access_unit
            if (packet_sleep_time < 0.0002):
                packet_sleep_time = 0.0002
            for raw_rtp_data in access_unit_raw:
                # if ((not pl_array[i] or True) and not(100 < i < 110)):
                # if not pl_array[i] or True:
                if no_loss or not pl_array[i] :
                    send_count += 1
                    self.sock.send(raw_rtp_data)
                    # wenn diese Zeile auskommentiert wird -> Video ist fehlerhaft
                    time.sleep(packet_sleep_time)
                    # self.send_access_unit(access_unit_raw)
                else:
                    lost_count += 1
                i += 1
        print("num_packets: " + str(i))
        print("num_send: " + str(send_count))
        print("num_lost: " + str(lost_count))
        # self.buffer.clear()
        self.close_socket()
