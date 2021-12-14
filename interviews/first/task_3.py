import random
import itertools


def variants_tree(input_list):

    variants_set = set()

    # if len(input_list) == 0:
    #     return 0
    #
    variant_count = 1

    for i in range(len(input_list) - 1):
        variant_count += variant_count * i

    count = 0

    # while count < variant_count:

    working_list = input_list.copy()
    res_list = []

    while len(working_list) > 3:
        elem = working_list.pop(0)
        res_list.append(elem)


    print(working_list)
    print(input_list)


    # variants_set.add()

    return variant_count


def recursive(prefix, values):

    if len(values) == 0:
        print(prefix)
    else:
        for i in range(len(values)):
            recursive(prefix + [values[i]], values[:i] + values[i + 1:])


# TODO backtracking
def permute(data, i, length):
  if i == length:
    print(data)
  else:
    for j in range(i, length):
      data[i], data[j] = data[j], data[i]
      permute(data, i + 1, length)
      data[i], data[j] = data[j], data[i]


def new_var(input_list):

    if len(input_list) == 0:
        return 0

    variants_set = set()

    variant_count = 1

    for i in range(len(input_list)):
        variant_count += variant_count * i

    while len(variants_set) < variant_count:

        input_list_copy = input_list.copy()
        new_list = []

        while input_list_copy:
            rand_value = random.choice(input_list_copy)
            input_list_copy.remove(rand_value)

            new_list.append(rand_value)

        variants_set.add(tuple(new_list))

    # TODO itertools.
    # itertools.permutations(list)

    return variants_set


if __name__ == '__main__':
    # 1234 1243 1324 1343 1432 1423
    # 2134 2143 2341 2314 2413 2431
    # 1, 2, 6, 24
    listt = [1, 2, 3, 4, 5]

    recursive([], listt)

    permute(a, 0, len(a))

    # res = new_var(listt)
    # print(len(res))
    # print(res)