# Algoritmo de Bubble Sort para ordenar uma lista de números. O algoritmo percorre a lista várias vezes, comparando elementos adjacentes e trocando-os de posição se estiverem na ordem errada. O processo é repetido até que a lista esteja ordenada.

def bubble_sort(my_list):
     n = len(my_list)
     for i in range(n):
         print(f"Iteração {i}. Lista atual: {my_list}")
         for j in range(0, n - i - 1):
             print(f"Iteração {i}, comparação {j}. Comparando números {my_list[j]} e {my_list[j + 1]}")
             if my_list[j] > my_list[j + 1]:
                 my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]
     return my_list

my_list = [10, 32, 44, 55, 18, 27, 32, 45, 1, 3]
my_list_sorted = bubble_sort(my_list)
print(my_list_sorted)