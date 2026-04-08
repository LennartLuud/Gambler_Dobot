# Dual-camera YOLO card detection
# Press Q in either window to stop, S to toggle confidence display

import math
import threading
import cv2
from collections import Counter, deque
from ultralytics import YOLO

DEFAULT_MODEL = "synthetic"
SHOW_CONFIDENCE = True

configuration_dict = {
    "synthetic": {
        "model_path": "C:/Users/luud.lt7a493/Desktop/luud proge/python/dobonontsik/yolov8m_synthetic.pt",
        "class_names": [
            "10", "10", "10", "10",
            "2",  "2",  "2",  "2",
            "3",  "3",  "3",  "3",
            "4",  "4",  "4",  "4",
            "5",  "5",  "5",  "5",
            "6",  "6",  "6",  "6",
            "7",  "7",  "7",  "7",
            "8",  "8",  "8",  "8",
            "9",  "9",  "9",  "9",
            "A",  "A",  "A",  "A",
            "J",  "J",  "J",  "J",
            "K",  "K",  "K",  "K",
            "Q",  "Q",  "Q",  "Q",
        ],
    },
}

card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "A": 1, "J": 10, "K": 10, "Q": 10,
}

# Shared state per camera
camera_state = {
    1: {"stable_cards": [], "lock": threading.Lock()},
    0: {"stable_cards": [], "lock": threading.Lock()},
}

stop_event = threading.Event()

print("Loading model...")
current_config = configuration_dict[DEFAULT_MODEL]
# Load once — YOLO is not thread-safe for the same instance, so each thread gets its own
classNames = current_config["class_names"]
model_path = current_config["model_path"]
file_lock = threading.Lock()

class CameraThread(threading.Thread):
    def __init__(self, cam_id):
        super().__init__()
        self.cam_id = cam_id
        self.daemon = True  # dies when main thread exits

    def run(self):
        global SHOW_CONFIDENCE

        # Each thread loads its own model instance (YOLO is not thread-safe)
        model = YOLO(model_path)

        cap = cv2.VideoCapture(self.cam_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not cap.isOpened():
            print(f"[Camera {self.cam_id}] Could not open camera.")
            return

        window_title = f"Camera {self.cam_id} - Cards Detection ({DEFAULT_MODEL})"
        frame_history = deque(maxlen=10)
        frame_count = 0

        while not stop_event.is_set():
            success, img = cap.read()
            if not success:
                print(f"[Camera {self.cam_id}] Failed to read frame.")
                break

            results = model(img, stream=True, verbose=False)
            detected_cards = []
            seen_cards = set()
            total_score = 0

            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])
                    confidence = math.ceil(box.conf[0].item() * 100) / 100
                    cls = int(box.cls[0])
                    class_name = classNames[cls]

                    if class_name in seen_cards:
                        continue
                    seen_cards.add(class_name)

                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    total_score += card_values.get(class_name, 0)
                    detected_cards.append(class_name)

                    label = class_name if not SHOW_CONFIDENCE else f"{class_name} {confidence}"
                    cv2.putText(img, label, (x1, y1),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            frame_history.append(set(detected_cards))
            frame_count += 1

            if frame_count % 10 == 0:
                all_cards = [card for frame in frame_history for card in frame]
                counts = Counter(all_cards)
                stable = [card for card, count in counts.items() if count >= 6]

                with camera_state[self.cam_id]["lock"]:
                    camera_state[self.cam_id]["stable_cards"] = stable
            file_lock.acquire()
            try:
                cam0_cards = camera_state[0]["stable_cards"]
                cam1_cards = camera_state[1]["stable_cards"]
                with open("C:/Users/luud.lt7a493/Desktop/luud proge/python/dobonontsik/detected_cards.txt", "w", encoding="utf-8") as f:
                    f.write(" ".join(cam0_cards) + "\n")
                    f.write(" ".join(cam1_cards) + "\n")
                    f.write("0")
            finally:
                file_lock.release()

            cv2.putText(img, f"Total Score: {total_score}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(window_title, img)

            key = cv2.waitKey(1)
            if key == ord("q"):
                stop_event.set()  # stop all threads
                break
            if key == ord("s"):
                SHOW_CONFIDENCE = not SHOW_CONFIDENCE

        cap.release()
        cv2.destroyWindow(window_title)


def get_stable_cards(cam_id):
    """Fetch latest stable cards detected by a given camera."""
    with camera_state[cam_id]["lock"]:
        return list(camera_state[cam_id]["stable_cards"])


# Start both camera threads
thread1 = CameraThread(cam_id=1)
thread2 = CameraThread(cam_id=0)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

cv2.destroyAllWindows()
print("All cameras stopped.")
