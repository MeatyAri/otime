import pytest
from otime import analyze_time_complexity

def test_bubble_sort_complexity():
    def bubble_sort(arr):
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    sizes = [100, 200, 400]
    complexity, r_squared = analyze_time_complexity(
        bubble_sort,
        lambda x: list(range(x)),
        sizes,
        save_plot=False
    )
    
    assert complexity == "O(n²)"
    assert r_squared > 0.9
