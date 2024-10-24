import numpy as np

def safe_normalize(x):
    """Safely normalize an array, handling edge cases."""
    min_val = np.min(x)
    max_val = np.max(x)
    if np.isclose(min_val, max_val):
        return np.zeros_like(x)
    return (x - min_val) / (max_val - min_val)

def safe_fit(x, y):
    """Safely perform polynomial fitting with error handling."""
    try:
        # Add small noise to prevent perfect collinearity
        x = x + np.random.normal(0, 1e-10, x.shape)
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        y_pred = polynomial(x)
        
        # Calculate R-squared
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        ss_res = np.sum((y - y_pred) ** 2)
        
        if np.isclose(ss_tot, 0):
            r_squared = 0
        else:
            r_squared = 1 - (ss_res / ss_tot)
            
        return polynomial, r_squared
    except Exception as e:
        return None, float('-inf')
