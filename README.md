# OTime: Time Complexity Analyzer
A Python package for empirically analyzing the time complexity of functions.

## Installation
```bash
pip install otime
```

## Usage
```python
from otime import analyze_time_complexity

def my_function(data):
    # Your function here
    pass

sizes = [100, 200, 400, 800, 1600]
complexity, r_squared = analyze_time_complexity(
    my_function,
    lambda x: list(range(x)),  # Input generator
    sizes
)
print(f"Time complexity: {complexity}")
print(f"R-squared: {r_squared}")
```

## More examples
```python
from otime import analyze_time_complexity

# Example usage
def example_input_generator(size):
    """Generate a list of given size for testing."""
    return size

def func(n):
    for i in range(n):
        j = i * i
        while j > 0:
            j //= 4

sizes = [100, 200, 400, 800, 1600, 3200]
complexity, r_squared = analyze_time_complexity(
    func, 
    example_input_generator,
    sizes,
    save_plot=True
)
print(f"\nResults:")
print(f"Detected time complexity: {complexity}")
print(f"R-squared value: {r_squared:.4f}")
```

## Features
- Automatic time complexity detection
- Visual plotting of results
- Support for common complexity classes
- Robust numerical analysis

## License
MIT License
