from hauptkomponenten.video_qualitaet.video_quality_analyser import *
from global_variables import *

# HINWEIS: Bevor dieses Script ausgeführt werden kann müssen zwei Videos erzuegt werden die verglichen werden sollen
# Ein Video ohne Paketverluste kann z.B. durch streaming_main.py erzeugt werden
# Ein Video mit Paketverluste kann z.B. durch packet_loss_main.py erzeugt werden

video2 = project_path + "output/streaming_main.mp4"
video1 = project_path + "output/packet_loss_main.mp4"

# video1 = "/Users/nils/Desktop/ba/case_1_ref_video.mp4 "
# video2 = "/Users/nils/Desktop/ba/packet_loss_simulation_128_0video.mp4 "
compare_video_to_ref(video1,video2,project_path + "output/")

print("DONE")