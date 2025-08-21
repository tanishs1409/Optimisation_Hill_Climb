


# # currently uses a linear interpolation method
# # try adapting into the arctan transform fit for interpolation
# # use hill climb (maybe, still dk what hillclimb actually is) 
# # to find the point where spend vs lift is best ratio... u know what i mean
# # dL/dS becomes unoptimal 

# # ---------------------------------------------------------------------------------------------------------

# ARCTAN TRANSF0RM INTERPOLATION FOR GRAPH

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
# ---------------------------------------------------------------------------------------------------------

# THIS TAKES A FIXED Y VALUE, THEN FINDS THE CORRESPONDING SMALLEST X VALUE ACROSS ALL CURVES

"""

def find_lowest_x_for_y(curves, target_y):
    min_x = float('inf')
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

"""