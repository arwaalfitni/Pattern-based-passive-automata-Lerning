def get_threshold(filePath):
    # read all the values from the file
    with open(filePath, 'r') as file:
        values = file.readlines()
    # convert the values to int and store them in a list
    int_values = [int(value.strip()) for value in values]
    if not int_values:
        return None
    # calculate the threshold as 30% of the maximum value
    max_value = max(int_values)
    threshold = int(0.3 * max_value)
    return threshold
