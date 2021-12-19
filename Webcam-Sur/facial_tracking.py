import cv2
import os
import time
from datetime import datetime
import mediapipe as mp
import sys
import psutil
import subprocess
from constants import PYTHONVERSION
from alert_email import AlertEmail
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

        self.initial_detection_time = -1
        self.start_recording_threshold = 2 # recording start x seconds after detection
        self.record_vid_name = ""

    
    def run_detection(self, frame) -> bool:
        mpDraw = mp.solutions.drawing_utils
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = self.face_cascade.detectMultiScale(gray, 1.15, 5)
        # hands = self.handObj.process(imageRGB)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        # if hands.multi_hand_landmarks != None:
        #     for handLandmarks in hands.multi_hand_landmarks: # handLandmarks is a single hand
        #         mpDraw.draw_landmarks(frame, handLandmarks, self.mpHand.HAND_CONNECTIONS)

        cv2.imshow("Camera", frame)

        if len(faces) > 0:
            return True
        return False


    def initialize_recording(self):
        current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        self.record_vid_name = f"recordings/{current_time}.mp4"
        output_vid = cv2.VideoWriter(self.record_vid_name, fourcc, 20.0, frame_size)

        self.vid_output = output_vid

    def stop_recording(self):
        self.vid_output.release()


    def check_disk_storage(self):
        fan = psutil.disk_usage(path=os.path.dirname(os.path.abspath(__file__)))

        if fan.percent > 95:
            print(time.time())
            print("Storage exceeded limit...")
            sys.exit(0)


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

            if human_detected and self.initial_detection_time == -1:
                self.initial_detection_time = time.time()

            if human_detected == False and time.time() - self.initial_detection_time >= 30:
                self.initial_detection_time = -1

            gate = time.time() - self.initial_detection_time >= self.start_recording_threshold

            if human_detected and gate:
                if recording == False:
                    # checks for the available storage
                    self.check_disk_storage()

                    # captures an image before the start of recording
                    s, img = self.cap.read()

                    # if s:
                    #     print("Image captured...")
                    #     cv2.namedWindow("cam-test", cv2.WINDOW_AUTOSIZE)
                    #     cv2.imshow("cam-test",img)
                    #     cv2.destroyWindow("cam-test")
                    #     cv2.imwrite("image-capture.jpg",img) 

                    # subprocess.Popen(f"py -{PYTHONVERSION} ./alert_email.py", shell = True)

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

                    self.generate_image()
                    print("Images have been successfully generated.")
                    subprocess.Popen(f"py -{PYTHONVERSION} ./alert_email.py {self.initial_detection_time - 2} {missing_start_time}", shell = True)

                    self.initial_detection_time = -1

                    print("Recording ended...")

                elif recording:
                    self.vid_output.write(frame)

            if cv2.waitKey(1) == ord('q'):
                print("Program Terminated...")
                self.cap.release()
                cv2.destroyAllWindows()


    def generate_image(self):
        cam = cv2.VideoCapture(os.path.join(os.path.abspath(os.path.dirname(__file__)), self.record_vid_name))

        count = 0
        currentframe = 0
        maxframe = 5
        multiplier = 2 # default frame skips between each image

        length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

        if length > 20:
            multiplier = int(length / 5)
            print(f"With video frames of {length}, the frame multiplier has been set to {multiplier}")

        while(True):
            ret, frame = cam.read()
            if ret and count % multiplier == 0:

                if int(currentframe / multiplier) >= maxframe:
                    break

                name = f'image-capture({int(currentframe / multiplier)}).jpg'
                cv2.imwrite(name, frame)
                currentframe += multiplier
                count += 1
            elif ret:
                count += 1
            else:
                break


        cam.release()
        cv2.destroyAllWindows()


    def run_program(self):
        ii = IntegrityIdentifier()
        ii.load_pid_to_file(os.path.basename(__file__), os.getpid())

        self.record()


if __name__ == "__main__":
    obj = Detection()
    obj.run_program()