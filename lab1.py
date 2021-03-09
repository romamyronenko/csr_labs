import numpy as np

data = np.array([233, 303, 81, 129, 200, 82, 115, 228, 64, 17,
                 67, 648, 29, 39, 210, 10, 94, 465, 135, 312,
                 606, 698, 15, 764, 32, 45, 54, 13, 116, 24,
                 477, 16, 841, 95, 3, 79, 118, 208, 9, 59, 171,
                 295, 78, 67, 38, 57, 91, 18, 39, 324, 416,
                 270, 114, 25, 675, 287, 374, 119, 227, 5,
                 109, 94, 171, 226, 183, 350, 27, 64, 433, 88,
                 167, 152, 159, 319, 8, 162, 36, 488, 65, 77,
                 307, 522, 140, 65, 355, 482, 180, 29, 342,
                 233, 117, 182, 184, 113, 86, 630, 476, 136,
                 397, 66])

MALFUNCTION_PERCENTAGE = 0.62  # percentage of elements which can break down
TIME_WITHOUT_BREAKDOWN = 275
MALFUNCTION_INTENSITY_TIME = 648
N = len(data)

# sort the data for comfort
sorted_data = sorted(data)

mean_value = data.mean()  # average time until breaking down

# max value of data which is the last element of sorted
max_value = sorted_data[len(sorted_data) - 1]

k = 10  # splitting into k chunks
h = max_value / k

intervals = [round(interval * h, 2) for interval in range(k + 1)]


def data_sort_through_intervals(arr, intervals):
    data_intervals = []
    for element in arr:
        data_intervals.append([])
        for i in range(k):
            if intervals[i] <= element <= intervals[i + 1]:
                data_intervals[i].append(element)
    return data_intervals


# statistic frequency calculation (щільність)
def f_calculator(data_intervals, k):
    F = []
    for i in range(k):
        F.append(len(data_intervals[i]) / (N * h))
    return F


# find the index of interval the number is in
def find_the_interval(number, intervals):
    for i in range(k):
        if intervals[i] <= number <= intervals[i + 1]:
            return i


# probability working without breaking down
def probabilities(frequency):
    P = []
    for i in range(k):
        square = 0
        for j in range(i + 1):
            square += (frequency[j] * h)
        P.append(round(1 - square, 5))
    return P


# function for calculating T with specific percentage of breakable elements
def T(percentage, probability_arr, intervals):
    new_p_arr = probability_arr.copy()
    new_p_arr.insert(0, 1)
    for i in range(len(new_p_arr)):
        if new_p_arr[i] > percentage:
            new_p_arr.insert(i + 1, percentage)
    index = new_p_arr.index(percentage)
    d = round((new_p_arr[index + 1] - percentage) / (new_p_arr[index + 1] - new_p_arr[index - 1]), 2)
    T_value = round(intervals[index] - h * d, 2)
    return T_value


def probability_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    square = 0
    for i in range(number_of_interval + 1):
        if i != number_of_interval:
            square += (frequency_arr[i] * h)
        else:
            square += (frequency_arr[i] * (time - intervals[i]))
    p = round(1 - square, 4)
    return p


def intensity_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    p = probability_for_time(time, frequency_arr, intervals)
    return round(frequency_arr[number_of_interval] / p, 4)


data_intervals = data_sort_through_intervals(sorted_data, intervals)
print("Intervals: \n", intervals)

f_array = f_calculator(data_intervals, k)

p_array = probabilities(f_array)

t_value = T(MALFUNCTION_PERCENTAGE, p_array, intervals)
print("Середній наробіток до відмови: ", t_value)

p = probability_for_time(TIME_WITHOUT_BREAKDOWN, f_array, intervals)
print("Ймовірність часу до відмови: " + str(TIME_WITHOUT_BREAKDOWN) + " год" + "\n", p)

intensity = intensity_for_time(MALFUNCTION_INTENSITY_TIME, f_array, intervals)
print("Інтенсивність для " + str(MALFUNCTION_INTENSITY_TIME) + " год" + "\n", intensity)
