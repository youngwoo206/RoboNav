import os
import json

with open("track1-qv_pipe_train.json", "r") as f:
    data = json.load(f)
    f.close()

available_files = os.listdir("/home/anirudh/code/repos/pipe-defect-detection/raw/")

available_categories = {}
for video in data.keys():
    video_name = video.split(".")[0]
    if video_name in available_files:
        available_categories[video] = data[video]


with open("available_videos.json", "w") as f:
    json.dump(available_categories, f)
    f.close()
