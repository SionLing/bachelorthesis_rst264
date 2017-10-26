project_path_for_cmd = '/Users/nils/Studium/Materialien\ 6.Semester/BachelorArbeit/public_repository/RST264/'
project_path = '/Users/nils/Studium/Materialien 6.Semester/BachelorArbeit/public_repository/RST264/'

default_sdp_file_path = project_path_for_cmd + 'default_files/default_sdp.sdp'
default_pcap_filepath = project_path + 'default_files/default_pcap.pcap'

ffmpeg_receive_cmd = "cd %s && ffmpeg -protocol_whitelist file,crypto,rtp,udp -i %s -framerate 30 -vcodec libx264 -f mp4 -c copy -r 30 %s.mp4"