from math import ceil
# this helper conatins functions which are specified in Section 9 of the ITU standard for H264,
# also the names of the functions are the same as in the defenition

# named as specified in ITU document
def ue(v):
    return codeNum(v)

# named as specified in ITU document
def se(v):
    code_num = codeNum(v)
    k = code_num[0]
    return (pow(-1,(k+1)) * ceil(k/2.0), code_num[1])


# unsigned integer Exp-Golomb-coded syntax element with the left bit first.
# specification in clause 9.1
# we assume that the input v is given as an array of Bits
# returns the value of the function as defined in the stadard and the new bit_array
def codeNum(v):
    # convert the Byte array into an array of single bits so that single bits can be analysed
    # bit_array = byte_array2bit_array(v)
    bit_array = v
    leading_zero_bits = -1
    b = 0
    while(b == 0):
        read_bits_temp = read_bits(1, bit_array)
        b = read_bits_temp[0]
        bit_array = read_bits_temp[1]
        leading_zero_bits += 1

    # returning codeNum
    read_bits_tupel = read_bits(leading_zero_bits,bit_array)
    return (pow(2,leading_zero_bits)-1 + read_bits_tupel[0], read_bits_tupel[1])

# this function is also specified in the standard in
# in this implementation it reads n bist from the given bit_array and an interprets them as an unsigned interger
# returns the integer and the new (reduced) bit_array
def read_bits(n, bit_array):
    assert(n <= len(bit_array))
    if(n == 0):
        return (0,bit_array)
    else:
        bits = bit_array[:n]
        return (bit_array2int(bits),bit_array[n:])

# this function returns a new bit_array without the first n bits
def reduce_bit_array(n, bit_array):
    assert(n <= len(bit_array))
    return bit_array[n:len(bit_array)]

# with this function we can access an bit at pos in an array of bytes
def access_bit(byte_array, pos):
    base = int(pos/8)
    shift = pos % 8
    return (byte_array[base] & (1<<shift)) >> shift

def byte_array2bit_array(byte_array, size = None):
    bit_array = []
    if (size is None):
        for byte in byte_array:
            temp_bit_array = byte_to_bit_array(byte)
            bit_array = bit_array + temp_bit_array
    else:
        i = 0
        while (i < size and i < len(byte_array)):
            byte = byte_array[i]
            temp_bit_array = byte_to_bit_array(byte)
            bit_array = bit_array + temp_bit_array
            i += 1
    return bit_array


# NOTE: byte is an integer here
def byte_to_bit_array(byte):
    result = []
    bin_repr = bin(byte)
    assert(bin_repr[0] == "0" and bin_repr[1] == "b")
    i = 2
    while(i < len(bin_repr)):
        result.append(int(bin_repr[i]))
        i += 1
    # make the list a full byte representation
    result = fill_zero_bits(8,result)
    return result

def fill_zero_bits(requested_length, bit_array):
    to_fill = 8 - len(bit_array)
    bit_array[0:0] = [0] * to_fill
    return bit_array

def bit_array2int(bit_array):
    bit_array = [str(x) for x in bit_array]
    bit_string = ''.join(bit_array)
    return int(bit_string,2)

# https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-whilst-preserving-order
def remove_duplicates(list):
    seen = set()
    seen_add = seen.add
    return [x for x in list if not (x in seen or seen_add(x))]

