import frameClient
import cv2
import time
import handTrackingModule
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volumeInterface = interface.QueryInterface(IAudioEndpointVolume)

volumeRange = volumeInterface.GetVolumeRange()
minVolume, maxVolume = volumeRange[0:2]

### Uncomment to initialize video capture here
# camWidth, camHeight = 1280, 720
# capture = cv2.VideoCapture(0)
# capture.set(3, camWidth)
# capture.set(4, camHeight)

prevTime = 0
volumeBar = 400

handDetector = handTrackingModule.HandDetector(min_detection_confidence=0.7, max_num_hands=1)

def boundingBoxArea(boundingBox) :
    return (boundingBox[2] - boundingBox[0]) * (boundingBox[3] - boundingBox[1])

def process_frame(img, draw=True):
    global prevTime, volumeBar, handDetector, minVolume, maxVolume, volumeInterface

    handDetector.detectHands(img)
    landmarkList, handBoundingBox, palmBoundingBox = handDetector.findPositions(img, handNumber=0)

    if landmarkList:
        # Filter based on palmArea
        palmArea = boundingBoxArea(palmBoundingBox) // 100
        cv2.putText(img, f'palmArea({palmArea})', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)

        if 20 < palmArea < 1000:
            # Find distance
            length, info = handDetector.findDistance(4, 8, img, draw=True)
            midX, midY = info[4:6]

            # Convert volume
            lengthMultiplier = np.interp(palmArea, [20, 1000], [3, 0.5])
            length = length * lengthMultiplier
            volumePercentage = np.interp(length, [50, 300], [0, 100])
            volumeBar = np.interp(volumePercentage, [0, 100], [400, 150])

            # Reduce volume step resolution to make it smoother
            smoothness = 5
            volumePercentage = smoothness * round(volumePercentage / smoothness)

            # Enable volume setting based on fingers up
            fingersUpState = handDetector.fingersUp()
            if fingersUpState[2] == 0 and fingersUpState[3] == 0 and fingersUpState[4] == 1:
                volumeInterface.SetMasterVolumeLevelScalar(volumePercentage / 100, None)
                if draw:
                    cv2.circle(img, (midX, midY), 10, (0, 255, 0), cv2.FILLED)

    # Drawings
    if draw:
        # cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        # cv2.rectangle(img, (50, int(volumeBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.rectangle(img, (5, 150), (20, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (5, int(volumeBar)), (20, 400), (255, 0, 0), cv2.FILLED)
        currentVolume = int(volumeInterface.GetMasterVolumeLevelScalar() * 100)
        cv2.putText(img, f'Volume({currentVolume}%)', (80, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Frame rate
    currentTime = time.time()
    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime
    cv2.putText(img, str(int(fps)), (5, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2)

    # Render
    cv2.imshow("Image (press q to exit)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise KeyboardInterrupt # Exits

if __name__ == "__main__":
    frameClient.main(callbackFunc=process_frame, showOriginalFrame=False)

    ### Uncomment this to use local video capture (comment out the frameClient line)
    # while True:
    #     success, img = capture.read()
    #     process_frame(img)
