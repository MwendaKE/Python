import numpy
import matplotlib.pyplot as plot


mean_of_data = 10
std_of_data = 5
num_of_samples = 500

# Generate normal distribution data

data = numpy.random.normal(loc=mean_of_data, scale=std_of_data, size=num_of_samples)

# Plot graph (Histogram)

plot.hist(data, bins=30, density=True, edgecolor='red', alpha=0.8, color='b')

# Show graph

plot.title('Normal Distribution Graph From Random Values')
plot.xlabel('X Values')
plot.ylabel('Y Values')

plot.show()