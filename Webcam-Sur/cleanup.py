'''
File designed to clean up recorded data
'''

import os
import glob
from pathlib import Path

class CleanUp:
    def __init__(self):
        self.recording_folder = "recordings/*mp4"
        self.image_capture = "image-capture.jpg"

    def cleanup(self):
        files = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.recording_folder), recursive=True)
        
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

        try:
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.image_capture))
        except OSError as e:
            print("Error: Image not found.")

      

if __name__ == "__main__":
    c = CleanUp()
    c.cleanup()