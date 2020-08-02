a_list = ['a']
a_list = a_list + [2.0, 3]
print(a_list)

a_list.append(True)
print(a_list)

a_list.extend(['four', 'Ω'])
print(a_list)

a_list.insert(0, 'Ω')
print(a_list)