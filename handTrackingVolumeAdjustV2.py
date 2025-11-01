import logging
import frameClient
# Use a module logger instead of importing from venv (that module doesn't export a logger)
logger = logging.getLogger(__name__)
# Configure basic logging so errors are visible when running as a script.
logging.basicConfig(level=logging.INFO)
import cv2
import overlay_colors as colors
import time
import handTrackingModule
import numpy as np
import math
import audio

### Uncomment to initialize video capture here
# camWidth, camHeight = 1280, 720
# capture = cv2.VideoCapture(0)
# capture.set(3, camWidth)
# capture.set(4, camHeight)

prevTime = 0
volumeBar = 400

lastFingerEventTime = time.time()

handDetector = handTrackingModule.HandDetector(min_detection_confidence=0.7, max_num_hands=1)

def boundingBoxArea(boundingBox) :
    return (boundingBox[2] - boundingBox[0]) * (boundingBox[3] - boundingBox[1])

def process_frame(img, draw=True):
    global prevTime, volumeBar, handDetector
    global lastFingerEventTime
    isAdjustingVolume = False

    handDetector.detectHands(img)
    landmarkList, handBoundingBox, palmBoundingBox = handDetector.findPositions(img, handNumber=0)

    if landmarkList:
        palmArea = boundingBoxArea(palmBoundingBox) // 100

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
            fingerStateCorrect = (fingersUpState[2] == 0 and fingersUpState[3] == 0 and fingersUpState[4] == 1)
            if fingerStateCorrect:
                currentTime = time.time()
                if (currentTime - lastFingerEventTime) > 0.2:
                    # set system volume (percent 0-100)
                    try:
                        isAdjustingVolume = True
                        audio.set_volume(volumePercentage)
                    except Exception:
                        # on failure, ignore so UI still runs
                        logger.debug("Failed to set volume", exc_info=True)
                        pass
                    lastFingerEventTime = currentTime
            else:
                isAdjustingVolume = False
            if draw:
                circleColor = colors.COLOR_GREEN if isAdjustingVolume else colors.COLOR_LINE
                cv2.circle(img, (midX, midY), 10, circleColor, cv2.FILLED)

    # Drawings
    if draw:
        # Finger distance bar
        dx, dy = -140, 75
        x_fill = 150 + (400 - int(volumeBar)) + dx
        x_fill = max(150 + dx, min(400 + dx, x_fill))
        barFillColor = colors.COLOR_GREEN if isAdjustingVolume else colors.COLOR_LINE
        cv2.rectangle(img, (150 + dx, 5 + dy), (x_fill, 20 + dy), barFillColor, cv2.FILLED)
        cv2.rectangle(img, (150 + dx, 5 + dy), (400 + dx, 20 + dy), colors.COLOR_LINE, 3)

        try:
            currentVolume = int(audio.get_volume())
        except Exception:
            currentVolume = 0

        adjustingAudioTextColor = colors.COLOR_GREEN if isAdjustingVolume else colors.COLOR_WHITE
        adjustingAudioText = f'Changing audio' if isAdjustingVolume else 'Not changing audio'
        cv2.putText(img, adjustingAudioText, (5, 70), cv2.FONT_HERSHEY_PLAIN, 1, adjustingAudioTextColor, 2)
        cv2.putText(img, f'AUDIO={currentVolume}%', (0, 45), cv2.FONT_HERSHEY_PLAIN, 2, colors.COLOR_GREEN, 2)

    # Frame rate
    currentTime = time.time()
    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime
    cv2.putText(img, f'{str(int(fps))}FPS', (5, 20), cv2.FONT_HERSHEY_PLAIN, 1, colors.COLOR_GREEN, 2)

    # Render
    cv2.imshow("Image (press q to exit)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise KeyboardInterrupt # Exits

if __name__ == "__main__":
    # Keep the behavior when executed as a script, but expose a callable main()
    def main(showOriginalFrame=False):
        """Run the V2 volume adjuster.

        Args:
            showOriginalFrame (bool): If True, the original shared frame window will be shown
                                     alongside the processed view. Defaults to False.
        """
        try:
            frameClient.main(callbackFunc=process_frame, showOriginalFrame=showOriginalFrame)
        except KeyboardInterrupt:
            print("Exited by user")

    # Execute when run as a script
    main(showOriginalFrame=False)

    ### Uncomment this to use local video capture (comment out the frameClient line)
    # while True:
    #     success, img = capture.read()
    #     process_frame(img)
