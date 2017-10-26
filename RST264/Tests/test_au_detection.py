from hauptkomponenten.einlesen.pcap_nalu_parser import *
from hauptkomponenten.frame_grenzen.access_unit_detector import *
from global_variables import *

import unittest

class access_unit_helper_test(unittest.TestCase):

    def test_nalu_boundaries(self):

        parser = Pcap_nalu_parser(default_pcap_filepath,output_mode=False)
        nalu_list = parser.parse_nalus()

        sps = nalu_list[0]
        pps = nalu_list[1]
        sei = nalu_list[2]
        idr = nalu_list[3]
        n_idr = nalu_list[4]

        test = [sps,pps,sei,idr,n_idr,pps,n_idr,sps,pps] + nalu_list[12:15] + [sei,sei] + nalu_list[18:21]

        au_detector = Access_unit_detector(test)
        au_list = au_detector.get_access_units()

        au_types = list(map(lambda y: list(map(lambda x: x.nalu_type,y)), au_list))

        # ACHTUNG: Dies ist ein künstlich konstruierter Fall, er ist nur für die default pcap dati gültig
        self.assertEqual(au_types,[[7,8,6,5],[1,8,1],[7,8,1],[1],[1],[6,6,1],[1],[1]])


