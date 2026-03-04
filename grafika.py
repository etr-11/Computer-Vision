import cv2
import numpy as np


image_pts = np.array([ [150, 156], [150, 81], [293, 81],[293, 156] ])

world_pts = np.array([ [123, 170],[91, 121],[376, 120],[445, 170] ])

frame = cv2.imread("demonstration/f2.png")
if frame is None:
    print("Не удалось загрузить image.png")
    exit()

H, _ = cv2.findHomography(image_pts, world_pts)
print("H:\n", H)
print(frame.shape)
warped = cv2.warpPerspective(frame, H, (677, 564))
cv2.imshow("top_view", warped)
cv2.waitKey(0)
