import cv2
import mediapipe
import time
import overlay_colors as colors

capture = cv2.VideoCapture(0)

mpHands = mediapipe.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

mpDraw = mediapipe.solutions.drawing_utils

currentTime = 0
prevTime = 0

while True:
    success, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for index, landmark in enumerate(handLandmarks.landmark):
                imgHeight, imgWidth, imgChannels = img.shape
                imgX, imgY = int(landmark.x * imgWidth), int(landmark.y * imgHeight)
                if index == 8:
                    cv2.circle(img, (imgX, imgY), 25, colors.COLOR_FINGERTIP, cv2.FILLED)

            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    currentTime = time.time()
    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (5, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, colors.COLOR_GREEN, 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)