import time
import numpy as np
from typing import Callable, List, Tuple
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from .utils import safe_fit, safe_normalize

def analyze_time_complexity(func: Callable, input_generator: Callable[[int], any], 
                          sizes: List[int], num_trials: int = 3,
                          save_plot: bool = True, plot_path: str = 'time_complexity_plot.png') -> Tuple[str, float]:
    """
    Analyze the time complexity of a given function.
    
    Parameters:
    - func: Function to analyze
    - input_generator: Function that generates input of a given size
    - sizes: List of input sizes to test
    - num_trials: Number of trials for each input size
    - save_plot: Whether to save the plot to a file
    - plot_path: Path where to save the plot
    
    Returns:
    - complexity_class: String describing the likely time complexity
    - r_squared: R-squared value of the best fit
    """
    
    # Measure execution times
    times = []
    for size in sizes:
        size_times = []
        for _ in range(num_trials):
            input_data = input_generator(size)
            start_time = time.time()
            func(input_data)
            end_time = time.time()
            size_times.append(end_time - start_time)
        times.append(np.mean(size_times))
    
    # Convert to numpy arrays
    times = np.array(times)
    sizes = np.array(sizes)
    
    # Ensure we have valid measurements
    if np.all(times <= 0) or np.all(np.isclose(times, times[0])):
        print("Warning: Invalid time measurements detected")
        return "Unknown", 0.0
    
    # Define complexity classes with safer transformations
    complexity_classes = {
        'O(n)': (lambda x: x, 'Linear'),
        'O(n log n)': (lambda x: x * np.log2(x + 1), 'Linearithmic'),
        'O(n²)': (lambda x: x**2, 'Quadratic'),
        'O(n³)': (lambda x: x**3, 'Cubic'),
        'O(log n)': (lambda x: np.log2(x + 1), 'Logarithmic'),
    }
    
    best_fit = None
    best_r_squared = -float('inf')
    best_complexity = ''
    
    # Normalize times once
    times_normalized = safe_normalize(times)
    
    for complexity, (transform, name) in complexity_classes.items():
        try:
            # Transform and normalize sizes
            transformed_sizes = transform(sizes)
            if np.any(np.isinf(transformed_sizes)) or np.any(np.isnan(transformed_sizes)):
                print(f"Warning: Invalid transformation for {complexity}")
                continue
                
            transformed_sizes_normalized = safe_normalize(transformed_sizes)
            
            # Perform fitting
            polynomial, r_squared = safe_fit(transformed_sizes_normalized, times_normalized)
            
            if polynomial is not None and r_squared > best_r_squared:
                best_r_squared = r_squared
                best_complexity = complexity
                best_fit = (polynomial, transformed_sizes_normalized, times_normalized)
                
        except Exception as e:
            print(f"Warning: Failed to fit {complexity}: {str(e)}")
            continue
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.scatter(sizes, times, label='Measured times', color='blue', alpha=0.6)
    
    if best_fit is not None:
        polynomial, transformed_sizes_normalized, _ = best_fit
        x_range = np.linspace(min(sizes), max(sizes), 100)
        transform = complexity_classes[best_complexity][0]
        
        # Safely transform and normalize x_range
        x_range_transformed = transform(x_range)
        x_range_normalized = safe_normalize(x_range_transformed)
        
        # Generate predictions and denormalize
        y_pred_normalized = polynomial(x_range_normalized)
        y_pred = y_pred_normalized * (np.max(times) - np.min(times)) + np.min(times)
        
        plt.plot(x_range, y_pred, 'r-', 
                label=f'Best fit ({best_complexity})\nR² = {best_r_squared:.4f}',
                alpha=0.8)
    
    plt.xlabel('Input size')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_plot:
        Path(plot_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Plot saved to: {plot_path}")
    
    return best_complexity, best_r_squared
