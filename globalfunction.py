
def sorted_intersect(list1, list2):
    """
    statement in document.
    """
    index_1 = 0
    index_2 = 0
    result = []
    while index_1 < len(list1) and index_2 < len(list2):
        if list1[index_1] == list2[index_2]:
            result.append(list1[index_1])
            index_1 += 1
            index_2 += 1
        elif list1[index_1] < list2[index_2]:
            index_1 += 1
        elif list1[index_1] > list2[index_2]:
            index_2 += 1
    return result

# test

# l1 = [1, 2, 3, 4, 5, 6, 7, 8]
# l2 = [3, 5, 6, 10, 22]
# print(sorted_intersect(l1, l2))
