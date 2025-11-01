import cv2
import mediapipe
import time
import overlay_colors as colors

camWidth, camHeight = 1280, 720
capture = cv2.VideoCapture(0)
capture.set(3, camWidth)
capture.set(4, camHeight)

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
        hand = 0
        for handLandmarks in results.multi_hand_landmarks:
            for index, landmark in enumerate(handLandmarks.landmark):
                imgHeight, imgWidth, imgChannels = img.shape
                imgX, imgY = int(landmark.x * imgWidth), int(landmark.y * imgHeight)
                # if index == 8:
                #     cv2.circle(img, (imgX, imgY), 25, colors.COLOR_FINGERTIP, cv2.FILLED)
                if index == 0:
                    landmark_formatted = "({:.5e}, {:.5e}, {:.5e})".format(landmark.x, landmark.y, landmark.z)
                    if hand == 0:
                        color = colors.COLOR_POINT_B
                        cv2.circle(img, (imgX, imgY), 10, color, cv2.FILLED)
                        cv2.putText(img, landmark_formatted, (60, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, color, 1)
                    elif hand == 1:
                        color = colors.COLOR_POINT_A
                        cv2.circle(img, (imgX, imgY), 10, color, cv2.FILLED)
                        cv2.putText(img, landmark_formatted, (60, 60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, color, 1)

            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)
            hand = hand + 1

    currentTime = time.time()
    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (5, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, colors.COLOR_GREEN, 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)