"""
Written By: Ryan Skeele
Oregon State University
Robotic Decision Making Laboratory

Wildfire UAV exploration/exploitation monitoring simulation
"""
#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pylab
from osgeo import gdal
import matplotlib.animation as animation

timestep= 100   # Timestep from navigation algorithm
lut= dict()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)


toa= gdal.Open('data/ash1_raster.toa')
fli= gdal.Open('data/ash1_raster.fli')
fli = fli.ReadAsArray()
toa= toa.ReadAsArray()
anim_plot= [[0 for i in range(len(fli[0]))] for j in range(len(fli))]


def _floor(i, step):
    return int(i*1000 / step) * step


# Packing function:
def pack_lut(lut, toa, timestep):
    max_time = 0
    for i in xrange(0, len(toa)):
        for j in xrange(0, len(toa[0])):
            if toa[i][j] == -1:
                continue;
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

def uav():	
	fov_h= 45	#degrees
	fov_v= 37	#degrees
	speed_max= 16	#m/s
	flight_time = 50 #minutes
	turning_radius= 3 #radius meters
	return uav_position




print len(fli)*len(fli[0])
total = 0
for k,v in lut.items():
    total += len(v)
print total

im = ax.matshow(anim_plot)
im.set_clim(0, 1000)
#fig.show()
totalplotted = 0

for i in range(0,max_time,timestep):
    if lut.get(i) is not None:
        totalplotted += len(lut[i])
        print len(lut[i]), "cells to plot,", totalplotted, "plotted so far"
        for x,y in lut[i]:
            #print anim_plot[x][y], "setting to", fli[x][y], ":"
            anim_plot[x][y]= fli[x][y]
            #for i in (x-1,x,x+1):
            #    for j in (y-1,y,y+1):
            #        print anim_plot[i][j]
        im.set_data(anim_plot)
    plt.pause(0.001)

plt.show()   # Stop at end.

#anim = animation.FuncAnimation(fig, anim, interval=1)

