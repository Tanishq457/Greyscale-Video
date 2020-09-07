import cv2 
import numpy as np
import sys, importlib, os, glob, shutil, sys

if __name__ == "__main__":
    try:
        spam_spec = importlib.util.find_spec("filetype")
        if spam_spec is None:
            raise(Exception)
        

    except:
        print('This program requires filetype package to run. Please install it through: \npip install filetype')
        exit()

import filetype

def createFrames(video):
    try:
        try:
            os.mkdir('temp')
        except:
            print('Error creating directory temp', file=sys.stderr)
            return 

        cap = cv2.VideoCapture(video)
        print('Filename: ' + video, file=sys.stderr)

        if not cap.isOpened():
            print(f'Error Opening File {video}', file=sys.stderr)
            return

        if not cap.isOpened():
            print(f'Error Opening File {video}', file=sys.stderr)
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
            print('Some Error Occured', file=sys.stderr)
            cap.release()
            shutil.rmtree('./temp')
            return

        cap.release()

        return fps, width, height
    except:
        print('An error', file=sys.stderr)
        try:
            shutil.rmtree('./temp')
        except:
            pass
        return


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
        print('Error removing temp files', file=sys.stderr)
    
    return name


if __name__ == "__main__":
        
    if(len(sys.argv) < 2):
        print(f'Insufficient Arguments - {len(sys.argv)} given, 2 required.\nExample: python convert.py filename')
        exit()
    video = sys.argv[1]

    if filetype.guess(video).mime.split('/')[0] != 'video':
        print('Given file is not a video file. Please give a video file.')
        exit()


    if('temp' in os.listdir()):
        print('Please rename the already present temp folder and then run again')
        exit()
    
    width, height, fps = createFrames(video)

    combineGreyFrames(video, width, height, fps)