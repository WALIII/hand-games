
import cv2
import mediapipe as mp
import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.index_tip_pos = (0, 0)

    def update(self):
        success, frame = self.cap.read()
        if not success:
            return self.index_tip_pos
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Just use first hand
            index_tip = hand_landmarks.landmark[8]
            self.index_tip_pos = (
                int(index_tip.x * self.width),
                int(index_tip.y * self.height)
            )
        
        return self.index_tip_pos

    def wristdist(self): #index top to wrist
        success, frame = self.cap.read()
        if not success:
            return None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            pinkymcp = hand.landmark[17]
            indexmcp = hand.landmark[5]
            wrist = hand.landmark[0]
            middlemcp = hand.landmark[9]
            indextop = hand.landmark[12]

            x1, y1 = int(pinkymcp.x * self.width), int(pinkymcp.y * self.height)
            x2, y2 = int(wrist.x * self.width), int(wrist.y * self.height)
            x3, y3 = int(indexmcp.x * self.width), int(indexmcp.y * self.height)

            hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
            hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
            hand_size = (hand_width + hand_height) / 2

            # Now calculate distance from wrist to index tip
            tip_x = int(indextop.x * self.width)
            tip_y = int(indextop.y * self.height)
            wrist_x = int(wrist.x * self.width)
            wrist_y = int(wrist.y * self.height)

            distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
            if hand_size > 0:
                return (distance / hand_size)
            elif distance > 0:
                return distance
            
    def pinkywrist(self): #pinky top to wrist
        success, frame = self.cap.read()
        if not success:
            return None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            pinkymcp = hand.landmark[17]
            indexmcp = hand.landmark[5]
            wrist = hand.landmark[0]
            middlemcp = hand.landmark[9]
            pinkytop = hand.landmark[20]

            x1, y1 = int(pinkymcp.x * self.width), int(pinkymcp.y * self.height)
            x2, y2 = int(wrist.x * self.width), int(wrist.y * self.height)
            x3, y3 = int(indexmcp.x * self.width), int(indexmcp.y * self.height)

            hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
            hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
            hand_size = (hand_width + hand_height) / 2

            # Now calculate distance from wrist to index tip
            tip_x = int(pinkytop.x * self.width)
            tip_y = int(pinkytop.y * self.height)
            wrist_x = int(wrist.x * self.width)
            wrist_y = int(wrist.y * self.height)

            distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
            if hand_size > 0:
                return (distance / hand_size)
            elif distance > 0:
                return distance

        return None
    def thumbwrist(self): #thumb top to wrist
        success, frame = self.cap.read()
        if not success:
            return None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            pinkymcp = hand.landmark[17]
            indexmcp = hand.landmark[5]
            wrist = hand.landmark[0]
            middlemcp = hand.landmark[9]
            thumbtop = hand.landmark[4]

            x1, y1 = int(pinkymcp.x * self.width), int(pinkymcp.y * self.height)
            x2, y2 = int(wrist.x * self.width), int(wrist.y * self.height)
            x3, y3 = int(indexmcp.x * self.width), int(indexmcp.y * self.height)

            hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
            hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
            hand_size = (hand_width + hand_height) / 2

            tip_x = int(thumbtop.x * self.width)
            tip_y = int(thumbtop.y * self.height)
            wrist_x = int(wrist.x * self.width)
            wrist_y = int(wrist.y * self.height)

            distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
            if hand_size > 0:
                return (distance / hand_size)
            elif distance > 0:
                return distance

        return None


    def indexwrist(self): 
        success, frame = self.cap.read()
        if not success:
            return None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            pinkymcp = hand.landmark[17]
            indexmcp = hand.landmark[5]
            wrist = hand.landmark[0]
            middlemcp = hand.landmark[9]
            indextop = hand.landmark[8]

            x1, y1 = int(pinkymcp.x * self.width), int(pinkymcp.y * self.height)
            x2, y2 = int(wrist.x * self.width), int(wrist.y * self.height)
            x3, y3 = int(indexmcp.x * self.width), int(indexmcp.y * self.height)

            hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
            hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
            hand_size = (hand_width + hand_height) / 2

            tip_x = int(indextop.x * self.width)
            tip_y = int(indextop.y * self.height)
            wrist_x = int(wrist.x * self.width)
            wrist_y = int(wrist.y * self.height)

            distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
            if hand_size > 0:
                return (distance / hand_size)
            elif distance > 0:
                return distance
    def ringwrist(self): 
        success, frame = self.cap.read()
        if not success:
            return None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            pinkymcp = hand.landmark[17]
            indexmcp = hand.landmark[5]
            wrist = hand.landmark[0]
            middlemcp = hand.landmark[9]
            ringtop = hand.landmark[16]

            x1, y1 = int(pinkymcp.x * self.width), int(pinkymcp.y * self.height)
            x2, y2 = int(wrist.x * self.width), int(wrist.y * self.height)
            x3, y3 = int(indexmcp.x * self.width), int(indexmcp.y * self.height)

            hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
            hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
            hand_size = (hand_width + hand_height) / 2

            
            tip_x = int(ringtop.x * self.width)
            tip_y = int(ringtop.y * self.height)
            wrist_x = int(wrist.x * self.width)
            wrist_y = int(wrist.y * self.height)

            distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
            if hand_size > 0:
                return (distance / hand_size)
            elif distance > 0:
                return distance
        return None
    def handsize(self, frame, results):
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            h, w, _ = frame.shape  

            pinky = hand.landmark[17]
            index = hand.landmark[5]
            wrist = hand.landmark[0]

            x1, y1 = pinky.x * w, pinky.y * h
            x2, y2 = wrist.x * w, wrist.y * h
            x3, y3 = index.x * w, index.y * h

            hand_width = ((x1 - x3)**2 + (y1 - y3)**2)**0.5
            hand_height = ((x2 - x3)**2 + (y2 - y3)**2)**0.5
            hand_size = (hand_width + hand_height) / 2

            return hand_size
    def middlewrist(self):
        success, frame = self.cap.read()
        if not success:
            return None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            pinkymcp = hand.landmark[17]
            indexmcp = hand.landmark[5]
            wrist = hand.landmark[0]
            middlemcp = hand.landmark[9]
            pinkytop = hand.landmark[20]

            x1, y1 = int(pinkymcp.x * self.width), int(pinkymcp.y * self.height)
            x2, y2 = int(wrist.x * self.width), int(wrist.y * self.height)
            x3, y3 = int(indexmcp.x * self.width), int(indexmcp.y * self.height)

            hand_width = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
            hand_height = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
            hand_size = (hand_width + hand_height) / 2

            tip_x = int(middlemcp.x * self.width)
            tip_y = int(middlemcp.y * self.height)
            wrist_x = int(wrist.x * self.width)
            wrist_y = int(wrist.y * self.height)

            distance = ((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2) ** 0.5
            if hand_size > 0:
                return (distance / hand_size)
            elif distance > 0:
                return distance
        return None
