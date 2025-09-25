lst = [2, 3, 5, 6, 8, 12, 99]
summa = 0
for i in lst:
    if i % 2 == 0 and i % 3 == 0:
        summa += i

print(summa)