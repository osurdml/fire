"""
Written By: Ryan Skeele and Kyle Cesare
Oregon State University
Robotic Decision Making Laboratory

Wildfire UAV exploration/exploitation monitoring simulation
"""
#!/usr/bin/env python2

TIMESTEP = .05

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
from sklearn.cluster import KMeans

np.set_printoptions(threshold='nan')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

toa= gdal.Open('data/ash1_raster.toa')
fli= gdal.Open('data/ash1_raster.fli')
fli = fli.ReadAsArray()
toa= toa.ReadAsArray()

# Field of view for UAV is in the following configuration
view_mask = np.zeros((100, 100))
rr, cc = polygon(np.array([30, 30, 50]), np.array([40, 60, 50]))
view_mask[rr, cc] = 1

fire_map = np.zeros_like(fli)

im = ax.matshow(fire_map)
im.set_clim(0, 1000)

#Starting location of UAV in the Fire Map
uav_pos= (150,150)
view_mask_rot= view_mask 
perp_vec= [0,0] 
vec_to_nearest= [0,0]
uav_dist=[0]
yaw= [0]

# function for uav location and path planning 
def uav_pose(uav_dist, uav_pos, perp_vec, vec_to_nearest, yaw):
	if uav_dist >15:
		uav_pos=(int(uav_pos[0]+vec_to_nearest[0]*2), int(uav_pos[1]+vec_to_nearest[1]*2))
	elif uav_dist <11:
		uav_pos=(int(uav_pos[0]-vec_to_nearest[0]*2), int(uav_pos[1]-vec_to_nearest[1]*2))
	else:
		uav_pos= (int(uav_pos[0]+perp_vec[0]*2), int(uav_pos[1]+perp_vec[1]*2))
	starting_vec= [-1,0]
	yaw = math.atan2(vec_to_nearest[1], vec_to_nearest[0])- math.atan2(starting_vec[1], starting_vec[0])
	return uav_pos, yaw 


max_time = math.ceil(np.amax(toa))
#time_counter=0


for t in np.arange(0, max_time, TIMESTEP):
	for i in range(10):	
		# Find burning areas within the current time interval
		fire_map = np.logical_and(toa < t, toa > 0)
		fire_map = np.where(fire_map, fli, np.zeros_like(fli))
	
		# Extract the fire line
		frontier = fire_map > 0
		frontier = convolve2d(frontier, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], mode='same')
		frontier = np.logical_and(frontier < 8, frontier > 0)
		frontier = np.where(frontier == True, fire_map, np.zeros_like(fire_map))
		frontier_only= frontier	
		# Calculate distances to each point on the fireline
		(xs, ys) = np.nonzero(frontier)
		if xs.size > 0:
			dists = (xs - uav_pos[0]) ** 2 + (ys - uav_pos[1]) ** 2
			nearest = np.argmin(dists)
			uav_dist= np.sqrt((xs[nearest]-uav_pos[0])**2 + (ys[nearest]-uav_pos[1])**2)	
			"""
			# Store the nearest point on fireline 
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					frontier[xs[nearest] + dx, ys[nearest] + dy] = 5000
			"""
			# Find the perpendicular vector to the fireline
			vec_to_nearest = np.array([xs[nearest] - uav_pos[0], ys[nearest] - uav_pos[1]])
			vec_to_nearest = vec_to_nearest / np.linalg.norm(vec_to_nearest)
			perp_vec = np.empty_like(vec_to_nearest)
			perp_vec[0] = -vec_to_nearest[1]
			perp_vec[1] = vec_to_nearest[0]
	
			"""
			# Plot the perpendicular vector
			rr, cc = line(uav_pos[0], uav_pos[1],
				int(uav_pos[0] + perp_vec[0] * 10),
				int(uav_pos[1] + perp_vec[1] * 10))
			frontier[rr, cc] = 5000
			"""

		# Position the UAV
		uav_pos, yaw= uav_pose(uav_dist, uav_pos, perp_vec, vec_to_nearest, yaw)
		
		# Show the location of the UAV
		for lx in range(-1,2):
			for ly in range(-1,2):
				frontier[uav_pos[0]+lx, uav_pos[1]+ly] = 499
		for dx in [-2,-2,2,2]:
			for dy in [-2,-2,2,2]:
				frontier[uav_pos[0]+dx, uav_pos[1]+dy] = 499 

		#UAV FOV
		#print yaw
		#print math.degrees(yaw)
		view_mask_rot= rotate(view_mask, math.degrees(yaw))
		view_mask_rot= np.where(frontier[uav_pos[0]-50:uav_pos[0]+50,uav_pos[1]-50:uav_pos[1]+50] > 0, frontier[uav_pos[0]-50:uav_pos[0]+50,uav_pos[1]-50:uav_pos[1]+50], view_mask_rot*100)	
		frontier[uav_pos[0]-50:uav_pos[0]+50,uav_pos[1]-50:uav_pos[1]+50] = view_mask_rot 			

			
		#time_counter= time_counter +1
		hotspots = np.asarray(np.where(frontier_only > 200)).reshape((-1, 2))
		k = KMeans(n_clusters=2)
		kmeans_indices= k.fit(hotspots)
		centers = k.cluster_centers_

		print "Centers:", centers


		"""
		hotspots= np.logical_and(hotspots[uav_pos[0]-50:uav_pos[0]+50,uav_pos[1]-50:uav_pos[1]+50], view_mask_rot)
		untracked_hotspots = untracked_hotspots+hotspots 		
		print untracked_hotspots

#use k clustering to find hotspots, calculate their average x,y location and compare/match it with the closest location in the next iteration. To determine K value do a percentage of cells in cluster that are not hotspots if over percentage then increase the K value. Track the time untracked of each cluster. Implement algorithm; time untracked, distance to hotspot times some constant.
	"""	

		# im.set_data(hotspots)
	
		plt.pause(0.0001)

plt.show()   # Stop at end.

#anim = animation.FuncAnimation(fig, anim, interval=1)

