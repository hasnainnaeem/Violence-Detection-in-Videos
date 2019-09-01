
import cv2
import os
import sys
import numpy as np
import time
from src.ViolenceDetector import *
import settings.DeployLiveSettings as deploySettings
import settings.DataSettings as dataSettings
import src.data.ImageUtils as ImageUtils


def PrintHelp():
    print("Usage:")
    print("\t $(ThisScript)  $(PATH_FILE_NAME_OF_SOURCE_VIDEO)")
    print()
    print("or, specified $(PATH_FILE_NAME_TO_SAVE_RESULT) to save detection result:")
    print("\t $(ThisScript)  $(PATH_FILE_NAME_OF_SOURCE_VIDEO)  $(PATH_FILE_NAME_TO_SAVE_RESULT)")
    print()


class VideoSavor:
    def AppendFrame(self, image_):
        self.outputStream.write(image_)

    def __init__(self, targetFileName, videoCapture):
        width = int(deploySettings.DISPLAY_IMAGE_SIZE)
        height = int(deploySettings.DISPLAY_IMAGE_SIZE)
        frameRate = int(videoCapture.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        self.outputStream = cv2.VideoWriter(targetFileName + ".avi", codec, frameRate, (width, height))


def PrintUnsmoothedResults(unsmoothedResults_):
    print("Unsmoothed results:")
    print("\t [ ")
    print("\t   ", end='')
    for i, eachResult in enumerate(unsmoothedResults_):
        if i % 10 == 9:
            print(str(eachResult) + ", ")
            print("\t   ", end='')

        else:
            print(str(eachResult) + ", ", end='')

    print("\n\t ]")


""" 
                    The Game is ON!
"""

# We create a VideoCapture object to read from the camera (pass 0):



def DetectViolence(PATH_FILE_NAME_TO_SAVE_RESULT):
    # font for text used on video frames
    font = cv2.FONT_HERSHEY_SIMPLEX

    violenceDetector = ViolenceDetector()
    capture = cv2.VideoCapture(0)
    shouldSaveResult = (PATH_FILE_NAME_TO_SAVE_RESULT != None)

    if shouldSaveResult:
        videoSavor = VideoSavor(PATH_FILE_NAME_TO_SAVE_RESULT + "_Result", capture)

    listOfForwardTime = []

    # Get some properties of VideoCapture (frame width, frame height and frames per second (fps)):
    frame_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv2.CAP_PROP_FPS)

    # Print these values:
    print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(frame_width))
    print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(frame_height))
    print("CAP_PROP_FPS : '{}'".format(fps))

    # Check if camera opened successfully
    if capture.isOpened() is False:
        print("Error opening the camera")

    flag = False
    # Read until video is completed
    while capture.isOpened():
        # Capture frame-by-frame from the camera
        ret, frame = capture.read()

        if ret is True:
            # Display the captured frame:
            # cv2.imshow('Input frame from the camera', frame)
            netInput = ImageUtils.ConvertImageFrom_CV_to_NetInput(frame)

            startDetectTime = time.time()
            isFighting = violenceDetector.Detect(netInput)
            endDetectTime = time.time()
            listOfForwardTime.append(endDetectTime - startDetectTime)

            targetSize = deploySettings.DISPLAY_IMAGE_SIZE - 2 * deploySettings.BORDER_SIZE
            currentImage = cv2.resize(frame, (targetSize, targetSize))
            if isFighting:
                resultImage = cv2.copyMakeBorder(frame,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 cv2.BORDER_CONSTANT,
                                                 value=deploySettings.FIGHT_BORDER_COLOR)

            else:
                resultImage = cv2.copyMakeBorder(frame,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 cv2.BORDER_CONSTANT,
                                                 value=deploySettings.NO_FIGHT_BORDER_COLOR)
            # frameText = "Violence Detected!" if isFighting else "No Violence Detected."
            # textColor = deploySettings.FIGHT_BORDER_COLOR if isFighting else deploySettings.NO_FIGHT_BORDER_COLOR
            # cv2.putText(frame, frameText, (50, 50), font, 4, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Violence Detection", resultImage)
            if shouldSaveResult:
                videoSavor.AppendFrame(resultImage)

            userResponse = cv2.waitKey(1)
            if userResponse == ord('q'):
                capture.release()
                cv2.destroyAllWindows()
                flag = True
                break
            else:
                isCurrentFrameValid, currentImage = capture.read()
        print("Details about current frame:")
        PrintUnsmoothedResults(violenceDetector.unsmoothedResults)
        averagedForwardTime = np.mean(listOfForwardTime)
        # print("Averaged Forward Time: ", averagedForwardTime)

        if flag:
            break
    # print("Details about current frame:")
    # PrintUnsmoothedResults(violenceDetector.unsmoothedResults)
    # averagedForwardTime = np.mean(listOfForwardTime)
    # print("Averaged Forward Time: ", averagedForwardTime)


if __name__ == '__main__':
    print("\n\n\n")
    try:
        PATH_FILE_NAME_TO_SAVE_RESULT = sys.argv[1]+"\\"
    except:
        PATH_FILE_NAME_TO_SAVE_RESULT = ".\\results\\DeployResults\\"
    DetectViolence(PATH_FILE_NAME_TO_SAVE_RESULT)

