def user_info(name, age, hobby=""):
    print(f"Имя: {name}, возраст: {age}, хобби: {hobby}")

user_info('serg',18)



def repeat_word(word, times = 3):
    words = str(word * times)
    print(words)

repeat_word('volt')



def shopping_list(item1, item2, item3 = None):
    print(item1, item2, item3)

shopping_list(item3='apple', item2='banane', item1='lime')

def say_hello_to_all(*name):
    print(name)
    print('hello', name)

say_hello_to_all("Egor", "Max", "Ivan")
# from struct import unpack

def print_profile(*asdasdasdasd, **kwargs):
    print(asdasdasdasd)
    print(kwargs)

print_profile(1, 2, 3, 12, 12431223, 12313, name="Egor", age=14, city="Vladimir")


def atm(balance, withdraw):

    if balance < 0:
        return None

    if withdraw is None:
        return None

    if withdraw <= balance:
        print(balance - withdraw)
        # return - возврат
        return balance - withdraw
    else:
        return "Недостаточно средств"


withdraw_balance = atm(1000, 300)
print(withdraw_balance)
withdraw_balance1 = atm(1000, 1500)
print(withdraw_balance1)
