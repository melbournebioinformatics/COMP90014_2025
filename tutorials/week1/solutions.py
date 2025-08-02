
import numpy as np

# Task 1
def selection_sort(items):
    """
    Sorts a list using selection sort
    """

    # Get the length of the array
    n = len(items)
    for i in range(n):
        # Find the index of the minimum item
        min_idx = i
        for j in range(i + 1, n, 1):
            if items[j] < items[min_idx]:
                min_idx = j
        # Swap the minimum item with the first unsorted item
        items[i], items[min_idx] = items[min_idx], items[i]
    return items


# Task 2
def merge(array1, array2):
    """
    merges two sorted lists into a single sorted list. 
    """

    pt1, pt2 = 0, 0
    merged_array = np.zeros(len(array1) + len(array2))
    while pt1 < len(array1) and pt2 < len(array2):
        if array1[pt1] <= array2[pt2]:
            merged_array[pt1 + pt2] = array1[pt1]
            pt1 += 1
        else:
            merged_array[pt1 + pt2] = array2[pt2]
            pt2 += 1
    while pt1 < len(array1):
        merged_array[pt1 + pt2] = array1[pt1]
        pt1 += 1
    while pt2 < len(array2):
        merged_array[pt1 + pt2] = array2[pt2]
        pt2 += 1
    return merged_array

