def change_seq_1(my_list):
    new_list = []

    # TODO REVERSED
    for i in reversed(my_list):
        print(i)

    for i in range(1, len(my_list)):
        new_list.append(my_list[-i])

    new_list.append(my_list[0])

    return new_list


def change_seq_2(my_list):
    for i in range(len(my_list) // 2):
        h = my_list[i]
        my_list[i] = my_list[-i]
        my_list[-i] = h

    first_elem = my_list[0]
    del my_list[0]

    my_list.append(first_elem)

    return my_list


if __name__ == '__main__':
    listt = [1, 2, 3, 4, 5, 6, 7]

    # new_l = change_seq_2(listt)
    #
    # change_seq_1(listt)
    # print(new_l)

    # todo get_item
    list_2 = listt[::-1]
    print(list_2)