import math

import cv2
import mediapipe
import time

class HandDetector():
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.landmarkList = []

        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.static_image_mode,
                              max_num_hands=self.max_num_hands,
                              min_detection_confidence=self.min_detection_confidence,
                              min_tracking_confidence=self.min_tracking_confidence)
        self.mpDraw = mediapipe.solutions.drawing_utils
        self.tipIndexes = [4, 8, 12, 16, 20]

    def detectHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)

    def findPositions(self, img, handNumber=0, draw=True):
        self.landmarkList = []
        xHandList, yHandList = [], []
        xPalmList, yPalmList = [], []
        handBoundingBox = ()
        palmBoundingBox = ()

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNumber]
            for index, landmark in enumerate(hand.landmark):
                imgHeight, imgWidth, imgChannels = img.shape
                imgX, imgY = int(landmark.x * imgWidth), int(landmark.y * imgHeight)
                xHandList.append(imgX)
                yHandList.append(imgY)
                self.landmarkList.append([index, imgX, imgY])
                if index in [0, 5, 9, 13, 17]:
                    xPalmList.append(imgX)
                    yPalmList.append(imgY)

                if draw:
                    cv2.circle(img, (imgX, imgY), 5, (200, 0, 0), cv2.FILLED)

            handBoundingBox = min(xHandList), min(yHandList), max(xHandList), max(yHandList)
            palmBoundingBox = min(xPalmList), min(yPalmList), max(xPalmList), max(yPalmList)

        if draw:
            if handBoundingBox:
                cv2.rectangle(img, (handBoundingBox[0], handBoundingBox[1]), (handBoundingBox[2], handBoundingBox[3]),
                              (255, 50, 0), 2)
            if palmBoundingBox:
                cv2.rectangle(img, (palmBoundingBox[0], palmBoundingBox[1]), (palmBoundingBox[2], palmBoundingBox[3]),
                             (150, 50, 0), 2)

        return self.landmarkList, handBoundingBox, palmBoundingBox

    def fingersUp(self):
        fingers = []

        # Thumb
        if self.landmarkList[self.tipIndexes[0]][1] > self.landmarkList[self.tipIndexes[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Other fingers
        for index in range(1, 5):
            if self.landmarkList[self.tipIndexes[index]][2] < self.landmarkList[self.tipIndexes[index] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, landmark1Id, landmark2Id, img, draw=True):
        x1, y1 = self.landmarkList[landmark1Id][1::]
        x2, y2 = self.landmarkList[landmark2Id][1::]
        midX, midY = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)

        if draw:
            # cv2.putText(img, f'x1={x1}, y1={y1}', (60, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (55, 66, 200), 1)
            cv2.circle(img, (x1, y1), 10, (55, 66, 200), cv2.FILLED)
            # cv2.putText(img, f'x2={x2}, y2={y2}', (60, 60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (177, 235, 220), 1)
            cv2.circle(img, (x2, y2), 10, (177, 235, 220), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (midX, midY), 10, (255, 0, 255), cv2.FILLED)

        return length, [x1, y1, x2, y2, midX, midY]
def main():
    capture = cv2.VideoCapture(0)

    currentTime = 0
    prevTime = 0

    handDetector = HandDetector()

    while True:
        success, img = capture.read()

        handDetector.detectHands(img)
        landmarkList = handDetector.findPositions(img)

        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        prevTime = currentTime

        cv2.putText(img, str(int(fps)), (5, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()