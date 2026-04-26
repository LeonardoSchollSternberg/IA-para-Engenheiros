my_list = [3,7,10,2,5,8,9,1,4,6]
print(my_list)  # [3,7,10,2,5,8,9,1,4,6]

# Revertendo a lista com o método reverse()
my_list_reversed =  my_list.copy()  # Criando uma cópia da lista original para não modificá-la
my_list_reversed.reverse()
print(my_list_reversed)  # [6,4,1,9,8,5,2,10,7,3]

# Revertendo a lista com o slicing
reversed_list = my_list[::-1]
print(reversed_list)  # [3,7,10,2,5,8,9,1,4,6]

# Revertendo a lista com o método reversed()
reversed_list = list(reversed(my_list))
print(reversed_list)  # [3,7,10,2,5,8,9,1,4,6]

# Revertendo a lista com o loop for
reversed_list = []
for i in range(len(my_list)-1, -1, -1):
    reversed_list.append(my_list[i])
print(reversed_list)  # [3,7,10,2,5,8,9,1,4,6]

# Revertendo a lista com o método pop()
my_list_pop = my_list.copy()  # Criando uma cópia da lista original para não modificá-la
reversed_list = []
while my_list_pop:
    reversed_list.append(my_list_pop.pop())
print(reversed_list)  # [3,7,10,2,5,8,9,1,4,6]

# Revertendo a lista com o método insert()
reversed_list = []
for item in my_list:
    reversed_list.insert(0, item)
print(reversed_list)  # [3,7,10,2,5,8,9,1,4,6]

# Reverti utilizando o método reverse, slicing, reversed(), loop for, pop() e insert()