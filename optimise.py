import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from arctan import aggregate_curves, arctan_curves, plot_curves
from scipy.optimize import curve_fit, root_scalar
import pandas as pd
    # Define different coefficients and divisors for each curve
params = [
    {"coefficient": 2.22, "divisor": 3.49},
    {"coefficient": 3.39, "divisor": 3.17},
    {"coefficient": 2.23, "divisor": 0.23},
    {"coefficient": 4.61, "divisor": 0.38},
    {"coefficient": 0.12, "divisor": 3.56},
    {"coefficient": 1.09, "divisor": 2.42},
    {"coefficient": 4.93, "divisor": 1.69},
    {"coefficient": 4.77, "divisor": 1.19},
    {"coefficient": 1.06, "divisor": 4.33},
    {"coefficient": 4.73, "divisor": 2.72},
    {"coefficient": 0.38, "divisor": 4.29},
    {"coefficient": 1.87, "divisor": 2.51},
    {"coefficient": 3.92, "divisor": 1.74},
    {"coefficient": 3.12, "divisor": 0.37},
    {"coefficient": 4.46, "divisor": 1.63},
    {"coefficient": 1.65, "divisor": 1.19},
    {"coefficient": 3.8, "divisor": 0.77},
    {"coefficient": 0.73, "divisor": 3.52},
    {"coefficient": 3.9, "divisor": 0.28},
    {"coefficient": 0.45, "divisor": 2.37}
]


curves = arctan_curves(params)
x = curves[0][0]
# extract only the y-values from each curve for aggregation
y_values = [curve[1] for curve in curves]
aggregated_curve = aggregate_curves(y_values)

plot_curves(x, y_values, aggregated_curve)

# ---------------------------------------------------------------------------------------------------------

# flatten data
flattened_data = []
for x, y_values, param in curves:
    for x, y_values in zip(x, y_values):
        flattened_data.append({
            "x": x,
            "y": y_values,
            "coefficient": param["coefficient"],
            "divisor": param["divisor"]
        })

df = pd.DataFrame(flattened_data)
df.to_csv("arctan_fixed.csv", index=False)

# ---------------------------------------------------------------------------------------------------------

df = pd.read_csv("arctan_fixed.csv")
grouped = df.groupby(["coefficient", "divisor"])
curves = [(group["x"].values, group["y"].values) for _, group in grouped]

target_y = 4.6

def hill_climb(curves, target_y):
    best_x = float("inf")
    best_curve_index = -1

    for i, (x, y) in enumerate(curves):
        # start at the first index
        current_index = 0
        while current_index < len(y) - 1:
            # move to the next index if it gets closer to the target y
            if abs(y[current_index + 1] - target_y) < abs(y[current_index] - target_y):
                current_index += 1
            else:
                break  # stop climbing when no improvement

        # check if this curve reaches the target y within tolerance
        if abs(y[current_index] - target_y) < 0.01:  # tolerance
            if x[current_index] < best_x:
                best_x = x[current_index]
                best_curve_index = i

    if best_curve_index == -1:
        raise ValueError(f"No curve reaches the target y-value: {target_y} within tolerance.")
    return best_curve_index, best_x


curve_index, min_x = hill_climb(curves, target_y)
print(f"Hill Climb: The curve with the lowest x for y={target_y} is curve {curve_index} with x={min_x:.4f}")

# ---------------------------------------------------------------------------------------------------------

