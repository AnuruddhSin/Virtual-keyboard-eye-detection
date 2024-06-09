import cv2  # Importing OpenCV library for computer vision tasks
import mediapipe as mp  # Importing Mediapipe library for hand tracking
import time  # Importing time module for timing operations
import math  # Importing math module for mathematical operations

class HandDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        # Constructor to initialize parameters
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize mediapipe hands module
        self.mpHands = mp.solutions.hands
        # Initialize hands object with parameters
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC, self.detectionCon, self.trackCon)

        # Initialize mediapipe drawing utilities
        self.mpDraw = mp.solutions.drawing_utils

        # Function to detect hands in the image

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image to detect hands
        self.results = self.hands.process(imgRGB)

        # Draw landmarks if hands are detected
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    # Function to find position of landmarks in the hand
    def findPosition(self, img, draw=True):
        h, w, c = img.shape
        self.lmlist = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks
            for handlms in myHand:
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h
                for id, lm in enumerate(handlms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmlist.append([id, cx, cy])
                    # Bounding box calculations
                    if cx > x_max:
                        x_max = cx
                    if cx < x_min:
                        x_min = cx
                    if cy > y_max:
                        y_max = cy
                    if cy < y_min:
                        y_min = cy

                # Draw bounding box
                if draw:
                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        return self.lmlist

    # Function to find the distance between two landmarks
    def findDistance(self, p1, p2, img=None, draw=True):
        x1 = self.lmlist[p1][1]
        y1 = self.lmlist[p1][2]
        x2 = self.lmlist[p2][1]
        y2 = self.lmlist[p2][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)

        # Draw lines and circles if draw is True
        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return length, img, [x1, y1, x2, y2, cx, cy]

    # Function to find the angle between three points
    def findAngle(self, img, p1, p2, pp1, pp2, draw=True):
        pp1x = self.lmlist[pp1][1]
        pp1y = self.lmlist[pp1][2]
        pp2x = self.lmlist[pp2][1]
        pp2y = self.lmlist[pp2][2]

        c1, c2 = (pp1x + pp2x) // 2, (pp1y + pp2y) // 2

        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        x3, y3 = c1, c2

        angle = math.degrees(math.atan2(y2 - y3, x2 - x3) - math.atan2(y1 - y3, x1 - x3))
        if angle < 0:
            angle += 180

        # Draw lines and circles if draw is True
        if draw:
            cv2.line(img, (x1, y1), (x3, y3), (0, 255, 0), 3)
            cv2.line(img, (x2, y2), (x3, y3), (0, 255, 0), 3)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)

        return angle


# Function to run the main program
def main():
    pTime = 0
    cTime = 0
    # Open the webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Initialize HandDetector object
    detector = HandDetector()

    while True:
        # Capture frame from the webcam
        success, img = cap.read()
        # Flip the image horizontally
        img = cv2.flip(img, 1)
        # Find hands in the image
        img = detector.findHands(img)
        # Find positions of landmarks
        lmlist = detector.findPosition(img)
        lmlist1 = detector.lmlist

        # Find angle between two fingers
        if lmlist:
            ang = detector.findAngle(img, 8, 12, 5, 9, draw=True)
            print(ang)

        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Display FPS on the image
        cv2.putText(img, str(int(fps)), (18, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    3, (255, 0, 255), 3)

        # Display the image
        cv2.imshow("Image", img)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()