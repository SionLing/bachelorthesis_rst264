from hauptkomponenten.einlesen.pcap_nalu_parser import *
from hauptkomponenten.frame_grenzen.access_unit_detector import *
from hauptkomponenten.streaming.socket_sender import *
from hauptkomponenten.streaming.rtp_helper import *
from global_variables import *

import threading

parser = Pcap_nalu_parser(default_pcap_filepath,True)
nalu_list = parser.parse_nalus()

au_detector = Access_unit_detector(nalu_list,True)
aus = au_detector.get_access_units()


rtp_timestamp_list = parser.rtp_timestamp_list
rtp_helper = RTP_helper(rtp_timestamp_list)
st_help = Socket_sender("127.0.0.1", 3010, "127.0.0.1", 4010, rtp_helper)
# alle AUs in den Buffer des senders
for au in aus:
    st_help.access_unit_to_buffer(au,1400,[500,600,700]) # die ersten Pakete der AU haben max 500, 600 oder 700 Byte payload (kann beliebeig angepasst werden)

# Das Streamen kalppt nur wenn auch empfangen wird, sonst ist der Port zum empfangen nicht offen
def stream():
    st_help.send_all_packets_without_loss()

def receive():
    dir_path_for_video_save = project_path_for_cmd + 'output'
    sdp_filepath = default_sdp_file_path
    filename = 'streaming_main'
    ffmpeg_cmd = ffmpeg_receive_cmd %(dir_path_for_video_save,sdp_filepath,filename)
    subprocess.call(ffmpeg_cmd, shell=True)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=stream)

t1.start()
t2.start()

print("DONE")