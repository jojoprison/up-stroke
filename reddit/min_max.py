list_1 = []
numb = 0
summer = 0

while not len(list_1) == 5:
    numb = int(input('input number:\n'))
    list_1.append(numb)

for i in range(len(list_1)):
    summer = sum(list_1)
    break

average = int(summer / len(list_1))
print(summer)
print(average)
print(min(list_1))
print(max(list_1))
