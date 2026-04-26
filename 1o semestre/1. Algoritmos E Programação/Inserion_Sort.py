# Algoritmo de Insertion Sort para ordenar uma lista de números. O algoritmo percorre a lista e, para cada elemento, insere-o na posição correta em relação aos elementos anteriores, garantindo que a parte da lista já processada esteja sempre ordenada.

def insertion_sort(my_list):
    for i in range(1, len(my_list)):
        key = my_list[i]
        print(f"Iteração {i}. Chave: {key}. Lista atual: {my_list}")
        j = i - 1
        print(f"Comparando a chave {key} com os elementos anteriores: {my_list[:i]}")
        while j >= 0 and my_list[j] > key:
            my_list[j + 1] = my_list[j]
            j -= 1
        my_list[j + 1] = key
    return my_list

my_list = [10, 32, 44, 55, 18, 27, 32, 45, 1, 3]
my_list_sorted = insertion_sort(my_list)
print(my_list_sorted)