"""
Written By: Ryan Skeele
Oregon State University
Robotic Decision Making Laboratory

Wildfire UAV exploration/exploitation monitoring simulation
"""
#!/usr/bin/env python2

import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pylab
from osgeo import gdal
import matplotlib.animation as animation
np.set_printoptions(threshold='nan')
timestep= 100   # Timestep from navigation algorithm
lut= dict()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)


toa= gdal.Open('data/ash1_raster.toa')
fli= gdal.Open('data/ash1_raster.fli')
fli = fli.ReadAsArray()
toa= toa.ReadAsArray()

anim_plot= np.ndarray((len(fli), len(fli[0])))
fire_map= np.ndarray((len(fli), len(fli[0])))


"""
for i in range(len(fli))
	for j in range(len(fli)
	if fli(i,j)
		print fli
"""

class uav():	

	fov_h= 45	#degrees
	fov_v= 37	#degrees
	speed_max= 16	#m/s
	flight_time = 50 #minutes
	turning_radius= 3 #radius meters
	start_x= 0
	start_y= 0
	pose= 45

uav1 =uav()
print uav1.fov_h


"""
Notes

hotspot > 100, or do gradients and find max in gradient then keep track of x gradients
take in data, use centers to determine if in range
make movement decision
move
"""
#time cutoff
def _floor(i, step):
    return int(i*1000 / step) * step


# Packing function:
def pack_lut(lut, toa, timestep):
    max_time = 0
    for i in xrange(0, len(toa)):
        for j in xrange(0, len(toa[0])):
            if toa[i][j] == -1:
                continue
            time = _floor(toa[i][j], timestep)
            cell = (i,j)
            if lut.get(time) is None:
                lut[time] = set([cell])
            else:
                lut[time].add(cell)   
            if time > max_time:
                max_time = time
    return max_time

max_time = pack_lut(lut, toa, timestep)



"""
print len(fli)*len(fli[0])
total = 0
for k,v in lut.items():
    total += len(v)
print total
"""
im = ax.matshow(anim_plot)
im.set_clim(0, 1000)
#fig.show()
totalplotted = 0

for i in range(0,max_time,timestep):
    if lut.get(i) is not None:
        totalplotted += len(lut[i])


        #print len(lut[i]), "cells to plot,", totalplotted, "plotted so far"
        for x,y in lut[i]:
            fire_map[x][y]= fli[x][y]
	    #print anim_plot[x][y], "setting to", fli[x][y], ":"
            anim_plot[x][y]= fli[x][y]
            #for i in (x-1,x,x+1):
            #    for j in (y-1,y,y+1):
            #        print anim_plot[i][j]
           
	frontier = fire_map > 0
	frontier = convolve2d(frontier, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], mode='same')

	frontier = np.logical_and(frontier < 8, frontier > 0)
	frontier = np.where(frontier == True, fire_map, np.zeros_like(fire_map))
		

	im.set_data(frontier)
    plt.pause(0.001)

plt.show()   # Stop at end.

#anim = animation.FuncAnimation(fig, anim, interval=1)

