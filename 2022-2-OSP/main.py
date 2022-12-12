import cv2
from math import e, pi, sin, cos
import numpy as np
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)

        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)

        cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:

            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)

            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True

        else:
            return False


# Buttons
buttonListValues = [['C', 'sin', 'cos', '/'],
                    ['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', 'e', 'pi', '=']]
                   #['%', 'CE', 'C', 'del'],

buttonList = []
for x in range(4):
   for y in range(5):
    xpos = x * 100 + 500
    ypos = y * 100 + 150
    buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Variables
myEquation = ''
delayCounter = 0

x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2) # y = Ax^2 + Bx + C

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # width
cap.set(4, 720) # height
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Draw All
    cv2.rectangle(img, (500, 50), (500 + 400, 50 + 100),
                  (225, 225, 225), cv2.FILLED)

    cv2.rectangle(img, (500, 50), (500 + 400, 50 + 100),
                  (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)

    # Check for Hand
    if hands:
        # Find distance between fingers
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[4], lmList[8], img)

        # print(length)
        x, y = lmList[8]
        '''
        # Fine distance to lmList[8]
        # lmList2 = hands[0]['lmList2']
        x, y, w, h = hands[0]['bbox']
        x1, y1 = lmList[5]
        x2, y2 = lmList[17]

        distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C
        '''
        # If clicked check which button and perform action

        if length < 50 and delayCounter == 0:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 5)][int(i / 5)]  # get correct number
                    if myValue == '=':
                        myEquation = str(eval(myEquation))

                    elif myValue == 'C':
                        myEquation *= 0

                    elif myValue == 'sin':
                        myEquation = str(eval(myEquation))
                        myEquation = round(sin(float(myEquation)), 6)
                        myEquation = str(myEquation)

                    elif myValue == 'cos':
                        myEquation = str(eval(myEquation))
                        myEquation = round(cos(float(myEquation)), 6)
                        myEquation = str(myEquation)

                    else:
                        myEquation += myValue
                    delayCounter = 1

    # to avoid multiple clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 20:
            delayCounter = 0

    # Write the Final answer
    cv2.putText(img, myEquation, (510, 130), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 0, 0), 3)
    #cv2.putText(img, f'{int(distanceCM)}cm', (x, y))

    # Display
    key = cv2.waitKey(1)
    cv2.imshow("Image", img)
    if key == ord('c'):
        myEquation = ''
