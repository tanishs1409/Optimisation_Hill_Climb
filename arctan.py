import numpy as np
import matplotlib.pyplot as plt

def arctan_curves(params, x_range=(0, 10, 0.1), num_points=1000):
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

