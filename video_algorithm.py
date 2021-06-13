import os
import cv2
import numpy as np
import time
import peakutils
from utils import  prepare_dirs
from meanColor import isSimilar
def keyFrames_meanColor(videoPath):
    keyFramesList=keyframeDetection(videoPath, 'none', 0.1 ,1, False)
    meanColorsList=[]
    for i in keyFramesList:
        average = i.mean(axis=0).mean(axis=0)
        average = np.array([average[2], average[1], average[0]])
        avg_patch = np.ones(shape=i.shape, dtype=np.uint8) * np.uint8(average)
        meanColorsList.append(list(avg_patch[0][0]))
    return meanColorsList
def is_videos_similar(meanColorsList_query,meanColorsList_db):
    print(meanColorsList_query)
    print(meanColorsList_db)
    similar_frames=0
    for i in range(len(meanColorsList_query)):
        if isSimilar(meanColorsList_query[i],meanColorsList_db[i]):
            similar_frames+=1
    if (similar_frames/len(meanColorsList_query))>0.9:
        return True
    else:
        return False




def keyframeDetection(source, dest, Thres , minKeyFrameTimeinSec = 1, logs=False):
    
    keyframePath = dest+'/keyFrames'
    prepare_dirs(keyframePath)

    cap = cv2.VideoCapture(source)
    numberOfFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
  
    if (cap.isOpened()== False):
        print("Error opening video file")

    keyFrames = []
    lstdiffMag = []
    timeSpans = []
    videoFrames = []
    lastFrame = None
    Start_time = time.process_time()
    # Read until video is completed

    for i in range(0,numberOfFrames,(fps*minKeyFrameTimeinSec)):
        cap.set(1, i)
        ret, frame = cap.read()

        frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
        


        videoFrames.append(frame)
        if frame_number == 0:
            lastFrame = frame


        diff = cv2.absdiff(frame, lastFrame)
        diffMag = np.count_nonzero(diff)
        lstdiffMag.append(diffMag)
        stop_time = time.process_time()
        time_Span = stop_time-Start_time
        timeSpans.append(time_Span)
        lastFrame = frame

    cap.release()
    y = np.array(lstdiffMag)
    base = peakutils.baseline(y, 8)
    #get indicies of the frames with higher diffrence than threshold
    indices = peakutils.indexes(y-base, Thres, min_dist=1)
    
    cnt = 1
    for frame_num in indices:
        #cv2.imwrite(os.path.join(keyframePath , 'keyframe'+ str(cnt) +'.jpg'), videoFrames[frame_num])
        keyFrames.append(videoFrames[frame_num])
        cnt +=1
        if(logs):
            log_message = 'keyframe ' + str(cnt) + ' happened at ' + str(timeSpans[frame_num]) + ' sec.'
            print(logs)
            print('frame Number: ' +frame_num)

    return keyFrames
