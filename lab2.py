def join_lists(a, b):
    if isinstance(b[0], int):
        res = [a] + b
        return res
    res = []
    for i in b:
        part_of_result = join_lists(a, i)
        if isinstance(part_of_result[0], list):
            res += part_of_result
        else:
            res.append(join_lists(a, i))
    return res


def get_correct_ways(matrix, start=0):
    res = []
    for i in matrix[start]:
        if not matrix[i]:
            res.append(i)
        else:
            part_of_result = join_lists(i, get_correct_ways(matrix, i))
            if isinstance(part_of_result[0], list):
                res += part_of_result
            else:
                res.append(part_of_result)
    return res


def get_mask(way):
    result = ['1'] * 8
    for i in way[:-1]:
        result[i - 1] = '0'
    return int('0b' + ''.join(result), 2)


def is_correct_way(way, masks):
    for mask in masks:
        if mask | way == 255:
            return True
    return False


def get_probability(way, ps):
    res = 1
    for elem_is_working, p in zip(bin(way)[2:], ps):
        if elem_is_working == '1':
            res *= p
        else:
            res *= 1 - p
    return res


E = [[1, 2],
     [3, 4],
     [3, 5],
     [4, 5],
     [6, 7],
     [6, 8],
     [7, 8],
     [9],
     [9],
     []]

P = [0.75, 0.1, 0.87, 0.55, 0.6, 0.28, 0.36, 0.76]

ways = get_correct_ways(E)

masks = [get_mask(way) for way in ways]
p_result = 0
for i in range(256):
    if is_correct_way(i, masks):
        p_result += get_probability(i, P)

print(p_result)
