from Helper.NALU_Parsing.parameter_set_manager import *
from Helper.access_unit_detection.access_unit_helper import *
from global_variables import *

class Access_unit_detector(object):

    def __init__(self, nalus, output_mode =False):
        self.nalus = nalus
        self.access_units = []
        # Manager for seq_parameter_set
        self.seq_param_manager = Parameter_set_manager()
        # Manager for pic_parameter_set
        self.pic_param_manager = Parameter_set_manager()
        self.output_mode = output_mode
        # Flags in erster liste:    bpcp -> start eines PCP
        #                           epcp -> ende PCP
        # zweites array für au_id
        self.nalus_with_flags = list(map(lambda x: ([],x,[]),self.nalus))


    def mark_beginnings_of_pcp(self):
        print("beginnings")
        i = self.index_of_first_vcl_nalu_type_125()

        # Überprüfe ob vorher noch PPS oder SPS auftauchen und aktiviere sie, wenn ja
        self.check_for_parameter_sets(i)
        self.set_beg_of_pcp_flag(i)

        pre_vcl_nalu = self.nalus[i]
        i += 1
        while(i < len(self.nalus)):
            current_nalu = self.nalus[i]

            # Wenn PPS oder SPS vorhanden müssen die für das korrekte Parsen der Syntaxelemente aktiviert werden
            # "Sequence parameter set(7)"
            if (current_nalu.nalu_type == 7):
                self.seq_param_manager.add_new_parameter_set(current_nalu)
            # "Picture parameter set(8)"
            elif current_nalu.nalu_type == 8:
                self.pic_param_manager.add_new_parameter_set(current_nalu)
            # Wenn NALU type 1, 2 oder 5 vorliegt, dann überprüfe, ob es sich den Anfang eines neuen PCP handelt
            elif (self.nalu_type_125(current_nalu)):
                beg_of_pcp = beginning_of_pcp(pre_vcl_nalu,current_nalu,self.seq_param_manager,self.pic_param_manager)
                if beg_of_pcp:
                    self.set_beg_of_pcp_flag(i)
                pre_vcl_nalu = current_nalu
            # ist der NALU Typ nicht 7, 8 oder 1, 2, 5 dann erhöhe den index trotzdem und gehe zu nächsten NALU,
            # da über die aktuell betrachtete bisher keine Aussage getroffen werden kann
            i += 1

    # ACHTUNG: diese Funktion arbeitet nur korrekt wenn zuvor mark_beginnings_of_pcp ausgeführt wurde
    def mark_endings_of_pcp(self):
        print("ending")
        i = self.index_of_first_vcl_nalu_type_125()
        # Überprüfe ob vorher noch PPS oder SPS auftauchen und aktiviere sie, wenn ja
        self.check_for_parameter_sets(i)

        current_start_of_pcp = i
        temp_end_of_pcp = i

        i += 1

        while(i < len(self.nalus)):
            current_nalu = self.nalus[i]
            current_nalu_type = current_nalu.nalu_type
            if(self.is_beg_of_pcp(i)):
                self.set_end_of_pcp_flag(temp_end_of_pcp)
                current_start_of_pcp = i
                temp_end_of_pcp = i
            elif current_nalu.nalu_type == 7:
                self.seq_param_manager.add_new_parameter_set(current_nalu)
                # "Picture parameter set(8)"
            elif current_nalu.nalu_type == 8:
                self.pic_param_manager.add_new_parameter_set(current_nalu)
            elif(1 <= current_nalu.nalu_type <= 5 and self.redundant_pic_cnt(current_nalu) == 0):
                temp_end_of_pcp = i
            i += 1
        self.set_end_of_pcp_flag(temp_end_of_pcp)

    def check_for_parameter_sets(self, end_index):
        for i in range(end_index):
            current_nalu = self.nalus[i]
            if (current_nalu.nalu_type == 7):
                self.seq_param_manager.add_new_parameter_set(current_nalu)
                # "Picture parameter set(8)"
            elif current_nalu.nalu_type == 8:
                self.pic_param_manager.add_new_parameter_set(current_nalu)

    def set_beg_of_pcp_flag(self, i):
        self.nalus_with_flags[i][0].append('bpcp')

    def set_end_of_pcp_flag(self, i):
        self.nalus_with_flags[i][0].append('epcp')

    def is_beg_of_pcp(self, current_end_of_pcp_index):
        return 'bpcp' in self.nalus_with_flags[current_end_of_pcp_index][0]

    def is_end_of_pcp(self, current_end_of_pcp_index):
        return 'epcp' in self.nalus_with_flags[current_end_of_pcp_index][0]

    def redundant_pic_cnt(self, current_nalu):
        return get_redundant_pic_cnt(current_nalu, self.pic_param_manager, self.seq_param_manager)

    def index_of_first_vcl_nalu_type_125(self):
        i = -1
        current_nalu_is_vcl_125 = False
        while(not current_nalu_is_vcl_125 and i < len(self.nalus)):
            current_nalu = self.nalus[i+1]
            current_nalu_is_vcl_125 = self.nalu_type_125(current_nalu)
            i += 1
        return i

    def nalu_type_125(self,nalu):
        return nalu.nalu_type == 1 or nalu.nalu_type == 2 or nalu.nalu_type == 5

    def mark_access_unit_boundaries(self):
        self.mark_beginnings_of_pcp()
        self.mark_endings_of_pcp()

        # alle NALUs zwischen Anfang und Ende eines pcp gehören zur gelichen AU
        current_au_id = 0

        current_beg_pcp = -1
        current_end_pcp = -1

        current_beg_pcp = self.next_beg_pcp(current_beg_pcp)
        current_end_pcp = self.next_end_pcp(current_end_pcp)
        while(isinstance(current_beg_pcp,int) and isinstance(current_end_pcp,int)):

            assert current_beg_pcp <= current_end_pcp

            for i in range(current_beg_pcp,current_end_pcp+1):
                self.nalus_with_flags[i][2].append(current_au_id)
            current_au_id += 1

            current_beg_pcp = self.next_beg_pcp(current_beg_pcp)
            current_end_pcp = self.next_end_pcp(current_end_pcp)


        # restlichen NALUs zuordnen
        nalu_index_without_au_id = -1
        next_nalu_index_with_au_id = -1
        current_au_id = 0

        nalu_index_without_au_id = self.get_next_nalu_index_without_au_id(nalu_index_without_au_id)
        next_nalu_index_with_au_id = self.get_next_nalu_index_with_au_id(nalu_index_without_au_id)

        while isinstance(nalu_index_without_au_id,int):

            current_au_id = self.nalus_with_flags[next_nalu_index_with_au_id][2][0] - 1

            i = nalu_index_without_au_id
            boundarie_found_flag = False
            while (i < next_nalu_index_with_au_id):
                current_nalu = self.nalus[i]
                if (not boundarie_found_flag) and ((6<= current_nalu.nalu_type <=9) or (14<= current_nalu.nalu_type <=18)):
                    current_au_id += 1
                    boundarie_found_flag = True
                self.nalus_with_flags[i][2].append(current_au_id)
                i += 1

            nalu_index_without_au_id = self.get_next_nalu_index_without_au_id(nalu_index_without_au_id)
            next_nalu_index_with_au_id = self.get_next_nalu_index_with_au_id(nalu_index_without_au_id)

    def get_access_units(self):
        self.mark_access_unit_boundaries()
        prev_au_id = 0
        temp_au_buffer = []
        i = 0
        while (i < len(self.nalus)):
            current_nalu_with_flags = self.nalus_with_flags[i]
            current_au_id = current_nalu_with_flags[2][0]
            current_nalu = current_nalu_with_flags[1]
            if (current_au_id != prev_au_id):
                self.access_units.append(temp_au_buffer)
                prev_au_id = current_au_id
                temp_au_buffer = [current_nalu]
            else:
                temp_au_buffer.append(current_nalu)
            i += 1
        self.access_units.append(temp_au_buffer)

        if self.output_mode:
            filepath = project_path + "output/access_units_in_pcap_output.txt"
            self.print_access_units_to_textfile(filepath)

        return self.access_units

    def print_access_units_to_textfile(self, filename):
        text_file = open(filename, "w")
        for access_unit in self.access_units:
            text_file.write("\n#######################access_unit#######################\n")
            for nalu in access_unit:
                text_file.write(nalu.nalu_type_repr(nalu.nalu_type) + "\n")
            text_file.write("#########################################################\n")
        text_file.close()










# def get_access_units(self):
    #
    #     access_unit_buffer = []
    #     temp_nalu_buffer = []
    #     prev_nalu = None
    #
    #     i = 0
    #     # for current_nalu in self.parsed_nalus:
    #     while (i < len(self.nalus)):
    #         current_nalu = self.nalus[i]
    #         print(i)
    #         # "Sequence parameter set(7)"
    #         if (current_nalu.nalu_type == 7):
    #             self.seq_param_manager.add_new_parameter_set(current_nalu)
    #         # "Picture parameter set(8)"
    #         elif current_nalu.nalu_type == 8:
    #             self.pic_param_manager.add_new_parameter_set(current_nalu)
    #
    #         start_of_new_acces_unit = start_of_new_access_unit(prev_nalu, current_nalu, self.seq_param_manager,
    #                                                            self.pic_param_manager)
    #         if (start_of_new_acces_unit):
    #             access_unit_buffer.append(temp_nalu_buffer[:])
    #
    #             temp_nalu_buffer.clear()
    #
    #         temp_nalu_buffer.append(current_nalu)
    #         prev_nalu = current_nalu
    #
    #         i += 1
    #
    #     # appand also the last nalus
    #     access_unit_buffer.append(temp_nalu_buffer[:])
    #     self.access_units = access_unit_buffer
    #
    #     if self.output_mode:
    #         filepath = project_path + "output/access_units_in_pcap_output.txt"
    #         self.print_access_units_to_textfile(filepath)
    #
    #     return self.access_units

    def print_access_units_to_textfile(self, filename):
        text_file = open(filename, "w")
        for access_unit in self.access_units:
            text_file.write("\n#######################access_unit#######################\n")
            for nalu in access_unit:
                text_file.write(nalu.nalu_type_repr(nalu.nalu_type) + "\n")
            text_file.write("#########################################################\n")
        text_file.close()

    def next_beg_pcp(self, current_beg_pcp):
        i = current_beg_pcp + 1
        try:
            while not 'bpcp' in self.nalus_with_flags[i][0]:
                i += 1
            return i
        except:
            return None

    def next_end_pcp(self, current_end_pcp):
        try:
            i = current_end_pcp + 1
            while not 'epcp' in self.nalus_with_flags[i][0]:
                i += 1
            return i
        except:
            return None

    def get_next_nalu_index_without_au_id(self, index):
        try:
            index += 1
            while len(self.nalus_with_flags[index][2]) > 0:
                index += 1
            return index
        except:
            return None

    def get_next_nalu_index_with_au_id(self, index):
        try:
            index += 1
            while len(self.nalus_with_flags[index][2]) == 0:
                index += 1
            return index
        except:
            return None








