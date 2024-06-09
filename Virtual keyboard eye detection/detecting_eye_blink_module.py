import cv2
import mediapipe as mp
import math
import time

# To play sound
from pygame import mixer

mixer.init()
voice_click = mixer.Sound('click.mp3')  #


class FaceMeshDetector():
    # Initializing the FaceMeshDetector class with various parameters
    def __init__(self, staticMode=False, maxFaces=2, refinelandmarks=True, minDetectionCon=0.5, minTrackCon=0.5):
        # Setting up parameters
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.refinelandmarks = refinelandmarks
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        # Setting up mediapipe modules for face mesh detection
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces, self.refinelandmarks,
                                                 self.minDetectionCon, self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)

    # Function to find face mesh in an image
    def findFaceMesh(self, img, draw=True):
        # Converting the image to RGB format
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Processing the image to find face mesh
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        # Checking if face mesh is detected
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                # Drawing landmarks on the image if required
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                               self.drawSpec, self.drawSpec)
                # Extracting landmark coordinates for each face
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    face.append([x, y])
                faces.append(face)
        return img, faces

    # Function to find the distance between two points
    def findDistance(self, p1, p2, img=None):
        # Calculating the distance between two points
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, info, img
        else:
            return length, info

    # Function to detect eye blinks
    def EyeBlinkDetector(self, img, faces, draw=True):
        # Define left and right eye landmarks
        idList_l = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        idList_r = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

        # Initialize variables for left and right eyes
        color = (255, 0, 255)
        if faces:
            face = faces[0]
            for id in idList_l:
                if draw:
                    cv2.circle(img, face[id], 1, color, cv2.FILLED)
            for id in idList_r:
                if draw:
                    cv2.circle(img, face[id], 1, color, cv2.FILLED)

        # Calculate parameters for left eye
        leftUp, leftDown = face[159], face[145]
        leftLeft, leftRight = face[133], face[33]
        len_Ver_l, _ = FaceMeshDetector.findDistance(self, leftUp, leftDown)
        len_Hor_l, _ = FaceMeshDetector.findDistance(self, leftLeft, leftRight)

        # Calculate parameters for right eye
        rightUp, rightDown = face[386], face[374]
        rightLeft, rightRight = face[263], face[362]
        len_Ver_r, _ = FaceMeshDetector.findDistance(self, rightUp, rightDown)
        len_Hor_r, _ = FaceMeshDetector.findDistance(self, rightLeft, rightRight)

        # Calculate aspect ratio for both eyes
        ratio_l = int((len_Ver_l / len_Hor_l) * 100)
        ratio_r = int((len_Ver_r / len_Hor_r) * 100)

        # Determine if the eyes are blinked
        if ratio_r < 23 and ratio_l < 23:
            blinked = True
            color = (0, 200, 0)
        else:
            blinked = False

        return blinked, img


def main():
    # Open the default camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 1080)  # Set the width of the frames
    cap.set(4, 720)  # Set the height of the frames
    pTime = 0
    detector = FaceMeshDetector(maxFaces=1)  # Initialize FaceMeshDetector
    while True:
        success, img = cap.read()  # Read frames from the camera

        # Detect face mesh
        img, faces = detector.findFaceMesh(img, False)

        # Detect eye blinks if a face is detected
        if len(faces) != 0:
            blink = detector.EyeBlinkDetector(img, faces, True)

        # Display FPS and image
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 200), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 3)
        cv2.namedWindow("EBD", cv2.WINDOW_NORMAL)
        cv2.imshow("EBD", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
