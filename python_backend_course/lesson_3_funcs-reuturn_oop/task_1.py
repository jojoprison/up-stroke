
lst_1 = [1, 2, 3]

def append_list(lst):
    lst.append(4)
    return lst

# print(append_list(lst_1))
# print(append_list(lst_1))

list_2 = [1000, 100, 10]
print(list_2)

list_2[0] = 0
print(list_2)


# (RUB, USD, EUR)
tuple_1_money = (1000, 100, 10)



dict_1 = {
    'name': 'egor',
    'money': {
        'rub': 1000,
        'usd': 100,
        'eur': 10,
        'more': {
            'rubrub': 0
        }
    }
}

print(dict_1)
print(dict_1['name'])
print(dict_1['money']['usd'])
print(dict_1['money']['more']['rubrub'])

dict_1['money']['more'] = 0
print(dict_1)

dict_1 = {}
print(dict_1)




set_1 = {1, 2, 3}
print(set_1)
print(type(set_1))

set_1.add(4)
print(set_1)

set_1.add(1)
print(set_1)

set_1.remove(1)
print(set_1)

set_1.remove(1)
print(set_1)

# создать словарь где я буду хранить информацию о себе в виде:
# имя, адрес: улица, дом, # сегодняшняя дата

# написать функцию, которая будет принимать словарь user_data
# и обновлять в нем имя, переданное в качестве параметра
