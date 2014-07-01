import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pylab
from osgeo import gdal

timestep= 1   # Timestep from navigation algorithm

toa= gdal.Open('/home/rover/Documents/Programming/ash1_raster.toa')
fli= gdal.Open('/home/rover/Documents/Programming/ash1_raster.fli')
fli = fli.ReadAsArray()
toa= toa.ReadAsArray()

#print "%s", toa

lookup = []
for i in xrange(0, len(fli)):
	for j in xrange(0, len(fli[0])):
		lookup.append([i])

# Data of Lookup will look something like this:
{
   -1: set([(5,0), (5,1), (5,2)]),
    0: set([(0,0), (0,1), (0,2)]),
    1: set([(1,0), (1,1)]),
    5: set([(3,0), (3,1), (3,2), (3,3), (4,2), (4,4)])
}

def _floor(i, step):
    int(i*1000 / step) * step

# You need a packing function:
def pack_lut(lut, toa, timestep):
  	for i in xrange(0, len(toa)):
        	for j in xrange(0, len(toa[0])):
            		if toa[i][j] == -1:
            			continue;
        		time = _floor(toa[i][j])
	        	cell = (i,j)
        		if lut[time] is None:
	            		lut[time] = set(cell)
        		else:
        	    		lut[time].add(cell)   # TODO: need to use set, not list

        

print "%s", lookup
  
"""def animate(i):
         for fli
			fig = plt.imshow (data1, interpolation='nearest', vmin=0)
			fig = plt.imshow (fli, interpolation='nearest', vmin=0)

anim = animation.FuncAnimation(fig, animate, frames= xrange(100), fargs= (), interval=20)
plt.show()"""
