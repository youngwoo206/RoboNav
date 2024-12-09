import os
import cv2
from typing import List

# workdir where videos live
workdir = "/home/anirudh/code/defect_detection/OpenDataLab___VideoPipe/raw/track1-Video_Defect_Classification/track1_raw_video/"
videos:List[str] = os.listdir(workdir)

for video in videos:
    print(f"Processsing Video: {video}")
    prefix = video.split(".")[0]
    path = f"{workdir}{video}"
    final_path = f"/home/anirudh/code/repos/RoboNav/defect_detection/raw_images/{prefix}/"
    os.mkdir(final_path)
    vidcap = cv2.VideoCapture(path)
    success,image = vidcap.read()
    count = 1
    while success:
        cv2.imwrite(f"final_path/{count}.jpg", image)
        success, image = vidcap.read()
        count += 1

