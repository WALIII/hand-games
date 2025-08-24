import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.index_tip_pos = (0, 0)
        self.frame = None
        self.results = None
        self.frame = None
        self.results = None

    def capture_frame(self):
        """Capture and process one frame per loop iteration"""
    def capture_frame(self):
        """Capture and process one frame per loop iteration"""
        success, frame = self.cap.read()
        if not success:
            self.frame = None
            self.results = None
            return False
        self.frame = frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        return True

    def update(self):
        """Return index fingertip position as (x, y) in pixels"""
        if not self.results or not self.results.multi_hand_landmarks:
            self.frame = None
            self.results = None
            return False
        self.frame = frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        return True

    def update(self):
        """Return index fingertip position as (x, y) in pixels"""
        if not self.results or not self.results.multi_hand_landmarks:
            return self.index_tip_pos

        hand_landmarks = self.results.multi_hand_landmarks[0]
        index_tip = hand_landmarks.landmark[8]
        self.index_tip_pos = (
            int(index_tip.x * self.width),
            int(index_tip.y * self.height)
        )

        hand_landmarks = self.results.multi_hand_landmarks[0]
        index_tip = hand_landmarks.landmark[8]
        self.index_tip_pos = (
            int(index_tip.x * self.width),
            int(index_tip.y * self.height)
        )
        return self.index_tip_pos

    def _get_hand_size(self, hand):
        """Helper to compute normalized hand size for scaling distances"""
        pinkymcp = hand.landmark[17]
        indexmcp = hand.landmark[5]
        wrist = hand.landmark[0]

        x1, y1 = pinkymcp.x * self.width, pinkymcp.y * self.height
        x2, y2 = wrist.x * self.width, wrist.y * self.height
        x3, y3 = indexmcp.x * self.width, indexmcp.y * self.height
    def _get_hand_size(self, hand):
        """Helper to compute normalized hand size for scaling distances"""
        pinkymcp = hand.landmark[17]
        indexmcp = hand.landmark[5]
        wrist = hand.landmark[0]

        x1, y1 = pinkymcp.x * self.width, pinkymcp.y * self.height
        x2, y2 = wrist.x * self.width, wrist.y * self.height
        x3, y3 = indexmcp.x * self.width, indexmcp.y * self.height

        hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
        hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
        hand_size = (hand_width + hand_height) / 2
        return hand_size

    def wristdist(self):
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        indextip = hand.landmark[12]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = indextip.x * self.width
        tip_y = indextip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height
        hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
        hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
        hand_size = (hand_width + hand_height) / 2
        return hand_size

    def wristdist(self):
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        indextip = hand.landmark[12]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = indextip.x * self.width
        tip_y = indextip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def pinkywrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def pinkywrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        pinkytip = hand.landmark[20]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = pinkytip.x * self.width
        tip_y = pinkytip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        hand = self.results.multi_hand_landmarks[0]
        pinkytip = hand.landmark[20]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = pinkytip.x * self.width
        tip_y = pinkytip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def thumbwrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def thumbwrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        thumbtip = hand.landmark[4]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = thumbtip.x * self.width
        tip_y = thumbtip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        hand = self.results.multi_hand_landmarks[0]
        thumbtip = hand.landmark[4]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = thumbtip.x * self.width
        tip_y = thumbtip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None
        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def indexwrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
    def indexwrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        indextip = hand.landmark[8]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = indextip.x * self.width
        tip_y = indextip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        hand = self.results.multi_hand_landmarks[0]
        indextip = hand.landmark[8]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = indextip.x * self.width
        tip_y = indextip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def ringwrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def ringwrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        ringtip = hand.landmark[16]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = ringtip.x * self.width
        tip_y = ringtip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        hand = self.results.multi_hand_landmarks[0]
        ringtip = hand.landmark[16]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = ringtip.x * self.width
        tip_y = ringtip.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def middlewrist(self):
        if not self.results or not self.results.multi_hand_landmarks:
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        middlemcp = hand.landmark[9]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = middlemcp.x * self.width
        tip_y = middlemcp.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        hand = self.results.multi_hand_landmarks[0]
        middlemcp = hand.landmark[9]
        wrist = hand.landmark[0]

        hand_size = self._get_hand_size(hand)

        tip_x = middlemcp.x * self.width
        tip_y = middlemcp.y * self.height
        wrist_x = wrist.x * self.width
        wrist_y = wrist.y * self.height

        distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
        if hand_size > 0:
            return distance / hand_size
        return distance if distance > 0 else None

    def handwall(self):
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

    def handnormalization(self):
        # This method as you had it is incomplete — you can add your normalization logic here
        # using self.frame and self.results if you want.
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand_landmarks = self.results.multi_hand_landmarks[0]
        # Example access:
        thumbtip = hand_landmarks.landmark[4]
        wrist = hand_landmarks.landmark[0]
        middletip = hand_landmarks.landmark[12]
        pinkytop = hand_landmarks.landmark[20]
    def min_max_scale(self,value, calibration_data):
        if not calibration_data:
            return 0

        min_val = min(calibration_data)
        max_val = max(calibration_data)

        if max_val == min_val:
            return 0  # Avoid divide-by-zero
        if value is not None and min_val is not None:
            return (value - min_val) / (max_val - min_val)


        # Add normalization calculations here if needed

    def release(self):
        self.cap.release()
