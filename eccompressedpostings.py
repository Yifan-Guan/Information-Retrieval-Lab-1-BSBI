import array

class ECCompressedPostings:
    @staticmethod
    def vb_code(postings):
        bin_postings = bin(postings)[2: ]
        result = ''
        start_index = 0
        add_number = (7 - len(bin_postings) % 7) % 7
        bin_postings = add_number * '0' + bin_postings
        sign = '1'
        while start_index < len(bin_postings):
            end_index = start_index + 7
            temp_piece = bin_postings[start_index: end_index]
            result = result + sign + temp_piece
            sign = '0'
            start_index = end_index
        return result


    @staticmethod
    def encode(postings_list):
        gap_list = [ECCompressedPostings.vb_code(postings_list[0])]
        for i in range(1, len(postings_list)):
            gap_list.append(ECCompressedPostings.vb_code(postings_list[i] - postings_list[i - 1]))
        code_str = ''
        for g in gap_list:
            code_str += g
        code_str = ((8 - (len(code_str) % 8)) % 8) * '0' + code_str
        byte_stream = bytearray()
        for i in range(0, len(code_str), 8):
            byte_stream.append(int(code_str[i: i + 8], 2))
        return array.array('B', byte_stream).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        byte_stream = array.array('B')
        byte_stream.frombytes(encoded_postings_list)
        code_str = ''
        for byte in byte_stream:
            byte_str = bin(byte)[2:].zfill(8)
            code_str += byte_str
        start_index = 0
        gap_list = []
        for i in range(0, len(code_str)):
            if code_str[i] == '1':
                start_index = i
                break
        temp_piece = ''
        while start_index < len(code_str):
            end_index = start_index + 8
            temp_piece += code_str[start_index + 1: end_index]
            if end_index == len(code_str) or code_str[end_index] == '1':
                gap_list.append(int(temp_piece, 2))
                temp_piece = ''
            start_index = end_index

        decoded_postings_list = [gap_list[0]]
        for i in range(1, len(gap_list)):
            decoded_postings_list.append(gap_list[i] + decoded_postings_list[-1])
        return decoded_postings_list

# test

# def test_encode_decode(l):
#     print(l)
#     e = ECCompressedPostings.encode(l)
#     print(e)
#     d = ECCompressedPostings.decode(e)
#     print(d)
#     assert d == l
#     print(l, e)
#
# test_encode_decode([1, 2, 3, 4, 5, 6])
# print('-' * 30)
# test_encode_decode([33, 56, 535, 666])