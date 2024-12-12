import os
import cv2
from typing import List

# workdir where videos live
workdir = "/Users/ylee/Documents/Projects/RoboNav/defect_detection/data/raw_videos/"
# videos:List[str] = os.listdir(workdir)
videos = ["3520.mp4"]

for video in videos:
    print(f"Processsing Video: {video}")
    prefix = video.split(".")[0]
    path = f"{workdir}{video}"
    final_path = f"/Users/ylee/Documents/Projects/RoboNav/defect_detection/data/raw_images/{prefix}"
    os.mkdir(final_path)
    vidcap = cv2.VideoCapture(path)
    success,image = vidcap.read()
    count = 1
    while success:
        cv2.imwrite(f"{final_path}/{count}.jpg", image)
        success, image = vidcap.read()
        count += 1

