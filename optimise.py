import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from arctan import aggregate_curves, arctan_curves, find_lowest_x_for_y, plot_curves
from scipy.optimize import curve_fit, root_scalar
import pandas as pd
    # Define different coefficients and divisors for each curve
params = [
    {"coefficient": 1.36, "divisor": 2.95}
]

curves = arctan_curves(params)

x = curves[0][0]

# extract only the y-values from each curve for aggregation
y_values = [curve[1] for curve in curves]
aggregated_curve = aggregate_curves(y_values)
plot_curves(x, y_values, aggregated_curve)


# ---------------------------------------------------------------------------------------------------------

# # currently uses a linear interpolation method
# # try adapting into the arctan transform fit for interpolation
# # use hill climb (maybe, still dk what hillclimb actually is) 
# # to find the point where spend vs lift is best ratio... u know what i mean
# # dL/dS becomes unoptimal 

# # ---------------------------------------------------------------------------------------------------------
"""
def arctan_model(x, a, b, c, d):
    return a * np.arctan(b * x + c) + d

# fit arctan model to the data
params, _ = curve_fit(arctan_model, x, aggregated_curve)

# y given x using the fitted model
def get_y_given_x(x_value):
    a, b, c, d = params
    return float(arctan_model(x_value, a, b, c, d))

# x given y using root finding
def get_x_given_y(y_value):
    a, b, c, d = params
    def func(x): 
        return arctan_model(x, a, b, c, d) - y_value

    # iteratively trying steps and seeing where function changes sign
    for i in range(len(x) - 1):
        if func(x[i]) * func(x[i + 1]) < 0:
            result = root_scalar(func, bracket=[x[i], x[i + 1]], method='brentq')
            if result.converged:
                return float(result.root)
    return None 

x_value = 10
y_value = 1.8

print(f"y for x={x_value}: {get_y_given_x(x_value)}")
print(f"x for y={y_value}: {get_x_given_y(y_value)}")
"""
# # ---------------------------------------------------------------------------------------------------------


data = curves
df = pd.DataFrame(data, columns=['x', 'y', 'z'])
df.to_csv('arctan.csv', index=False)

target_y = 1.0
curve_index, min_x = find_lowest_x_for_y(curves, target_y)
print(f"The curve with the lowest x for y={target_y} is curve {curve_index} with x={min_x:.4f}")

