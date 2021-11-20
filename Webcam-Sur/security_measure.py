import keyboard
from pynput.mouse import Controller
from time import sleep
import threading

class security_measure:
    def __init__(self):
        self.SECURITYTIMER = 5  # 21600 (6hr)


    def activate_security_measure(self):
        self.blockinput()
        sleep(self.SECURITYTIMER)
        self.unblockinput()

    def blockinput(self):
        global block_input_flag
        block_input_flag = 1
        t1 = threading.Thread(target=self.blockinput_start)
        t1.start()
        print("Security measure activated...")
        

    def unblockinput(self):
        self.blockinput_stop()
        print("Security measure deactivated...")
        

    def blockinput_start(self):
        mouse = Controller()
        global block_input_flag
        for i in range(150):
            keyboard.block_key(i)
        while block_input_flag == 1:
            mouse.position = (0, 0)

    def blockinput_stop(self):
        global block_input_flag
        for i in range(150):
            keyboard.unblock_key(i)
        block_input_flag = 0


if __name__ == "__main__":
    s = security_measure()
    s.blockinput()
    print("now blocking")
    sleep(5)
    s.unblockinput()
    print("now unblocking")