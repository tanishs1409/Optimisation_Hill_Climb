import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from arctan import aggregate_curves, arctan_curves, find_lowest_x_for_y, plot_curves
from scipy.optimize import curve_fit, root_scalar
import pandas as pd
    # Define different coefficients and divisors for each curve
params = [
    {"coefficient": 1.36, "divisor": 2.95},
    {"coefficient": 2.42, "divisor": 1.66}
]

curves = arctan_curves(params)
print("curves", curves)

x = curves[0][0]

# extract only the y-values from each curve for aggregation
y_values = [curve[1] for curve in curves]


aggregated_curve = aggregate_curves(y_values)

print("aggcurve", aggregated_curve)

plot_curves(x, y_values, aggregated_curve)


# ---------------------------------------------------------------------------------------------------------

# Flatten the data
flattened_data = []
for x, y_values, param in curves:
    for x, y_values in zip(x, y_values):
        flattened_data.append({
            "x": x,
            "y": y_values,
            "coefficient": param["coefficient"],
            "divisor": param["divisor"]
        })

# Create a DataFrame and save to CSV
df = pd.DataFrame(flattened_data)
df.to_csv("arctan_fixed.csv", index=False)


# saving the x y and param values for curves into an excel file to see how its being split up
# data = curves
# df = pd.DataFrame(data, columns=['x', 'y', 'z'])
# df.to_csv('arctan.csv', index=False)

# Load the CSV
df = pd.read_csv("arctan_fixed.csv")

# Group by curve parameters
grouped = df.groupby(["coefficient", "divisor"])

# Convert each group into (x_array, y_array) format
curves = [(group["x"].values, group["y"].values) for _, group in grouped]

# Define the target y-value
target_y = 1.5

# Use your function
curve_index, min_x = find_lowest_x_for_y(curves, target_y)
print(f"The curve with the lowest x for y={target_y} is curve {curve_index} with x={min_x:.4f}")


