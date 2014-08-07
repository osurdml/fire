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
from skimage.draw import polygon, circle, line
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

uav_pos= (50,50)
view_mask_rot= view_mask 
hotspots = np.zeros(10)
 
def algorithm(uav_pos,view_mask_rot, hotspots):
	#hotspots= np.zeros_like(view_mask_rot)
	hotspots= np.append(np.argsort(-view_mask_rot)[:3], hotspots) #this returns indexs, need to fix
	hotspots= np.argsort(-hotspots)[:10]
	uav_pos= (uav_pos[0]+1, uav_pos[1]+1)
	view_mask_rot= rotate(view_mask,uav_pos[0]*5)
	return uav_pos, view_mask_rot, hotspots

max_time = math.ceil(np.amax(toa))

for t in np.arange(0, max_time, TIMESTEP):
	# Find burning areas within the current time interval
	fire_map = np.logical_and(toa < t, toa > 0)
	fire_map = np.where(fire_map, fli, np.zeros_like(fli))

	# Extract the fire line
	frontier = fire_map > 0
	frontier = convolve2d(frontier, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], mode='same')
	frontier = np.logical_and(frontier < 8, frontier > 0)
	frontier = np.where(frontier == True, fire_map, np.zeros_like(fire_map))

	# Position the UAV
	uav_pos, view_mask_rot, hotspots = algorithm(uav_pos, view_mask_rot, hotspots) #rotate(view_mask, t * 10) #this too
	view_mask_rot = view_mask_rot * 100

	(xs, ys) = np.nonzero(frontier)
	if xs.size > 0:
		# dists = np.sum((frontier_points - np.array([uav_pos[0], uav_pos[1]])) ** 2, axis=1)
		dists = (xs - uav_pos[0]) ** 2 + (ys - uav_pos[1]) ** 2
		nearest = np.argmin(dists)

		for dx in range(-1, 2):
			for dy in range(-1, 2):
				frontier[xs[nearest] + dx, ys[nearest] + dy] = 5000

		vec_to_nearest = np.array([xs[nearest] - uav_pos[0], ys[nearest] - uav_pos[1]])
		vec_to_nearest = vec_to_nearest / np.linalg.norm(vec_to_nearest)
		perp_vec = np.empty_like(vec_to_nearest)
		perp_vec[0] = -vec_to_nearest[1]
		perp_vec[1] = vec_to_nearest[0]

		rr, cc = line(uav_pos[0], uav_pos[1],
			int(uav_pos[0] + perp_vec[0] * 10),
			int(uav_pos[1] + perp_vec[1] * 10))
		frontier[rr, cc] = 5000

	frontier[uav_pos[0], uav_pos[1]] = 5000

	hotspots = np.where(frontier > 500)

	im.set_data(frontier)

	plt.pause(0.0001)

plt.show()   # Stop at end.

#anim = animation.FuncAnimation(fig, anim, interval=1)

