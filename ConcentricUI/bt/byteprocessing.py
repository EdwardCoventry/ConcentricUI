def round_down(num, divisor):
    return num - (num % divisor)

def round_up(num, divisor=1):
    if num % divisor:
        return num - (num % divisor) + divisor
    else:
        return num

def get_byte(n, padding=True):
    array = [int(x) for x in bin(n)[2:]]
    if padding:
        array = pad(array, 8, next_multiple=True)
    return array

def pad(l, width, content=0, next_multiple=True):
    #  fixme it would be cool to do automatic types

    if next_multiple and len(l) > next_multiple:
        width = round_up(len(l), divisor=width)

    padding = [content] * width
    l = padding[len(l):] + list(l)
    return l


def get_byte_count(integer):
    bit_count = integer.bit_length()
    byte_count = round_up(bit_count, 8) // 8
    return byte_count


def split_array(mylist, chunk_size):
    return [mylist[offs:offs + chunk_size] for offs in range(0, len(mylist), chunk_size)]


def get_int_from_array(array):
    #  this turns an array into a byte ... ?

    array_as_a_string = ''.join((str(x) for x in array))

    array_as_a_byte = int(array_as_a_string, 2)

    return array_as_a_byte


def split_int_into_byte_list(integer):
    if integer < 256:
        #  just a little shortcut
        return [integer]

    byte_list = get_byte(integer, padding=True)

    chunks = split_array(byte_list, 8)
    # chunks.reverse()
    #  shouldnt just sending the integer work? ill leave it for now as it works
    #  but i think just self.send_integer(prepend_byte_count=True) should do it
    braille_ints = []
    for chunk in chunks:
        braille_int = get_int_from_array(chunk)
        braille_ints.append(braille_int)
    return braille_ints

def concatenate_byte_list_into_int(byte_list):
    if any([True for x in byte_list if x > 255]):
        raise Exception("At least one of the ints"
                        "(specifically {})"
                        "was just too big!".format([x for x in byte_list if x > 255]))
    binary_bytes = [format(x, "b") for x in byte_list]
    padded_binary_bytes = reversed([''.join(pad(x, 8, '0')) for x in binary_bytes])
    binary = "".join(padded_binary_bytes)

    print('!!!!! BIN', binary)

    concatenated_int = int(binary, 2)
    return concatenated_int


# 100101100
#['00101100', '000000001', '0', '0']


class ByteProcessing(object):

    @staticmethod
    def process_integers(integers):
        return_bytes = []
        for integer in integers:
            return_bytes.extend(ByteProcessing.process_integer(integer, prepend_byte_count=True))
        return return_bytes

    @staticmethod
    def process_integer(integer=0, prepend_byte_count=True):

        """

        This function is for sending/queuing integers to an Arduino-esque chip through a bt receiver.
        To send an integer that's over 1 byte long ( > 255) it must be split into individual bytes
        This function can send an integer as a single byte,
        or if the integer takes more than 1 byte use prepend_byte_count and the integer will be split into bytes,
        and the total number of bytes will be prepended to the bytes that are sent.

        eg. to send the number 290 = 100100010 the following bytes will be sent:
        00000010 = 2   #  byte count
        00000001 = 1   # higher order byte
        00100010 = 34  # lower order byte


        :param integer:
        :param prepend_byte_count:
        :return:
        """


        if prepend_byte_count is True:
            byte_count = get_byte_count(integer)
            if not byte_count:
                #  this bug was tricky to find... basically i want 00000000 to be assigned a byte count of 1
                byte_count = 1
        else:
            if integer > 255:
                Warning("Integer {} is too large to be sent to the chip in a single byte! "
                        "Consider setting prepend_byte_count = True".format(integer))
                print("Integer {} is too large to be sent to the chip in a single byte! "
                      "Consider setting prepend_byte_count = True".format(integer))
            return [integer]

        split_integer = split_int_into_byte_list(integer)

        return [byte_count] + split_integer