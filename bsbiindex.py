import os
import heapq
import contextlib
import pickle as pkl
from idmap import IdMap
from invertedindex import InvertedIndexWriter, InvertedIndexMapper, InvertedIndexIterator
from compressedpostings import CompressedPostings
from eccompressedpostings import ECCompressedPostings
import globalfunction

class BSBIIndex:
    """
    See the statement in the document.
    """

    def __init__(self, data_dir, output_dir, index_name = "BSBI", postings_encoding = None):
        self.term_id_map = IdMap()
        self.doc_id_map = IdMap()
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.index_name = index_name
        self.postings_encoding = postings_encoding
        self.intermediate_indices = []

    def save(self):
        """Dumps doc_id_map and term_id_map into output directory"""

        with open(os.path.join(self.output_dir, 'terms.dict'), 'wb') as f:
            # noinspection PyTypeChecker
            pkl.dump(self.term_id_map, f)
        with open(os.path.join(self.output_dir, 'doc.dict'), 'wb') as f:
            # noinspection PyTypeChecker
            pkl.dump(self.doc_id_map, f)

    def load(self):
        """Loads doc_id_map and term_id_map from output directory"""

        with open(os.path.join(self.output_dir, 'terms.dict'), 'rb') as f:
            self.term_id_map = pkl.load(f)
        with open(os.path.join(self.output_dir, 'doc.dict'), 'rb') as f:
            self.doc_id_map = pkl.load(f)

    def index(self):
        """
        See the statement from the document.
        """

        for block_dir_relative in sorted(next(os.walk(self.data_dir))[1]):
            td_pairs = self.parse_block(block_dir_relative)
            index_id = 'index_' + block_dir_relative
            self.intermediate_indices.append(index_id)
            with InvertedIndexWriter(index_id, directory=self.output_dir,
                                     postings_encoding=self.postings_encoding) as index:
                self.invert_write(td_pairs, index)
                td_pairs = None
        self.save()
        with InvertedIndexWriter(self.index_name, directory=self.output_dir,
                                 postings_encoding=self.postings_encoding) as merged_index:
            with contextlib.ExitStack() as stack:
                indices = [stack.enter_context(
                    InvertedIndexIterator(index_id, directory=self.output_dir,
                                          postings_encoding=self.postings_encoding))
                for index_id in self.intermediate_indices]
                self.merge(indices, merged_index)


    def parse_block(self, block_dir_relative):
        """
        See the statement in the document.
        :param block_dir_relative:
        """
        result = []
        block_dir_path = os.path.join(self.data_dir, block_dir_relative)
        file_list = os.listdir(str(block_dir_path))
        for file_name in file_list:
            with open(os.path.join(str(block_dir_path), file_name)) as f:
                doc_id = self.doc_id_map[os.path.join(str(block_dir_path), file_name)]
                file_word_list = f.read().split()
                for word in file_word_list:
                    term_id = self.term_id_map[word]
                    term_doc_pair = [term_id, doc_id]
                    result.append(term_doc_pair)
        return result



    def invert_write(self, td_pairs, index):
        """
        See the statement in the document.
        """
        result = {}
        for [term_id, doc_id] in td_pairs:
            if term_id not in result.keys():
                result[term_id] = []
            result[term_id].append(doc_id)
        term_id_list = sorted(result.keys())
        for term_id in term_id_list:
            doc_id_list = sorted((result[term_id]))
            index.append(term_id, doc_id_list)

    def merge(self, indices, merge_index):
        """
        See the statement in the document.
        """
        current_term = None
        current_postings_list = None
        for term, postings_list in heapq.merge(*indices):
            if term != current_term:
                if current_term is not None:
                    merge_index.append(current_term, list(sorted(set(current_postings_list))))
                current_term = term
                current_postings_list = postings_list
            else:
                current_postings_list += postings_list
        if current_term is not None:
            merge_index.append(current_term, list(sorted((set(current_postings_list)))))

    def retrieve(self, query):
        """
        statement in document.
        """

        if len(self.term_id_map) == 0 or len(self.doc_id_map) == 0:
            self.load()

        with InvertedIndexMapper(self.index_name, directory=self.output_dir,
                                 postings_encoding=self.postings_encoding) as mapper:
            result_postings_list = None
            query_term_list = query.split()
            for query_term in query_term_list:
                query_term_id = self.term_id_map.str_to_id.get(query_term)
                if query_term_id is None:
                    return []
                else:
                    postings_list = mapper[query_term_id]
                    if result_postings_list is None:
                        result_postings_list = postings_list
                    else:
                        result_postings_list = globalfunction.sorted_intersect(postings_list,
                                                                               result_postings_list)

            doc_list = []
            for doc_id in result_postings_list:
                doc = self.doc_id_map[doc_id]
                doc_list.append(doc)

            return doc_list

# test

# with open('toy-data/0/fine.txt', 'r') as f:
#     print(f.read())
# with open('toy-data/0/hello.txt', 'r') as f:
#     print(f.read())
#
# BSBI_instance = BSBIIndex(data_dir="toy-data", output_dir = 'tmp/', index_name = 'toy')
# pair_list = BSBI_instance.parse_block('0')
# print(pair_list)
#
# with InvertedIndexWriter('test', directory='temp') as index:
#     BSBI_instance.invert_write(pair_list, index)
#     print(index.postings_dict)

# BSBI_instance = BSBIIndex(data_dir='toy-data', output_dir = 'toy_output_dir', )
# BSBI_instance.index()
#
# BSBI_instance = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir', )
# BSBI_instance.index()

# BSBI_instance = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir', )
# result = BSBI_instance.retrieve('boolean retrieval')
# for i in result:
#     print(i)

# BSBI_instance = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir', )
# for i in range(1, 9):
#     with open('dev_queries/query.' + str(i)) as q:
#         query = q.read()
#         my_results = [os.path.normpath(path) for path in BSBI_instance.retrieve(query)]
#         with open('dev_output/' + str(i) + '.out') as o:
#             reference_results = [os.path.normpath(x.strip()) for x in o.readlines()]
#             assert my_results == reference_results, "Results DO NOT match for query: "+query.strip()
#         print("Results match for query:", query.strip())

# try:
#     os.mkdir('output_dir_compressed')
# except FileExistsError:
#     pass
#
# BSBI_instance_compressed = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir_compressed', postings_encoding=CompressedPostings)
# BSBI_instance_compressed.index()

# BSBI_instance_compressed = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir_compressed', postings_encoding=CompressedPostings)
# postings_list = BSBI_instance_compressed.retrieve('boolean retrieval')
# for postings in postings_list:
#     print(postings)

# try:
#     os.mkdir('output_dir_ec_compressed')
# except FileExistsError:
#     pass
#
# BSBI_instance_compressed = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir_ec_compressed', postings_encoding=ECCompressedPostings)
# BSBI_instance_compressed.index()