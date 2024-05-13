def calculate_percentage_change(lst):
    pct_changes = []
    for i in range(1, len(lst)):
        pct_change = abs(lst[i] - lst[i-1]) / lst[i-1] * 100
        pct_changes.append(pct_change)
    return pct_changes

def cluster_elements(lst, threshold):
    pct_changes = calculate_percentage_change(lst)
    clusters = []
    current_group = [lst[0]]

    for i in range(len(pct_changes)):
        if pct_changes[i] > threshold:
            clusters.append(current_group[:])
            current_group = [lst[i+1]]
        else:
            current_group.append(lst[i+1])

    clusters.append(current_group)

    return clusters

# Example usage
lst = [2, 3, 4, 8, 9, 10, 89, 90, 1000, 1001, 1002, 10000, 10100,100000,100500]
threshold = 50  # You can adjust this threshold as needed
result = cluster_elements(lst, threshold)
for idx, group in enumerate(result, 1):
    print(f"Group {idx}: {group}")
