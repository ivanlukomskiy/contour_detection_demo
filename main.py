import json

import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation

segmentor = SelfiSegmentation(0)
vid = cv2.VideoCapture(0)

while True:
    # capture frames from camera
    ret, img = vid.read()

    # remove background behind the person
    img = segmentor.removeBG(img, imgBg=(0, 0, 0), threshold=0.9)

    # convert to black/white; blur; do edge detection
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Canny(img, 10, 100)

    # flip colors so the contours are black
    img = cv2.bitwise_not(img)

    # detect contours and draw them on an empty canvas
    contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-1]
    img[:] = 255
    cv2.drawContours(img, contours, -1, (0, 0, 0), 2)

    cv2.imshow('image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# upon exit dump json with polygon coordinates
res = []
for polyline in contours:
    points = []
    for point in polyline:
        points.append([int(point[0][0]), int(point[0][1])])
    res.append(points)

with open("contours.json", "w") as outfile:
    json.dump(res, outfile, indent=2)

vid.release()
cv2.destroyAllWindows()
