from hauptkomponenten.einlesen.pcap_nalu_parser import *
from hauptkomponenten.frame_grenzen.access_unit_detector import *
from hauptkomponenten.streaming.socket_sender import *
from hauptkomponenten.streaming.rtp_helper import *
from global_variables import *
from hauptkomponenten.paket_verluste.packet_loss_simulator import *

import threading

parser = Pcap_nalu_parser(default_pcap_filepath,True)
nalu_list = parser.parse_nalus()

au_detector = Access_unit_detector(nalu_list,True)
aus = au_detector.get_access_units()


rtp_timestamp_list = parser.rtp_timestamp_list
rtp_helper = RTP_helper(rtp_timestamp_list)
skt_sender = Socket_sender("127.0.0.1", 3010, "127.0.0.1", 4010, rtp_helper)
# alle AUs in den Buffer des senders
for au in aus:
    skt_sender.access_unit_to_buffer(au, 1400, [500, 600, 700]) # die ersten Pakete der AU haben max 500, 600 oder 700 Byte payload (kann beliebeig angepasst werden)

# simuliere Paketverluste und speichere sie
random_seed = 42
csv_filename = "packet_loss_main_simulation"
simulate_packet_loss_norm_dist(skt_sender.buffer,random_seed,csv_filename,fps=30,mean=0.125,std=0.025,max_delay=0.16)

loss_array = read_loss_array_from_csv(project_path + "output/" + csv_filename + ".csv")

# Das Streamen kalppt nur wenn auch empfangen wird, sonst ist der Port zum empfangen nicht offen
def stream():
    skt_sender.send_all_packets_and_simulate_loss(loss_array)

def receive():
    dir_path_for_video_save = project_path_for_cmd + 'output'
    sdp_filepath = default_sdp_file_path
    filename = 'packet_loss_main'
    ffmpeg_cmd = ffmpeg_receive_cmd %(dir_path_for_video_save,sdp_filepath,filename)
    subprocess.call(ffmpeg_cmd, shell=True)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=stream)

t1.start()
t2.start()

print("DONE")