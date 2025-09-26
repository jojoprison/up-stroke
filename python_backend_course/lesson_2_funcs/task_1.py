a = 1
b = 2

# print(a + b)

a = 2

# print(a + b)

# define function
def say_hello(name, surname='zubachenko', third_name='maximovich'):
    print('hello', name, surname, third_name)

# say_hello('egor', 'zubachenko')
say_hello('egor')

def say_by(name, surname):
    print('by', name, surname)

say_by(surname = 'polt' ,name = 'serge')


def summa(b, a = 0, c = 0):
    print(a + b + c)

summa(5)

lst = [2, 3, 5, 8, 99]
summa = 0
for i in lst:
    if i % 3 == 0:
        summa += i

print(summa)

def sum_numbers_1(l):
    summa_s = 0
    for h in l:
        if h % 3 == 0:
            summa_s += h

    print(summa_s)

sum_numbers_1(lst)
