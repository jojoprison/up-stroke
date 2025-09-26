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
