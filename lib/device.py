import base64

import cv2
# TODO: fix ipcam
import urllib3, base64
import numpy as np


class IpCamera(object):
    def __init__(self, url, user=None, password=None):
        self.url = url
        auth_encoded = base64.encodestring('%s:%s' % (user, password))[:-1]

        self.req = urllib3.Request(self.url)
        self.req.add_header('Authorization', 'Basic %s' % auth_encoded)

    def get_frame(self):
        response = urllib3.urlopen(self.req)
        img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, 1)
        return frame


class Camera(object):
    def __init__(self, camera=0, resolution=[1280, 720]):
        self.cam = cv2.VideoCapture(camera)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.valid = False
        try:
            resp = self.cam.read()
            self.shape = resp[1].shape
            self.valid = True
        except:
            self.shape = None

    def get_frame(self):
        if self.valid:
            _, frame = self.cam.read()
        else:
            frame = np.ones((480, 640, 3), dtype=np.uint8)
            col = (0, 256, 256)
            cv2.putText(frame, "(Error: Camera not accessible)", (65, 220), cv2.FONT_HERSHEY_PLAIN, 2, col)
        return frame

    def release(self):
        self.cam.release()
