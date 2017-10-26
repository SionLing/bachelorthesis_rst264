# Bis Zeile 6 entspricht der folgende Code dem aus der Datei einlesen_main.
# Demnach enthält die Variable nalu_list eine Liste aller NALUs. Zum Einteilen dieser in AUs wird ein Objekt der Klasse
# Access_unit_detector erzeugt, wobei als Parameter die Liste der NALUs angegeben wird.
# weiterhin wird dann an dem Objekt die Methode get_access_units() aufgerufen, welche ein zweidimensionales Array zurückgibt,
# in dem die AUs jeweils als Listen von NALUs enthalten sind.

from hauptkomponenten.einlesen.pcap_nalu_parser import *
from hauptkomponenten.frame_grenzen.access_unit_detector import *
from global_variables import *

parser = Pcap_nalu_parser(default_pcap_filepath,True)
nalu_list = parser.parse_nalus()

au_detector = Access_unit_detector(nalu_list,True)
au_list = au_detector.get_access_units()

# Das zweite Beispiel (hier auskommentiert) zeigt hier noch mal die volle Schnittstelle des Konstruktors der Klasse
# Access_unit_detector. Neben dem Pflichtparameter nalu_list kann auch hier der outoutput_mode, welcher standardmäßig auf False gesetzt ist,
# auf True gesetzt werden. In Folge dessen werden die Typinformationen der NALUs nach AUs unterteilt in eine .txt-Datei geschrieben.

# au_detector = Access_unit_detector(nalu_list, output_mode=True)
# au_list = au_detector.get_access_units()
