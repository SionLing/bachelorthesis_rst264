# Das Folgenden Codebeispiel zeigt, wie eine .pcap-Datei durch das Werkzug eingelesen werden kann.
# Weiterhin zeigt es wie das Werkzeug genutzt wird um die eingelesenen Daten als NALUs zu erhalten.
#
# Hierzu wird in eine Instanz der Klasse Pcap_nalu_parser erstellt und als Parameter die gewünschte .pcap-Datei angegeben.
# Weiterhin wird an dem Objekt die Methode parse_nalus() aufgerufen, welche eine Liste der in dem aufgezeichneten Videostream
# enthaltenen NALUs zurückliefert.

from hauptkomponenten.einlesen.pcap_nalu_parser import *
from global_variables import *

parser = Pcap_nalu_parser(default_pcap_filepath,True)
nalu_list = parser.parse_nalus()

# Das zweite Beispiel (hier auskommentiert) zeigt die volle Schnittstelle des Konstruktors von Pcap_nalu_parser.
#  Neben dem Pflichtaparemter, welcher den Dateipfad zur .pcap-Datei darstellt, können zusätzlich folgende Angaben gemacht werden:
#   -> outoutput_mode (standardmäßig False):
#        	Wird dieser auf True gesetzt, so werden die aus der .pacap-Datei geparsten Typangaben der NALUs in eine .txt-Datei geschrieben und können so nachvollzogen werden.
# 	-> port (standardmäßig 554):
#           Über diese Parameter kann angegeben werden, welcher Port beim Streamen des Videos gewählt wurde. Nur Pakete mit diesem Port werden von dem Werkzeug beim Parsingporzess berücksichtigt.

# parser = Pcap_nalu_parser(default_pcap_filepath,output_mode=True, port=1234)
# nalu_list = parser.parse_nalus()

