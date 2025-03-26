class IdMap:
    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []

    def __len__(self):
        return len(self.id_to_str)

    def _get_str(self, i):
        if 0 <= i < len(self.id_to_str):
            return self.id_to_str[i]
        else:
            return ""

    def _get_id(self, s):
        if s not in self.str_to_id.keys():
            self.str_to_id[s] = len(self.id_to_str)
            self.id_to_str.append(s)
        return self.str_to_id[s]

    def __getitem__(self, key):
        if type(key) is int:
            return self._get_str(key)
        elif type(key) is str:
            return self._get_id(key)
        else:
            raise TypeError

# test

# testIdMap = IdMap()
# assert testIdMap['a'] == 0, "Unable to add a new string to the IdMap"
# assert testIdMap['bcd'] == 1, "Unable to add a new string to the IdMap"
# assert testIdMap['a'] == 0, "Unable to retrieve the id of an existing string"
# assert testIdMap[1] == 'bcd', "Unable to retrieve the string corresponding to a given id"
#
# try:
#     testIdMap[2]
# except IndexError as e:
#     assert True, "Doesn't throw an IndexError for out of range numeric ids"