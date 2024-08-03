import numpy as np
from numpy import arange
from scipy.optimize import curve_fit
from matplotlib import pyplot

# Define the hyperbola function
# def hyperbola(x, a, b):
    # return a / x + b
    
def hyperbola(x, a, b):
    return ((a / x) + b)

# def hyperbola(x, a, b, c):
    # return ((a / c * x) + b)

# Given conditions for fitting the hyperbola
x_data = np.array([0.5, 1.5, 3, 6, 11.5, 15])
y_data = np.array([5, 4, 3, 2, 1.5, 1.25])

# Fit the hyperbola curve to the given data points
params, _ = curve_fit(hyperbola, x_data, y_data)
# summarize the parameter values
a, b = params
# plot input vs output
pyplot.scatter(x_data, y_data)
# define a sequence of inputs between the smallest and largest known inputs
x_line = arange(min(x_data), max(x_data), 1)
# calculate the output for the range
# y_line = objective(x_line, a, b, c, d, e, f)
y_line = hyperbola(x_line, a, b)
# create a line plot for the mapping function
pyplot.plot(x_line, y_line, '--', color='red')
pyplot.show()

def calculate_percentage_change(lst):
    pct_changes = []
    for i in range(1, len(lst)):
        pct_change = abs(lst[i] - lst[i-1]) / lst[i-1] * 100
        pct_changes.append(pct_change)
    return pct_changes

def get_max_allowed_ratio(min_value):
    """Determine the maximum allowed ratio using the hyperbola."""
    return hyperbola(min_value, a, b)

def split_cluster(cluster, ratio_threshold):
    """Further split the cluster if the ratio between max and min exceeds the threshold."""
    new_clusters = []
    current_group = [cluster[0]]

    for i in range(1, len(cluster)):
        if (max(current_group) / min(current_group)) > ratio_threshold:
            new_clusters.append(current_group[:])
            current_group = [cluster[i]]
        else:
            current_group.append(cluster[i])

    new_clusters.append(current_group)
    return new_clusters

def cluster_elements(lst, threshold):
    pct_changes = calculate_percentage_change(lst)
    clusters = []
    current_group = [lst[0]]

    for i in range(len(pct_changes)):
        next_element = lst[i + 1]
        current_min = min(current_group)
        current_max = max(current_group)
        ratio_threshold = get_max_allowed_ratio(current_min)
        
        if pct_changes[i] > threshold or (current_max / current_min) > ratio_threshold:
            clusters.append(current_group[:])
            current_group = [next_element]
        else:
            current_group.append(next_element)
    
    clusters.append(current_group)

    # Further split clusters based on the ratio condition
    final_clusters = []
    for cluster in clusters:
        current_min = min(cluster)
        ratio_threshold = get_max_allowed_ratio(current_min)
        if (max(cluster) / min(cluster)) > ratio_threshold:
            final_clusters.extend(split_cluster(cluster, ratio_threshold))
        else:
            final_clusters.append(cluster)

    return final_clusters

# Example usage
lst = [0.01, 0.02, 0.05, 0.09, 0.1, 1, 2, 3, 4, 8, 9, 10, 89, 90, 100, 110, 150, 500, 600, 700, 800, 1000, 1001, 1002, 10000, 10010, 20000, 30000]
threshold = 100  # Threshold value for percentage change
result = cluster_elements(lst, threshold)

for idx, group in enumerate(result, 1):
    print(f"Group {idx}: {group}")
