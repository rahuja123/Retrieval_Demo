import numpy as np
import cv2

img = cv2.imread('../assets/images/overview_B3_cluster_1.png')
overlay_t = cv2.imread('stickman.png',-1) # -1 loads with transparency



def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):

	cv2.imshow('image',overlay_t)
	cv2.waitKey(0)
	"""
	@brief      Overlays a transparant PNG onto another image using CV2

	@param      background_img    The background image
	@param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
	@param      x                 x location to place the top-left corner of our overlay
	@param      y                 y location to place the top-left corner of our overlay
	@param      overlay_size      The size to scale our overlay to (tuple), no scaling if None

	@return     Background image with overlay on top
	"""

	bg_img = background_img.copy()

	if overlay_size is not None:
		img_to_overlay_t = cv2.resize(overlay_t.copy(), overlay_size)

	# Extract the alpha mask of the RGBA image, convert to RGB
	b,g,r,a = cv2.split(img_to_overlay_t)
	overlay_color = cv2.merge((b,g,r))

	# Apply some simple filtering to remove edge noise
	# mask = cv2.medianBlur(a,1)

	h, w, _ = overlay_color.shape
	roi = bg_img[y:y+h, x:x+w]

	# Black-out the area behind the logo in our original ROI
	img1_bg = cv2.bitwise_and(roi.copy(),roi.copy())

	# Mask out the logo from the logo image.
	img2_fg = cv2.bitwise_and(overlay_color,overlay_color)

	# Update the original image with our new ROI
	bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

	return bg_img

cv2.imshow('image',overlay_transparent(img, overlay_t,194,42, (200,200)))
cv2.waitKey(0)
