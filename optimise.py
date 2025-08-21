import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from arctan import aggregate_curves, arctan_curves, plot_curves
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

# ---------------------------------------------------------------------------------------------------------

# Load the CSV file
df = pd.read_csv("arctan_fixed.csv")

# Group by curve parameters
grouped = df.groupby(["coefficient", "divisor"])

# Convert each group into (x_array, y_array) format
curves = [(group["x"].values, group["y"].values) for _, group in grouped]

# Define the target y-value
target_y = 1.5

# Hill climbing algorithm
def hill_climb_find_lowest_x(curves, target_y):
    best_x = float("inf")
    best_curve_index = -1

    for i, (x, y) in enumerate(curves):
        # Start at the first index
        current_index = 0
        while current_index < len(y) - 1:
            # Move to the next index if it gets closer to the target y
            if abs(y[current_index + 1] - target_y) < abs(y[current_index] - target_y):
                current_index += 1
            else:
                break  # Stop climbing when no improvement

        # Check if this curve reaches the target y within tolerance
        if abs(y[current_index] - target_y) < 0.05:  # tolerance
            if x[current_index] < best_x:
                best_x = x[current_index]
                best_curve_index = i

    if best_curve_index == -1:
        raise ValueError(f"No curve reaches the target y-value: {target_y} within tolerance.")

    return best_curve_index, best_x

# Run the hill climbing algorithm
curve_index, min_x = hill_climb_find_lowest_x(curves, target_y)

# Output the result
print(f"Hill Climb: The curve with the lowest x for y={target_y} is curve {curve_index} with x={min_x:.4f}")

# ---------------------------------------------------------------------------------------------------------
