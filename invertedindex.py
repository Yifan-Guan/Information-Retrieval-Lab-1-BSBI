import os
import pickle as pkl
from operator import length_hint

from uncompressedpostings import UncompressedPostings


class InvertedIndex:
    """
    Statement in document. :)
    """

    def __init__(self, index_name, postings_encoding=None, directory=''):
        """
        Statement in document.
        """

        self.index_file_path = os.path.join(directory, index_name + '.index')
        self.metadata_file_path = os.path.join(directory, index_name + '.dict')

        if postings_encoding is None:
            self.postings_encoding = UncompressedPostings
        else:
            self.postings_encoding = postings_encoding

        self.directory = directory
        self.postings_dict = {}
        self.terms = []

    def __enter__(self):
        """Opens the index_file and loads metadata upon entering the context"""
        # open the index file
        self.index_file = open(self.index_file_path, 'rb+')

        # Load the postings dict and terms from the metadata file
        with open(self.metadata_file_path, 'rb') as f:
            self.postings_dict, self.terms = pkl.load(f)
            self.term_iter = self.terms.__iter__()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Closes the index_file and saves metadata upon exiting the context"""
        # Close the index file
        self.index_file.close()

        # Write the postings dict and terms to the metadata file
        with open(self.metadata_file_path, 'wb') as f:
            pkl.dump([self.postings_dict, self.terms], f)

class InvertedIndexWriter(InvertedIndex):
    def __enter__(self):
        self.index_file = open(self.index_file_path, "wb+")
        return self

    def append(self, term, postings_list):
        """
        See the statement in the document.
        """
        encoded_postings_list = self.postings_encoding.encode(postings_list)
        with open(self.index_file_path, 'r+b') as f:
            f.seek(0, 2)
            start_position_in_index_file = f.tell()
            number_of_postings_in_list = len(postings_list)
            length_in_bytes_of_postings_list = len(encoded_postings_list)
            self.terms.append(term)
            self.postings_dict[term] = (start_position_in_index_file,
                                        number_of_postings_in_list,
                                        length_in_bytes_of_postings_list)
            f.write(encoded_postings_list)


class InvertedIndexIterator(InvertedIndex):
    def __enter__(self):
        super().__enter__()
        self._initialization_hook()
        return self

    def _initialization_hook(self):
        self.current_term_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_term_index < len(self.terms):
            term = self.terms[self.current_term_index]
            (start_position_in_index_file, number_of_postings_in_list,
             length_in_bytes_of_postings_list) = self.postings_dict[term]
            self.index_file.seek(start_position_in_index_file)
            encoded_postings_list = self.index_file.read(length_in_bytes_of_postings_list)
            postings_list = self.postings_encoding.decode(encoded_postings_list)
            self.current_term_index += 1
            return term, postings_list
        else:
            raise StopIteration

    def delete_from_disk(self):
        self.delete_upon_exit = True

    def __exit__(self, exception_type, exception_value, traceback):
        self.index_file.close()
        if hasattr(self, 'delete_upon_exit') and self.delete_upon_exit:
            os.remove(self.index_file_path)
            os.remove(self.metadata_file_path)
        else:
            with open(self.metadata_file_path, 'wb') as f:
                # noinspection PyTypeChecker
                pkl.dump([self.postings_dict, self.terms], f)

class InvertedIndexMapper(InvertedIndex):
    def __getitem__(self, term):
        """
        Statement in document.
        """
        (start_position_in_index_file, number_of_postings_in_list,
         length_in_bytes_of_postings_list) = self.postings_dict[term]
        self.index_file.seek(start_position_in_index_file)
        encoded_postings_list = self.index_file.read(length_in_bytes_of_postings_list)
        postings_list = self.postings_encoding.decode(encoded_postings_list)
        return postings_list

# test

# with InvertedIndexWriter('test', directory='temp') as index:
#     index.append(1, [2, 3, 4])
#     index.append(2, [3, 4, 5])
#     index.index_file.seek(0)
#     assert index.terms == [1,2], "terms sequence incorrect"
#     assert index.postings_dict == {1: (0, 3, len(UncompressedPostings.encode([2,3,4]))),
#                                    2: (len(UncompressedPostings.encode([2,3,4])), 3,
#                                        len(UncompressedPostings.encode([3,4,5])))}, "postings_dict incorrect"
#     assert UncompressedPostings.decode(index.index_file.read()) == [2, 3, 4, 3, 4, 5], "postings on disk incorrect"
#
# with InvertedIndexIterator('test', directory='temp') as iterator:
#     for term, postings_list in iterator:
#         print(term, end='')
#         print(postings_list)
#
# with InvertedIndexMapper('test', directory='temp') as mapper:
#     print(mapper[1])
#     print(mapper[2])