import cv2
import mediapipe as mp
import numpy

class HandTracker:
    def __init__(self, camera_index=0, WIDTH=640, HEIGHT=480):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_detection_confidence=0.5,
                                         min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.results = None
        self.frame = None
        
        self.width = WIDTH
        self.height = HEIGHT
        # Camera
        self.cap = cv2.VideoCapture(camera_index)

    # -----------------------------
    # Frame handling
    # -----------------------------
    def capture_frame(self):
        """Grab a frame from the camera."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def update(self, frame):
        """Update hand tracking results from a frame (BGR)."""
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(self.frame)

    def draw(self, frame):
        """Draw hand landmarks on frame."""
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    # -----------------------------
    # Utility methods
    # -----------------------------
    def _get_hand_size(self, hand):
        """Reference size of hand in world coords (meters)."""
        wrist = hand.landmark[0]       # wrist
        middle_mcp = hand.landmark[9]  # base of middle finger
        ref_len = ((wrist.x - middle_mcp.x) ** 2 +
                   (wrist.y - middle_mcp.y) ** 2 +
                   (wrist.z - middle_mcp.z) ** 2) ** 0.5
        return ref_len if ref_len > 0 else 1.0

    def _normalized_distance(self, hand, id1, id2):
        """Normalized 3D distance between two landmarks."""
        ref = self._get_hand_size(hand)
        p1, p2 = hand.landmark[id1], hand.landmark[id2]
        dist = ((p1.x - p2.x) ** 2 +
                (p1.y - p2.y) ** 2 +
                (p1.z - p2.z) ** 2) ** 0.5
        return dist / ref if ref > 0 else None

    def _get_first_hand(self):
        """Return the first detected hand or None."""
        if self.results and self.results.multi_hand_landmarks:
            return self.results.multi_hand_landmarks[0]
        return None

    # -----------------------------
    # Distance functions (normalized, world coords)
    # -----------------------------
    def thumbwrist(self):
        hand = self._get_first_hand()
        return self._normalized_distance(hand, 4, 0) if hand else None

    def indexwrist(self):
        hand = self._get_first_hand()
        return self._normalized_distance(hand, 8, 0) if hand else None

    def middlewrist(self):
        hand = self._get_first_hand()
        return self._normalized_distance(hand, 12, 0) if hand else None

    def ringwrist(self):
        hand = self._get_first_hand()
        return self._normalized_distance(hand, 16, 0) if hand else None

    def pinkywrist(self):
        hand = self._get_first_hand()
        return self._normalized_distance(hand, 20, 0) if hand else None

    def wristdist(self):
        """Example: middle finger tip to wrist."""
        hand = self._get_first_hand()
        return self._normalized_distance(hand, 12, 0) if hand else None
    def handwall(self):
        """Check if hand is near edges of screen (pixel-based logic)."""
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand_landmarks = self.results.multi_hand_landmarks[0]

        WIDTH = self.width
        HEIGHT = self.height

        thumbtip_x = hand_landmarks.landmark[4].x * WIDTH
        wrist_y = hand_landmarks.landmark[0].y * HEIGHT
        middletip_y = hand_landmarks.landmark[12].y * HEIGHT
        pinkytip_x = hand_landmarks.landmark[20].x * WIDTH

        top = 0
        bottom = 0
        left = 0
        right = 0

        if thumbtip_x > (WIDTH * 0.8):
            left = 1.5
        if wrist_y < (HEIGHT * 0.3):
            bottom = 2
        if middletip_y > (HEIGHT * 0.7):
            top = 3
        if pinkytip_x < (WIDTH * 0.2):
            right = 4

        if top > 0 or bottom > 0 or left > 0 or right > 0:
            return [top, bottom, left, right]
        else:
            return None
    # -----------------------------
    # Cleanup
    # -----------------------------
    def close(self):
        """Release Mediapipe + camera resources."""
        self.hands.close()
        if self.cap.isOpened():
            self.cap.release()
