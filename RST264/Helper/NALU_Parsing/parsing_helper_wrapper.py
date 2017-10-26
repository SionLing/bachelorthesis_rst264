from Helper.NALU_Parsing.parsing_helper import *

class Parsing_helper_wrapper(object):

    def __init__(self, bytes, length = None):
            self.bits =  byte_array2bit_array(bytes, length)

    # reads number_of_bits bist out of the array and returns an interger
    # as specified in standard
    def u(self,number_of_bits):
        parsing_result = read_bits(number_of_bits,self.bits)
        return self.interpret_parsing_result(parsing_result)

    def ue(self):
        parsing_result = ue(self.bits)
        return self.interpret_parsing_result(parsing_result)

    def se(self):
        parsing_result = se(self.bits)
        return self.interpret_parsing_result(parsing_result)

    def interpret_parsing_result(self, parsing_result):
        return_value = parsing_result[0]
        self.bits = parsing_result[1]
        return return_value

    def get_bits_size(self):
        return len(self.bits)
