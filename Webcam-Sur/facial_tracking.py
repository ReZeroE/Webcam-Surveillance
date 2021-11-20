import cv2
import os
import time
from datetime import datetime
import mediapipe as mp
import sys
import subprocess

from integrity_identifier import IntegrityIdentifier

class Detection:
    def __init__(self):
        self.vid_output = None
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.mpHand = mp.solutions.hands
        self.handObj = self.mpHand.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.6)

    
    def run_detection(self, frame) -> bool:
        mpDraw = mp.solutions.drawing_utils
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = self.face_cascade.detectMultiScale(gray, 1.15, 5)
        hands = self.handObj.process(imageRGB)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        if hands.multi_hand_landmarks != None:
            for handLandmarks in hands.multi_hand_landmarks: # handLandmarks is a single hand
                mpDraw.draw_landmarks(frame, handLandmarks, self.mpHand.HAND_CONNECTIONS)

        cv2.imshow("Camera", frame)

        if len(faces) > 0:
            return True
        return False


    def initialize_recording(self):
        current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_vid = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20.0, frame_size)

        self.vid_output = output_vid

    def stop_recording(self):
        self.vid_output.release()


    def record(self):
        human_detected = False
        recording = False
        buffer_time = 10

        missing_start = True
        missing_start_time = -1

        alert_sent = False

        while True:
            switch, frame = self.cap.read()
            human_detected = self.run_detection(frame)

            if human_detected:
                if recording == False:
                    print("Start recording...")
                    self.initialize_recording()
                    recording = True
                
                missing_start = True
                self.vid_output.write(frame)

            if human_detected == False:
                if recording and missing_start:
                    print("Person missing detected...")
                    missing_start_time = time.time()
                    missing_start = False

                curr_time = time.time()
                if recording and curr_time - missing_start_time > buffer_time:
                    self.stop_recording()
                    recording = False
                    missing_start = True
                    print("Recording ended...")
                elif recording:
                    self.vid_output.write(frame)

            if cv2.waitKey(1) == ord('q'):
                print("Program Terminated...")
                self.cap.release()
                cv2.destroyAllWindows()


    def run_program(self):
        ii = IntegrityIdentifier()
        ii.load_pid_to_file(os.path.basename(__file__), os.getpid())

        self.record()


if __name__ == "__main__":
    obj = Detection()
    obj.record()