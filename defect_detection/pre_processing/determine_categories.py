import json

with open("defect_detection/available_videos.json","r") as f:
    data = json.load(f)
    f.close()

categories = {} # cat > [count, videos...]

for video_name in data.keys():
    cats = data[video_name]

    for cat in cats:
        if cat in categories:
            categories[cat][0] += 1
            categories[cat].append(video_name)
        else:
            categories[cat] = [1, video_name]

with open("video_categories.json", "w") as f:
    json.dump(categories, f)
    f.close()
