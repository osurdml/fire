import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pylab
from osgeo import gdal


toa= gdal.Open('/home/rover/Documents/Programming/ash1_raster.toa')
fli= gdal.Open('/home/rover/Documents/Programming/ash1_raster.fli')
fli = fli.ReadAsArray()
toa= toa.ReadAsArray()

#print "%s", toa
"""
lookup = [];
for i in xrange(0, len(fli)):
	for i in xrange(0, len(fli[0])):
		lookup.append(0);
"""
lookup = toa;
np.sort(lookup);


print "%s", lookup


def animate(i):
	for fl


anim = animation.FuncAnimation(fig, animate, interval=20)

#plt.imshow (data1, interpolation='nearest', vmin=0)
plt.imshow (fli, interpolation='nearest', vmin=0)
plt.show()
