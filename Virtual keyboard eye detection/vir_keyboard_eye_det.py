import cv2
from time import sleep
from detecting_eye_blink_module import FaceMeshDetector
from tracking_hand_module import HandDetector
from pygame import mixer

mixer.init()
voice_click = mixer.Sound('sclick.mp3')

# Create a window to display the virtual keyboard
cv2.namedWindow("Virtual_keyboard", cv2.WINDOW_NORMAL)

# Capture video from the camera
cap = cv2.VideoCapture(0)

# Set the resolution of the captured video
cap.set(3, 1280)
cap.set(4, 720)

# Initialize hand and eye detectors
detector = HandDetector(detectionCon=0.8)
eye_detector = FaceMeshDetector(maxFaces=1)

# Define the layout of the virtual keyboard
Keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "_"],
        ]

# Initialize an empty string to store typed text
finalText = ""

# Define the Button class to represent each key on the virtual keyboard
class Button():
    def __init__(self, pos, text, size=None):
        if size is None:
            size = [80, 80]
        self.pos = pos
        self.size = size
        self.text = text

# Create button objects for each key in the keyboard layout
buttonList = []
for i in range(len(Keys)):
    for j, Key in enumerate(Keys[i]):
        buttonList.append(Button([100 * j + 150, 100 * i + 150], Key))

# Function to draw all buttons on the image
def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 15, y + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
    return img

# Main loop to capture video and detect hand gestures
while True:
    success, img = cap.read()

    # Flip the image horizontally for correct orientation
    img1 = cv2.flip(img, 1)
    img = cv2.flip(img, 1)

    # Detect faces and eye blinks in the image
    img, faces = eye_detector.findFaceMesh(img, False)
    if len(faces) != 0:
        blink, img1 = eye_detector.EyeBlinkDetector(img, faces, True)

    # Find hands in the image
    img = detector.findHands(img)

    # Get hand landmarks
    lmList = detector.findPosition(img)

    # Display eye blink status and eye regions
    if faces:
        colour = (0, 0, 200)
        if blink:
            colour = (0, 200, 0)
        cv2.putText(img, f'Blinked :{blink}', (535, 140), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2, color=colour, thickness=2)
        # for left eye
        eye_roi_l = img1[faces[0][159][1] - 10:faces[0][145][1] + 10, faces[0][33][0] - 10:faces[0][133][0] + 10]
        w_x = faces[0][133][0] - faces[0][33][0]
        w_y = faces[0][145][1] - faces[0][159][1]
        # img[0:20 + w_y, 0:20 + w_x] = eye_roi_l
        img[110:110 + 20 + w_y, 450:450+20 + w_x] = eye_roi_l

        cv2.rectangle(img, (450, 110), (470 + w_x, 130 + w_y), colour, 2)

        # for right eye
        eye_roi_r = img1[faces[0][386][1] - 10:faces[0][374][1] + 10, faces[0][362][0] - 10:faces[0][263][0] + 10]
        w_x = faces[0][263][0] - faces[0][362][0]
        w_y = faces[0][374][1] - faces[0][386][1]
        # print(w_y, w_x)
        img[110:110 + 20 + w_y, 760:760 + 20 + w_x] = eye_roi_r
        cv2.rectangle(img, (760, 110), (780 + w_x, 130 + w_y), colour, 2)

    # Check for hand gestures and type corresponding keys
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                if blink:
                    voice_click.play()
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 15, y + 55),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
                    finalText += button.text
                    # Backspace button functionality
                elif button.text == "Backspace":
                    if len(finalText) > 0:
                        voice_click.play()
                        finalText = finalText[:-1]

    # Display the typed text
    cv2.rectangle(img, (200, 500), (1100, 580), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, finalText, (220, 550),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

    # Draw all buttons on the image
    img = drawALL(img, buttonList)

    # Add a slight delay for typing sensitivity control
    sleep(0.1)

    # Display the virtual keyboard image
    cv2.imshow("Virtual_keyboard", img)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()
