import cv2
from tools import proc_image

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
face_cascade2 = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture("/Users/sim/Downloads/Steve Carell Never Rewatches Himself In _The Office_.mp4")
# cap = cv2.VideoCapture(0)

# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')
frame_num = 0

while True:
    # Read the frame
    x, img = cap.read()
    if not x:
        break

    img = proc_image(img)
    cv2.imshow('vid', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
cap.release()
