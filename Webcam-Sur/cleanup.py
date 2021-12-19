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


        img_filename0 = 'image-capture(0).jpg'
        img_filename1 = 'image-capture(1).jpg'
        img_filename2 = 'image-capture(2).jpg'
        img_filename3 = 'image-capture(3).jpg'
        img_filename4 = 'image-capture(4).jpg'
        try:
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_filename0))
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_filename1))
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_filename2))
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_filename3))
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_filename4))
        except OSError as e:
            print("Error: Image not found.")

      

if __name__ == "__main__":
    c = CleanUp()
    c.cleanup()