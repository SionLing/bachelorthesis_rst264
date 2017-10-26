from scapy.all import *

class NAL_unit(Packet):
    name = "H264"
    nalu_enum_number_to_type = {0: "reserved (0)",
                                1: "Coded slice of a non-IDR picture(1)",
                                2: "Coded slice data partition A(2)",
                                3: "Coded slice data partition B(3)",
                                4: "Coded slice data partition C(4)",
                                5: "Coded slice of an IDR picture(5)",
                                6: "Supplemental enhancement information(6)",
                                7: "Sequence parameter set(7)",
                                8: "Picture parameter set(8)",
                                9: "Access unit delimiter(9)",
                                10: "End of sequence(10)",
                                11: "End of stream(11)",
                                12: "Filler data(12)",
                                13: "Sequence parameter set extension(13)",
                                14: "Prefix NAL unit(14)",
                                15: "Subset sequence parameter set(15)",
                                16: "Depth parameter set(16)",
                                17: "Reserved(17)",
                                18: "Reserved(18)",
                                19: "Coded slice of an auxiliary coded picture without partitioning(19)",
                                20: "Coded slice extension(20)",
                                21: "Coded slice extension for a depth view component or a 3D-AVC texture view component(21)",
                                22: "Reserved(22)",
                                23: "Reserved(23)",
                                24: "Single-time aggregation packet-A(24)",
                                25: "Single-time aggregation packet-B(25)",
                                26: "Multi-time aggregation packet-16(26)",
                                27: "Multi-time aggregation packet-24(27)",
                                28: "Fragmentation unit-A(28)",
                                29: "Fragmentation unit-B(29)",
                                30: "Reserved(30)",
                                31: "Reserved(31)"
                                }

    nalu_enum_type_to_number = {v: k for k, v in nalu_enum_number_to_type.items()}


    fields_desc = [
        BitField("forbidden_zero",0, 1),
        BitField("nal_ref_idc",00, 2),
        BitEnumField("nalu_type", None, 5, nalu_enum_number_to_type),

        # In case of a Single-Time Aggregation Packet-A
        # it might be possible to parse a variable number of fields out of it,
        # this parsing procedure is handeled in a single helper class

        # In Case of Fragmentation unit-A (nalu_type: 28)
        ConditionalField(BitField("FU_A_Header_S", 0, 1), lambda pkt: pkt.nalu_type == 28),
        ConditionalField(BitField("FU_A_Header_E", 0, 1), lambda pkt: pkt.nalu_type == 28),
        ConditionalField(BitField("FU_A_Header_R", 0, 1), lambda pkt: pkt.nalu_type == 28),
        ConditionalField(BitEnumField("FU_A_Header_actual_nalu_type", None, 5, nalu_enum_number_to_type), lambda pkt: pkt.nalu_type == 28),

        # In Case of Fragmentation unit-B (nalu_type: 29)
        ConditionalField(BitField("FU_B_Header_S", 0, 1), lambda pkt: pkt.nalu_type == 29),
        ConditionalField(BitField("FU_B_Header_E", 0, 1), lambda pkt: pkt.nalu_type == 29),
        ConditionalField(BitField("FU_B_Header_R", 0, 1), lambda pkt: pkt.nalu_type == 29),
        ConditionalField(BitEnumField("FU_B_Header_actual_nalu_type", None, 5, nalu_enum_number_to_type), lambda pkt: pkt.nalu_type == 29),
        ConditionalField(ShortField("DON", None), lambda pkt: pkt.nalu_type == 29)
    ]

    def nalu_type_repr(self, nalu_type):
        return self.nalu_enum_number_to_type[nalu_type]
