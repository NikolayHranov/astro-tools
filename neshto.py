import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


BVindex = 0

#The popular empirical correlation between the B-V index and the Temperature
t = 4600*(1/(0.92*BVindex+1.7)+1/(0.92*BVindex+0.62))

#The correlance between effective temperature of a star on the MS and the lifespan of it on
#the MS. Source: [3]
x = np.array([2900, 3800, 5000, 6000, 7000, 11000, 17000, 22000, 28000, 35000, 44500])
y = np.array([2000000, 200000, 30000, 10000, 2000, 200, 70, 20, 10, 7, 3.4])

f = interp1d(x, y)
x_interp = np.linspace(min(x), max(x), 400)
y_interp = f(x_interp)

#print(f(t))
#this gives us the time in Myr that a star with an effective temperature T stays on the surface
#thus giving us the age of the open star cluster
plt.scatter(x, y, color='blue', label='Data points')

plt.plot(x_interp, y_interp, color='red', label='Interpolation')

plt.title('Linear Interpolation')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()