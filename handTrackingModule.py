import cv2
import mediapipe
import time

class HandDetector():
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.static_image_mode,
                              max_num_hands=self.max_num_hands,
                              min_detection_confidence=self.min_detection_confidence,
                              min_tracking_confidence=self.min_tracking_confidence)
        self.mpDraw = mediapipe.solutions.drawing_utils

    def detectHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)

    def findPositions(self, img, handNumber=0, draw=True):
        landmarkList = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNumber]
            for index, landmark in enumerate(hand.landmark):
                imgHeight, imgWidth, imgChannels = img.shape
                imgX, imgY = int(landmark.x * imgWidth), int(landmark.y * imgHeight)
                landmarkList.append([index, imgX, imgY])
                if draw:
                    cv2.circle(img, (imgX, imgY), 5, (200, 0, 0), cv2.FILLED)

        return landmarkList

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