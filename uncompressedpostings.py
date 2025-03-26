import array

class UncompressedPostings:

    @staticmethod
    def encode(postings_list):
        """
        statement in document.
        :param postings_list:
        """
        return array.array('L', postings_list).tobytes()

    @staticmethod
    def decode(encode_postings_list):
        """
        statement in document.
        :param encode_postings_list:
        """
        decode_postings_list = array.array('L')
        decode_postings_list.frombytes(encode_postings_list)
        return decode_postings_list.tolist()

# test

# x = UncompressedPostings.encode([1, 2, 3])
# print(x)
# print(UncompressedPostings.decode(x))