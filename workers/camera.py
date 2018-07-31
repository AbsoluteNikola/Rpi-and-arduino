import picamera
import os
import time
from datetime import datetime


class CameraServer:

    def __init__(self):
        self.camera = picamera.PiCamera()
        os.chdir('/home/pi/Rpi-and-arduino/data/camera/')

    def serve(self):
        x = False
        while True:
            start = time.time()
            self.camera.capture('1.jpg' if x else '2.jpg')
            if x:
                os.symlink('1.jpg', 'tmp')
            else:
                os.symlink('2.jpg', 'tmp')
            os.rename('tmp', 'state.jpg')
            print(time.time() - start)
            time.sleep(max(0.0, 1 - (time.time() - start)))
            x = not x


if __name__ == '__main__':
    camera = CameraServer()
    camera.serve()
