"""
Written By: Ryan Skeele
Oregon State University
Robotic Decision Making Laboratory

Wildfire UAV exploration/exploitation monitoring simulation
"""
#!/usr/bin/env python2

TIMESTEP = 0.1

import math
import numpy as np
from scipy.signal import convolve2d
from skimage.draw import polygon, circle
from skimage.transform import rotate
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pylab
from osgeo import gdal
import matplotlib.animation as animation

np.set_printoptions(threshold='nan')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

toa= gdal.Open('data/ash1_raster.toa')
fli= gdal.Open('data/ash1_raster.fli')
fli = fli.ReadAsArray()
toa= toa.ReadAsArray()

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

view_mask = np.zeros((100, 100))
rr, cc = polygon(np.array([30, 30, 50]), np.array([40, 60, 50]))
view_mask[rr, cc] = 1

fire_map = np.zeros_like(fli)

im = ax.matshow(fire_map)
im.set_clim(0, 1000)

max_time = math.ceil(np.amax(toa))

for t in np.arange(0, max_time, TIMESTEP):
	fire_map = np.logical_and(toa < t, toa > 0)
	fire_map = np.where(fire_map, fli, np.zeros_like(fli))

	frontier = fire_map > 0

	frontier = convolve2d(frontier, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], mode='same')
		
	frontier = np.logical_and(frontier < 8, frontier > 0)

	frontier = np.where(frontier == True, fire_map, np.zeros_like(fire_map))

	uav_pos = (t * 20, t * 20) #this will be updated to get locations from algorithm.
	view_mask_rot = rotate(view_mask, t * 10) #this too
	view_mask_rot = view_mask_rot * 100

	#view_mask_rot_tf= np.logical_and(view_mask_rot, np.zeros_like(view_mask_rot))


	#print view_mask_rot_tf

	# fire_map=np.logical_and(frontier[uav_pos[0]:(uav_pos[0]+100),uav_pos[1]:(uav_pos[1]+100)], view_mask_rot)	

	#print fire_map

	# np.where(fire_map == True, fire_map[uav_pos[0]:(uav_pos[0]+100), uav_pos[1]:(uav_pos[1]+100)], view_mask_rot *100, np.zeros_like(fire_map))

	view_mask_rot= np.where(frontier[uav_pos[0]:uav_pos[0]+100,uav_pos[1]:uav_pos[1]+100] > 0, frontier[uav_pos[0]:uav_pos[0]+100,uav_pos[1]:uav_pos[1]+100], view_mask_rot)
	
	frontier[uav_pos[0]:uav_pos[0]+100,uav_pos[1]:uav_pos[1]+100] = view_mask_rot
	
#	print view_mask_rot

	im.set_data(frontier)

	plt.pause(0.0001)

plt.show()   # Stop at end.

#anim = animation.FuncAnimation(fig, anim, interval=1)

