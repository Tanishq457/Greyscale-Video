import cv2 
import numpy as np
import sys, importlib, os, glob, shutil, filetype 


def createFrames(video):
    
    try:
        os.mkdir('temp')
    except:
        print('Error creating directory temp')
        return 

    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print(f'Error Opening File {video}')
        return

    if not cap.isOpened():
        print(f'Error Opening File {video}')
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    try:
        i=0
        while True:  
            ret, frame = cap.read()
            if(not ret):
                print('Can\'t capture frames/Video End')
                break
        
            i+=1
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('./temp/temp_frame_'+str(i) + '.jpg', grey)    
            
    except:
        print('Some Error Occured')
        cap.release()
        return

    cap.release()

    return fps, width, height


def combineGreyFrames(video, width, height, fps, ):

    images = [image for image in os.listdir('./temp')]
    images.sort()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    name = ''
    if(os.path.splitext(video)[1] == '' ):
        name = 'greyscale_' + video + '.mp4'
    else:
        name = 'greyscale_' + video
    greyVideo = cv2.VideoWriter(name, fourcc, fps, (width, height))
    images = glob.glob('./temp/*.jpg')

    images = [os.path.splitext(os.path.basename(images[i]))[0] for i in range(len(images))]
    images = sorted(images, key=lambda x: int(x[11:]))

    for filename in images:
        img = cv2.imread('./temp/' + filename + '.jpg')
        greyVideo.write(img)

    greyVideo.release()

    try:
        shutil.rmtree('./temp')
    except:
        print('Error removing temp files')
    
    return name
