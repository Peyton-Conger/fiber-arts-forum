def calculate_gaps(sorted_list):
    if not isinstance(sorted_list, list):
        raise TypeError('sorted_list must be a list')
    if len(sorted_list) < 2:
        return []
    return [sorted_list[i+1] - sorted_list[i] for i in range(len(sorted_list)-1)]
