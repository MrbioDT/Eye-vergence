# a good ROI should be (19, 164) (388, 300)

import numpy as np
import cv2

def sort_contour_function(areas, contours, reverse=False):
    # this function sort each contour in terms of size from the biggest to smallest
    new_contours = list()
    index = list()
    n = len(areas)
    for i in range(n):
        index.append(areas.index(max(areas)))
        areas.remove(max(areas))
        new_contours.append(contours.pop(index[i]))
    return new_contours


def threshold_slider(slider_position):
    # read a new frame each time to avoid drawing overlap contours
    global threshold_value
    threshold_value = slider_position
    dt_video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,frame_number)
    dt_update_window()

def frame_slider(slider_position):
    # this function update the frame as the frame slider in trackbar change its location
    global frame_number
    frame_number = slider_position  # use this to connect two trackbar
    dt_video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,slider_position)

    dt_update_window()
#    print slider_position
#    print "this function is called, but I currently do not know how to use it"

def dt_update_window():
    # this function update the window with the current frame corresponding to the frame_number

    # read a new frame
    ret, frame = dt_video.read()
    if ROI:
        # frame = frame[25:166,409:312]
        frame = frame[ROI[0][1]:ROI[1][1], ROI[0][0]:ROI[1][0]] # set ideal ROI

    # find the contour
    ret, thresh = cv2.threshold(frame, threshold_value, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # I just move the sorting block here
    # sort the contours according to size and draw the first 3
    contour_area = [cv2.contourArea(c) for c in contours]
    sort_contours = sort_contour_function(contour_area, contours, reverse=False)
    new_contours = sort_contours[1:4]  # exclude the biggest contour of window(0)
    cv2.drawContours(frame, new_contours, -1, (255, 255, 255), 1)

    cv2.imshow(window, frame)

    global contours_list
    contours_list = new_contours




def haha(s):
    pass

#basic variables
ROI = [[19, 164], [388, 300]]
window = 'set_threshold'
dt_video = cv2.VideoCapture('example.avi')
dt_totalframe = int(dt_video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))  # total frame(float) in avi video, count
print dt_totalframe
frame_number = 0
threshold_value = 79 # initial set up
contours_list = list()

# read the first frame from here
ret,frame = dt_video.read()
frame = frame[ROI[0][1]:ROI[1][1],ROI[0][0]:ROI[1][0]]  #SET ideal ROI

# analysis the contour in the first frame
ret, thresh = cv2.threshold(frame, threshold_value, 255, 0) #initial
# The function applies fixed-level thresholding to a single-channel array. The function is typically used to get a bi-level (binary) image out of a grayscale image
# type 0 represents THRESH_BINARY means if pixel greater than threshold then it is maxvalue otherwise it is 0
# cv2.threshold(src, thresh, maxval, type[, dst])
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# sort the contours according to size and draw the first 3
# this is only for the 1st frame
contour_area = [cv2.contourArea(c) for c in contours]
sort_contours = sort_contour_function(contour_area,contours,reverse=False)
new_contours = sort_contours[1:4]  # exclude the biggest contour of window(0)
cv2.drawContours(frame,new_contours,-1,(255,255,255),1)

# Create the window and trackbar
cv2.namedWindow(window) #It is important to create the window first
cv2.createTrackbar('Frame',window,0,dt_totalframe,frame_slider)
cv2.createTrackbar('Threshold',window,69,255,threshold_slider)  #tag
# cv2.createTrackbar(trackbarName, windowName, value, count, onChange)

# Show the first frame
cv2.imshow(window, frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

print 'optimal threshold_value is ' + str(threshold_value)
#print ''
#print 'the contours_list is ' + str(contours_list)


'''
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

l_contours = contours[:3]
print len(l_contours)
cv2.drawContours(frame, l_contours, -1, (255,0,0), 1)
'''


#####CHECK_VERGENCE###MAJOR FUNCTION-3

def compute_centroid(cnt):
    #this function compute the centroid of given contour(cnt)
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    centroid = [cx, cy]
    return centroid # it is going to be a point stored in list

def compute_bodyaxis(mid,sb):
    # this function compute body axis as vector
    return [(mid[0]-sb[0]), (mid[1]-sb[1])]

# compute the centroid of each contours
centroid_list = [compute_centroid(cnt) for cnt in contours_list]

# assign the name to each centroid
sb_c = centroid_list[0]
l_c = centroid_list[1]
r_c = centroid_list[2]
mid_eye = [(l_c[0]+r_c[0])*0.5,(l_c[1]+r_c[1])*0.5]

# body axis
body_axis = compute_bodyaxis(mid_eye,sb_c)

