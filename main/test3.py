from djitellopy import Tello
import cv2
import time
tello =Tello()
tello.connect()
#tello.takeoff()
tello.streamon()
count = 0
vidcap = cv2.VideoCapture(tello.get_udp_video_address())
success,image = vidcap.read()
success = True

vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))

success,image = vidcap.read()

print ('Read a new frame: ', success)
cv2.imwrite("./img/frame%d.jpg" % count, image)

tello.streamoff()

