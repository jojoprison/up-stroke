# 1. Посчитать сумму всех чисел в списке, кратных 3.

lst = [2, 3, 5, 8, 99]
summa = 0
for i in lst:
    if i % 3 == 0:
        summa += i

print(summa)