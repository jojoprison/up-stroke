# найти минимальный остаток от деления / 3

nums = [1, 2, 3, 4, 5]

min_ost = 1000

for num in nums:
    print(f'cur_ost by {num}', num % 3)

    if num % 3 < min_ost:
        min_ost = num % 3

    print('min_ost', min_ost)

print('res',min_ost)
