import cv2
import sys
import numpy as np

vidpath = sys.argv[1]
filename = vidpath.split("\\")[-1]
print(filename)
folder_to_save = vidpath.strip(filename)

cap = cv2.VideoCapture(vidpath)

ret, frame = cap.read()

frames_to_save = []

paused = 1

while ret:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('video', frame)
    k = cv2.waitKey(paused)
    if k & 0xFF == ord('q'):
        break
    elif k & 0xFF == ord('k'):
        frames_to_save.append(frame)
    elif k & 0xFF == ord('p'):
        paused = 0 if paused == 1 else 1
cv2.destroyAllWindows()
if len(frames_to_save) > 0:
    h, w, d = np.shape(frames_to_save[0])
    summary = cv2.vconcat(frames_to_save)
    print(np.shape(summary))
    cv2.imshow('summary',summary)
    k = cv2.waitKey(0)
    if k & 0xFF == ord('q'):
        cv2.imwrite("{}{}_summary.png".format(folder_to_save, filename), summary)
        cv2.destroyAllWindows()
        print("saved to {}".format(folder_to_save))
else:
    print("no frames saved")