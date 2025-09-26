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


def user_info(name, age, hobby=""):
    print(f"Имя: {name}, возраст: {age}, хобби: {hobby}")

user_info('serg',18)


def repeat_word(word, times = 3):
    print(word * times)

repeat_word('volt')


def shopping_list(item1, item2, item3 = None):
    print(item1, item2, item3)

shopping_list('apple', 'banane', 'lime')

def say_hello_to_all(*name):
    print('hello', *name)

say_hello_to_all("Egor", "Max", "Ivan")

"""
def print_profile(**kwargs):
    print(**kwargs)

print_profile(name="Egor", age=14, city="Vladimir")
"""

def atm(balance, withdraw):
    if withdraw <= balance:
        return balance - withdraw
    else:
        return "Недостаточно средств"


withdraw_balance = atm(1000, 300)
print(withdraw_balance)
withdraw_balance1 = atm(1000, 1500)
print(withdraw_balance1)

