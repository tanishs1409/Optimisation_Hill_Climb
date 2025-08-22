## Optimal Spend Estimation using Arctangent Response Curves

This script is using various methods to determine the optimal x-value (Spend) when given a target y-value (Lift). The response curves are modelled as an arctangent function with varying coefficient and divisor values; 20 such curves were generated to test the methods listed below. 

Three methods were explored: 

### 1. Aggregation of arctangent transforms by mean values. (interpolation_arctangent.py)
A flexible arctangent function was fitted to aggregated_curve using non-linear least squares optimisation to model non-linear returns.
Interpolation was used and determine values in both directions - one function finds the corresponding y_value given a target x_value, and another finds the corresponding x_value given a target y_value. Uses root-finding (brentq method) - searches for a sign change in the function to locate the root.

However, this only operates on the aggregate curve. It does not account for situations like, in this case specifically, when we want to find the smallest x_value (Spend) given the target y_value (Lift). In marketing context, we want to achieve the target return from the smallest possible spend. 

### 2. Finding the most efficient curve for a target lift. (interpolation_arctangent.py)
Identifies which curve reaches a target lift value with the least spend across all available curves.
A list of curves is taken as a tuple of x and y arrays, and the function searches for the curve that reaches the specified targey_y value. Any curve that cannot reach the target lift is skipped, and for valid curves, the point where lift is closest to the target is determined.

One of the problems faced here, is that since the values were being stored as tuples, there was too much data to unpack for the function. 2 values were expected, but a thousand for each x and y was being scanned. This was discovered by saving the curves as an excel file and seeing how many values were in each cell. 
This was resolved by writing an iterative script that created a dictionary for x, y values for each point, saving this as a csv and using that rather than the raw curves data.

### 3. Hill Climb (optimise.py)
A greedy hill-climbing algorithm was implemented to find the most efficient curve that reaches the given target y_value with the lowest x_value.
Each curve is iterated through, starting from the beginning and only 'climbing' forwards if the next point is closer to the target lift. When no further improvements are found, and if the current point is within a tolerance limit of the target y_value, it checks if the x_value is lower than the best found so far. The tolerance is set at 0.01, but can be changed.



