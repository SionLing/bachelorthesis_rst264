import scapy.all as scap

from Helper.NALU_Parsing.seq_parameter_set_helper import *


class Parameter_set_manager(object):

    def __init__(self):
        self.parameter_set_dict = {}

    def add_new_parameter_set(self,nalu):
        # print(repr(nalu))
        # Sequence parameter set(7)
        nalu_payload = nalu[scap.Raw].load
        temp = nalu_payload[0]
        # print(nalu_payload)
        if(nalu.nalu_type == 7):
            seq_parameter_set = parse_seq_parameter_set_data(nalu_payload)
            id = seq_parameter_set.seq_parameter_set_id
            assert(isinstance( id, int ))
            self.parameter_set_dict[id] = seq_parameter_set

        # Picture parameter set(8)
        elif(nalu.nalu_type == 8):
            pic_parameter_set = parse_pic_parameter_set_data(nalu_payload)
            id = pic_parameter_set.seq_parameter_set_id
            assert(isinstance( id, int ))
            self.parameter_set_dict[id] = pic_parameter_set

    def get_param_set_by_id(self, id):
        try:
            return self.parameter_set_dict[id]
        except:
            return 0

