import cv2
from cvzone.HandTrackingModule import HandDetector

# Cam
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands= 1)

# Loop
while (1):
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # detection
    hands, img = detector.findHands(img, flipType=False)

    # display
    cv2.imshow("Image", img)
    cv2.waitKey(1)