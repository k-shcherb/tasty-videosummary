import cv2
import sys
import numpy as np
import math

vidpath = sys.argv[1]
filename = vidpath.split("\\")[-1]
print(filename)
folder_to_save = vidpath.strip(filename)

cap = cv2.VideoCapture(vidpath)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
print(frame_rate)

ret, frame = cap.read()

frames_to_save = []
frame_interval = int(1/60*1000)
paused = frame_interval

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
        paused = 0 if paused !=0 else frame_interval
cv2.destroyAllWindows()
if len(frames_to_save) > 0:
    h, w, d = np.shape(frames_to_save[0])

    num_sqrt = np.sqrt(len(frames_to_save))
    nearest_square = math.ceil(num_sqrt)
    print(nearest_square)
    rows = []
    while len(frames_to_save) < nearest_square*nearest_square:
        frames_to_save.append(np.zeros_like(frames_to_save[0]))
    for i in range(nearest_square):
        try:
            row = cv2.hconcat(frames_to_save[i*nearest_square:nearest_square+nearest_square*i])
        except IndexError:
            print("found index error")
            if len(frames_to_save[i*nearest_square:]) == 0:
                continue
            else:
                while len(frames_to_save) < nearest_square*nearest_square:
                    frames_to_save.append(np.zeros_like(frames_to_save[0]))
                row = cv2.hconcat(frames_to_save[i*nearest_square:nearest_square+nearest_square*i])
        rows.append(row)

    summary = cv2.vconcat(rows)
    print(np.shape(summary))
    cv2.imshow('summary',summary)
    k = cv2.waitKey(0)
    if k & 0xFF == ord('q'):
        cv2.imwrite("{}{}_summary.png".format(folder_to_save, filename), summary)
        cv2.destroyAllWindows()
        print("saved to {}".format(folder_to_save))
else:
    print("no frames saved")