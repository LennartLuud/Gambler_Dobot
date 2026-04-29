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
            "10C", "10D", "10H", "10S",
            "2C",  "2D",  "2H",  "2S",
            "3C",  "3D",  "3H",  "3S",
            "4C",  "4D",  "4H",  "4S",
            "5C",  "5D",  "5H",  "5S",
            "6C",  "6D",  "6H",  "6S",
            "7C",  "7D",  "7H",  "7S",
            "8C",  "8D",  "8H",  "8S",
            "9C",  "9D",  "9H",  "9S",
            "AC",  "AD",  "AH",  "AS",
            "JC",  "JD",  "JH",  "JS",
            "KC",  "KD",  "KH",  "KS",
            "QC",  "QD",  "QH",  "QS",
        ],
    },
}

card_values = {
    "2C": 2,  "2D": 2,  "2H": 2,  "2S": 2,
    "3C": 3,  "3D": 3,  "3H": 3,  "3S": 3,
    "4C": 4,  "4D": 4,  "4H": 4,  "4S": 4,
    "5C": 5,  "5D": 5,  "5H": 5,  "5S": 5,
    "6C": 6,  "6D": 6,  "6H": 6,  "6S": 6,
    "7C": 7,  "7D": 7,  "7H": 7,  "7S": 7,
    "8C": 8,  "8D": 8,  "8H": 8,  "8S": 8,
    "9C": 9,  "9D": 9,  "9H": 9,  "9S": 9,
    "10C":10, "10D":10, "10H":10, "10S":10,
    "AC": 1,  "AD": 1,  "AH": 1,  "AS": 1,
    "JC": 10, "JD": 10, "JH": 10, "JS": 10,
    "KC": 10, "KD": 10, "KH": 10, "KS": 10,
    "QC": 10, "QD": 10, "QH": 10, "QS": 10,
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

last_written_state = {"cam0": [], "cam1": []}

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

            if frame_count % 5 == 0:
                all_cards = [card for frame in frame_history for card in frame]
                counts = Counter(all_cards)
                stable = [card for card, count in counts.items() if count >= 6]

                # If nothing detected recently, clear immediately
                if not detected_cards:
                    stable = []

                with camera_state[self.cam_id]["lock"]:
                    camera_state[self.cam_id]["stable_cards"] = stable
            

            file_lock.acquire()
            try:
                cam0_cards = [c[:-1] if not c.startswith("10") else "10" for c in camera_state[0]["stable_cards"]]
                cam1_cards = [c[:-1] if not c.startswith("10") else "10" for c in camera_state[1]["stable_cards"]]
                
                if cam0_cards != last_written_state["cam0"] or cam1_cards != last_written_state["cam1"]:
                    last_written_state["cam0"] = cam0_cards
                    last_written_state["cam1"] = cam1_cards
                    with open("C:/Users/luud.lt7a493/Desktop/luud proge/python/dobonontsik/detected_cards.txt", "w") as f:
                        f.write(" ".join(cam0_cards) + "\n")
                        f.write(" ".join(cam1_cards) + "\n")
                        f.write("0")
                    print(cam1_cards, cam0_cards)
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
