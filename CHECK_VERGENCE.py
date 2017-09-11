# a good ROI should be (19, 164) (388, 300)
# optimal threshold_value is 79

import cv2

def compute_centroid(cnt):
    #this function compute the centroid of given contour(cnt)
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    centroid = [cx, cy]
    return centroid # it is going to be a point stored in list