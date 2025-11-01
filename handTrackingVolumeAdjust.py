import cv2
import time
import handTrackingModule
import numpy as np
import math
import overlay_colors as colors
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def main():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    volumeRange = volume.GetVolumeRange()
    minVolume, maxVolume = volumeRange[0:2]

    camWidth, camHeight = 1280, 720
    capture = cv2.VideoCapture(0)
    capture.set(3, camWidth)
    capture.set(4, camHeight)

    prevTime = 0
    volumeBar = 400

    handDetector = handTrackingModule.HandDetector(min_detection_confidence=0.7)

    while True:
        success, img = capture.read()

        handDetector.detectHands(img)
        landmarkList = handDetector.findPositions(img, handNumber=0)

        if landmarkList:
            x1, y1 = landmarkList[4][1::]
            x2, y2 = landmarkList[8][1::]
            midX, midY = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x2 - x1, y2 - y1)

            cv2.putText(img, f'x1={x1}, y1={y1}', (60, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, colors.COLOR_POINT_A, 1)
            cv2.circle(img, (x1, y1), 10, colors.COLOR_POINT_A, cv2.FILLED)
            cv2.putText(img, f'x2={x2}, y2={y2}', (60, 60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, colors.COLOR_POINT_B, 1)
            cv2.circle(img, (x2, y2), 10, colors.COLOR_POINT_B, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), colors.COLOR_LINE, 3)

            if length < 50:
                cv2.circle(img, (midX, midY), 10, colors.COLOR_LINE, cv2.FILLED)

            # print(length)

            # Length range: 50-300, volume range: -65 - 0
            newVolume = np.interp(length, [50, 300], [minVolume, maxVolume])
            volumeBar = np.interp(length, [50, 300], [400, 150])
            print(f'length({length}), newVolume({newVolume})')
            volume.SetMasterVolumeLevel(newVolume, None)

        cv2.rectangle(img, (50, 150), (85, 400), colors.COLOR_BLUE, 3)
        cv2.rectangle(img, (50, int(volumeBar)), (85, 400), colors.COLOR_BLUE, cv2.FILLED)

        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        prevTime = currentTime

        cv2.putText(img, str(int(fps)), (5, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, colors.COLOR_GREEN, 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()