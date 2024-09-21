import numpy
import statistics


def calculate_mode(data):
    try:
        mode = statistics.mode(data_list)
        
    except statistics.StatisticsError:
        mode = "No mode"
        
    return mode
       
         
mean_of_data = 10
std_of_data = 5
num_of_samples = 500


# Generate random data using numpy

data = numpy.random.normal(loc=mean_of_data, scale=std_of_data, size=num_of_samples)


# Convert the numpy Array to python list

data_list = data.tolist()


# Data statistics

mean_value = numpy.mean(data)
median_value = numpy.median(data)
variance_value = numpy.var(data, ddof=1)  # ddof=1 for sample variance
std_value = numpy.std(data, ddof=1)  # ddof=1 for sample std

mode_value = calculate_mode(data_list)

# Quartiles

first_quartile = numpy.percentile(data, 25) # ¼
second_quartile = numpy.percentile(data, 50)  # Equal to median (²/4 or ½)
third_quartile = numpy.percentile(data, 75) # ¾ 

# Deciles and Percentiles

deciles = numpy.percentile(data, numpy.arange(0, 90, 10))
percentiles = numpy.percentile(data, [1, 5, 10, 25, 50, 75, 90, 95, 99])


# Printing Results:

print()
 
print(f" > Mean = {mean_value}")
print(f" > Median = {median_value}")
print(f" > Mode = {mode_value}")
print(f" > Variance = {variance_value}")
print(f" > Std = {std_value}")

print()

print(f" > 1st Quartile (Q1) = {first_quartile}")
print(f" > 2nd Quartile (Q2 = Median = {second_quartile}")
print(f" > 3rd Quartile (Q3) = {third_quartile}")

print()

print(f" > Selected Deciles: \n")

for decile in deciles:
    print(f"  • {decile}")
    
print()

print(f" > Selected Percentiles: \n")

for percentile in percentiles:
    print(f"  • {percentile}")

print()

''' 
INSIGHT: 7th decile is equal to 70th percentile and 8th decile
 is equal to 80th percentile.
'''