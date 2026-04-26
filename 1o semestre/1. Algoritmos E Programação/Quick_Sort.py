# Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)
my_list = [10, 32, 44, 55, 18, 27, 32, 45, 1, 3]
sorted_list = quick_sort(my_list)
print(sorted_list)  # [1, 3, 10, 18, 27, 32, 32, 44, 45, 55]