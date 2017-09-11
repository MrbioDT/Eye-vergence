from filepicker import *
from eye_tracker_helpers import *
import pandas as pd
import os
from matplotlib import pyplot as plt
import cv2

dt_lefttop_p = [0, 0]
dt_rightdown_p = [0, 0]
ROI = None

def dt_update_window(windowname,frame):
    cv2.imshow(windowname,frame)

def dt_slider_position(slider_position):
    # this function update the frame as the frame slider in trackbar change its location
    dt_object.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,slider_position)
    ret, frame = dt_object.read()
    if ROI:
        #frame = frame[25:166,409:312]
        frame = frame[ROI[0][1]:ROI[1][1],ROI[0][0]:ROI[1][0]]
    dt_update_window(dt_windowname,frame)
#    print slider_position
#    print "this function is called, but I currently do not know how to use it"

def dt_mouse_event(event,x,y,flags,param):   # tag.30.08.2017 how to draw the size-changable retangle?
    global dt_rightdown_p, dt_lefttop_p
    dt_color = (255,255,255)
    dt_thickness = 1
    dt_selection = False
    if event == cv2.EVENT_LBUTTONDOWN:
        dt_lefttop_p[0] = x
        dt_lefttop_p[1] = y
        print 'EVENT_LBUTTONDOWN'
    elif event == cv2.EVENT_LBUTTONUP:
        dt_rightdown_p[0],dt_rightdown_p[1] = x,y
        dt_selection = True
        print 'EVENT_LBUTTONUP'
    if dt_selection:
        print dt_selection
        print (dt_lefttop_p[0],dt_lefttop_p[1]),(dt_rightdown_p[0],dt_rightdown_p[1])
 #       cv2.rectangle(frame,(dt_lefttop_p[0],dt_lefttop_p[1]),(x,y),dt_color,dt_thickness)



if __name__ == "__main__":

    ### SELECT A FOLDER TO ANALYZE, FIND ALL AVI FILES IN THAT FOLDER ###  ###temp-omit
    folder = pickdir()
    filenames = os.listdir(folder)
    avis = [filename for filename in filenames if os.path.splitext(filename)[1] == '.avi']

    ### CREATE A FOLDER WHERE RESULTS WILL BE SAVED ###  ###temp-omit
    output_folder = os.path.join(folder, 'results')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ### PROMPTS FOR USING ROI, CHANGING DEFAULT THRESHOLD, CHECK TRACKING FOR EACH VIDEO, PLOTTING DATA ###  ###temp-omit
    use_roi = raw_input('draw ROI? y/n ')
    # set_threshold = raw_input('set new threshold? y/n ')
    set_threshold = 'y'
#    check_tracking = raw_input('check eye tracking for each video? y/n ')
#    plot_data = raw_input('plot each trial once analysed? y/n ')

    ### MAJOR FUNCTION-1 ROI SELECTION ###  ###rewrite  ###task, I still need to add the function to draw the size changable rectangle
    if use_roi == 'y':
    # here, it is default to set ROI

        dt_object = cv2.VideoCapture(os.path.join(folder, avis[0]))
        dt_windowname = 'ROI SELECTION'
        dt_trackbarname_frame = 'Frame'
        dt_position = 0  # initial position of trackbar, value
        dt_totalframe = int(dt_object.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))  # total frame(float) in avi video, count
        # could be packaged into video class as attribute


        cv2.namedWindow(dt_windowname)
        cv2.createTrackbar(dt_trackbarname_frame,dt_windowname,dt_position,dt_totalframe,dt_slider_position)
        # cv2.createTrackbar(trackbarName, windowName, value, count, onChange)
        cv2.setMouseCallback(dt_windowname,dt_mouse_event)


        ret,frame = dt_object.read()
        print frame
        print type(frame)
        print frame.shape


        cv2.imshow(dt_windowname,frame)
        cv2.waitKey(0)   # press any key would serve as exit
        ROI = [dt_lefttop_p,dt_rightdown_p] #ROI is stored in a list
        print 'the ROI set is ' + str(ROI)

        #remember the output should be two points left-top and right-down
        cv2.destroyAllWindows()

    ###MAJOR FUNCTION-2 SET THE THRESHOLD  ### rewriting
    ### this function is achieved in set_threshold