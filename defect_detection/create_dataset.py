import os
import cv2
import json
import keras
import numpy as np

available_videos = [("4736", 0), ("2383", 0), ("d20017", 1), ("26852", 1)]
categorization = [0, 0, 1, 1]
out_json = {"data": [], "target" : []}

for video, categorization  in available_videos:
    print(f"Categorizing Video")
    base_path = f"data/raw_images/{video}"
    all_frames = os.listdir(f"{base_path}/")
    counter = 0
    for frame in all_frames:
        print(frame)
        if video == "26852":
            if counter < 25 * 60:
                counter += 1
                continue
            else:
                success, image = cv2.imread(f"{base_path}/{frame}")
                out_json["data"].append(image)
                out_json["target"].append(categorization)

        else:
            image = cv2.imread(f"{base_path}/{frame}")
            out_json["data"].append(np.ndarray.tolist(image))
            out_json["target"].append(categorization)

with open("data/training_data.json", "w") as f:
    json.dump(out_json, f)





