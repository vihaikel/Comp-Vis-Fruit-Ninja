import cv2
import mediapipe as mp
import config

class ColorTracker:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.HEIGHT)
        self.trail_points = []

        # Inisialisasi MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        frame = cv2.flip(frame, 1)  # Membalik frame secara horizontal
        frame = cv2.resize(frame, (config.WIDTH, config.HEIGHT))  # Mengubah ukuran frame sesuai pengaturan

        # MediaPipe membutuhkan format warna rgb
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        current_pos = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Mengambil ID Index Tip Finger (ID 8)
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                x = int(index_tip.x * config.WIDTH)
                y = int(index_tip.y * config.HEIGHT)
                current_pos = (x, y)
                self.trail_points.append(current_pos)
                break  # Hanya mengambil tangan pertama yang terdeteksi

        # Batasi panjang jejak pedang
        if len(self.trail_points) > config.MAX_TRAIL_LEN:
            self.trail_points.pop(0)

        return frame, current_pos

    def release(self):
        self.cap.release()
        self.hands.close()
