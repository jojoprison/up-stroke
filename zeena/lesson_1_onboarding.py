# int 4 bit, char - 8 bit. smallint, bigint
# float: для плавающией точки 1.25. 1 - 0.1 + 0.1 != 1 ~ 0.999999
# str
# bool: True / False
# None - тоже тип данных

# complex (e + mantiss)
# Decimal - объектный тип, нужно для денег валют

# КЛАССИЧЕСКИЕ структурные типы:
# tuple - кортеж. то же самое что list, но НЕИЗМЕНЯЕМ
# set - множество. содержит уникальные элементы
# list - [], array, массив ДИНАМИЧЕСКИЙ
# dict - словарь ключ - значение key - value - O(1)
# key всегда объект ХЕШИРУЕМЫЙ то есть .hashable()

# frozenset, frozenlist, frozendict - НЕИЗМЕНЯЕМЫЕ

# 1
# надо сделать так, чтоб на выходе был массив, где
# каждый элемент - 2 символа имени.
# исключить пробелы
# name = 'adasdasdasd'
name = 'egor    zubach    enko   '
lst = []

if ' ' in name:
    name = name.replace(' ', '')
# print(name)

for i in range(0, len(name), 2):

    lst.append(name[i:i + 2])

# print(lst)

# 2
# посчитать является ли число 1 кратным переданному числу в параметре 2
# надо делить до талого number на delimiter и проверять, кратно ли number или нет

# TYPING появился с python3.8
number: int = 100
delimiter: int = 5

while number % delimiter == 0:
    number = number / delimiter

if number == 1:
    print('ok')
else:
    print('not ok')


#
# if number % delimiter == 0:
#     print('ok')
# else:
#     print('not ok')
