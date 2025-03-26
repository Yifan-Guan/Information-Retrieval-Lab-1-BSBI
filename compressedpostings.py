import array

class CompressedPostings:
    @staticmethod
    def gama_encode(number):
        temp = bin(number)[2:]
        result = (len(temp) - 1) * '1' + '0' + temp[1:]
        return result

    @staticmethod
    def encode(postings_list):
        gap_list = [CompressedPostings.gama_encode(postings_list[0] + 1)]
        for i in range(1, len(postings_list)):
            gap_list.append(CompressedPostings.gama_encode(postings_list[i] - postings_list[i - 1] + 1))
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
        while start_index < len(code_str):
            separator_index = start_index
            while code_str[separator_index] != '0':
                separator_index += 1
            piece_len = separator_index - start_index
            end_index = separator_index + piece_len + 1
            gap_list.append(int(('1' + code_str[separator_index + 1: end_index]), 2) - 1)
            start_index = end_index
        decoded_postings_list = [gap_list[0]]
        for i in range(1, len(gap_list)):
            decoded_postings_list.append(gap_list[i] + decoded_postings_list[-1])
        return decoded_postings_list




# test
# def test_encode_decode(l):
#     print(l)
#     e = CompressedPostings.encode(l)
#     print(e)
#     d = CompressedPostings.decode(e)
#     print(d)
#     assert d == l
#     print(l, e)
#
# test_encode_decode([1, 2, 3, 4, 5, 6])
# print('-' * 30)
# test_encode_decode([33, 56, 535, 666])
