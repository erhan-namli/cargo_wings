import cv2
from pyzbar.pyzbar import decode
from djitellopy import Tello

tello = Tello()
tello.connect()
tello.streamon()

# Adjust this value as needed
num_frames = 1  # Number of frames to capture

# Open the video stream
vidcap = cv2.VideoCapture(tello.get_udp_video_address())

# Loop through frames
for count in range(num_frames):
    success, frame = vidcap.read()  # Read frame from Tello stream
    if success:
        # Decode QR codes
        decoded_objects = decode(frame)

        if decoded_objects:
            # QR codes found, print their data
            for obj in decoded_objects:
                print("Data:", obj.data.decode('utf-8'))
                print("Type:", obj.type)
                print()
        else:
            print("No QR codes found in the frame.")

        # Display the frame
        #cv2.imshow('Frame', frame)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    else:
        print('Failed to capture frame %d' % count)

# Release resources
vidcap.release()
tello.streamoff()
