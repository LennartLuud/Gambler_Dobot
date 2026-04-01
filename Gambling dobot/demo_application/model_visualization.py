# Base code provided by Dipankar Medhi article https://dipankarmedh1.medium.com/real-time-object-detection-with-yolo-and-webcam-enhancing-your-computer-vision-skills-861b97c78993
# Note press Q to stop the demo

import math
import sys
from ultralytics import YOLO
import cv2

# Change to 'tuned' to use it as the default one
DEFAULT_MODEL = "synthetic"
SHOW_CONFIDENCE = True

configuration_dict = {
    "synthetic": {
        "model_path": "C:/Users/ligi.sn7a493/Documents/Gambler_Dobot-main/Gambling dobot/demo_application/final_models/yolov8m_synthetic.pt",
        "class_names": [
            "10",
            "10",
            "10",
            "10",
            "2",
            "2",
            "2",
            "2",
            "3",
            "3",
            "3",
            "3",
            "4",
            "4",
            "4",
            "4",
            "5",
            "5",
            "5",
            "5",
            "6",
            "6",
            "6",
            "6",
            "7",
            "7",
            "7",
            "7",
            "8",
            "8",
            "8",
            "8",
            "9",
            "9",
            "9",
            "9",
            "A",
            "A",
            "A",
            "A",
            "J",
            "J",
            "J",
            "J",
            "K",
            "K",
            "K",
            "K",
            "Q",
            "Q",
            "Q",
            "Qs",
        ],
    },
}

print("Loading application...")
"""
configuration_model = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_MODEL

if configuration_model not in configuration_dict.keys():
    print(f"Allowed parameters for model are {configuration_dict.keys()}. Defaulting to {DEFAULT_MODEL}...")
    configuration_model = DEFAULT_MODEL
"""
current_config = configuration_dict.get(DEFAULT_MODEL)

# Load the model and class names
model = YOLO(current_config["model_path"])
classNames = current_config["class_names"]

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 960)
cap.set(4, 720)


# Card values mapping
card_values = {
    "2c": 2,
    "2d": 2,
    "2h": 2,
    "2s": 2,
    "3c": 3,
    "3d": 3,
    "3h": 3,
    "3s": 3,
    "4c": 4,
    "4d": 4,
    "4h": 4,
    "4s": 4,
    "5c": 5,
    "5d": 5,
    "5h": 5,
    "5s": 5,
    "6c": 6,
    "6d": 6,
    "6h": 6,
    "6s": 6,
    "7c": 7,
    "7d": 7,
    "7h": 7,
    "7s": 7,
    "8c": 8,
    "8d": 8,
    "8h": 8,
    "8s": 8,
    "9c": 9,
    "9d": 9,
    "9h": 9,
    "9s": 9,
    "10c": 10,
    "10d": 10,
    "10h": 10,
    "10s": 10,
    "Ac": 1,
    "Ad": 1,
    "Ah": 1,
    "As": 1,
    "Jc": 10,
    "Jd": 10,
    "Jh": 10,
    "Js": 10,
    "Kc": 10,
    "Kd": 10,
    "Kh": 10,
    "Ks": 10,
    "Qc": 10,
    "Qd": 10,
    "Qh": 10,
    "Qs": 10,
}

window_title = f"Playing Cards Detection - Model: {DEFAULT_MODEL}"
from collections import Counter, deque

detected_cards = []
frame_history = deque(maxlen=10)  # stores each frame's detected set
frame_count = 0

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    total_score = 0
    detected_cards.clear()
    seen_cards = set()

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            confidence = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            class_name = classNames[cls]

            if class_name in seen_cards:
                continue
            seen_cards.add(class_name)

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            total_score += card_values.get(class_name, 0)
            detected_cards.append(class_name)

            display_text = class_name if not SHOW_CONFIDENCE else f"{class_name} {confidence}"
            cv2.putText(img, display_text, [x1, y1], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    frame_history.append(set(detected_cards))  # log this frame's cards
    frame_count += 1

    # Every 10 frames, write only cards seen in majority (6+) of last 10 frames
    if frame_count % 10 == 0:
        all_cards = [card for frame in frame_history for card in frame]
        counts = Counter(all_cards)
        stable_cards = [card for card, count in counts.items() if count >= 6]

        with open("detected_cards.txt", "w", encoding="utf-8") as f:
            f.write(" ".join(stable_cards) + "\n")

    cv2.putText(img, f"Total Score: {total_score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow(window_title, img)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    if key == ord("s"):
        SHOW_CONFIDENCE = not SHOW_CONFIDENCE