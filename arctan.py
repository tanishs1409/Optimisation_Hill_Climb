import numpy as np
import matplotlib.pyplot as plt

def arctan_curves(params, x_range=(0, 1.1, 0.1), num_points=1):
    x = np.linspace(x_range[0], x_range[1], num_points)

    curves = []
    for param in params:
        y = param["coefficient"] * np.arctan(x / param["divisor"])
        # Ensure y values are strictly positive
        y = np.maximum(y, 0.01)
        curves.append((x, y, param))
    return curves


# function to aggregate multiple curves into a single curve
def aggregate_curves(curves):  
    # convert list of y-value arrays into a NumPy array for easier manipulation
    curves_array = np.array(curves)
    # aggregate by taking the mean across all curves at each x-value
    aggregated = np.mean(curves_array, axis=0)
    return aggregated


def plot_curves(x, curves, aggregated_curve):
    plt.figure(figsize=(10, 6))  # Set figure size
    # plot each individual curve
    for i, y in enumerate(curves):
        plt.plot(x, y, linestyle='--', label=f"Curve {i+1}")
    plt.plot(x, aggregated_curve, label="Aggregated Curve", linewidth=2, color="black")
    plt.title("Spend vs Lift")
    plt.xlabel("Spend / 000s")
    plt.ylabel("Lift / 000s")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def find_lowest_x_for_y(curves, target_y):
    min_x = 0
    curve_index = -1
    found_valid = False
    print(type(curves))
    for i, (x, y) in enumerate(curves):
        if target_y < np.min(y) or target_y > np.max(y):
            continue  # Skip curves that can't reach the target y
        idx = (np.abs(y - target_y)).argmin()
        if x[idx] < min_x:
            min_x = x[idx]
            curve_index = i
            found_valid = True
    if not found_valid:
        raise ValueError(f"No curve reaches the target y-value: {target_y}")
    return curve_index, min_x
