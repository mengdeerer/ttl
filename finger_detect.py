import cv2
import mediapipe as mp
import numpy as np
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_tracking_confidence=0.5,
    min_detection_confidence=0.5,
)
draw = mp.solutions.drawing_utils


def angle(joint0, jointi, jointj):
    # 计算角度
    xi, yi = jointi.x, jointi.y
    xj, yj = jointj.x, jointj.y
    x0, y0 = joint0.x, joint0.y
    v1 = [xi - x0, yi - y0]
    v2 = [xj - x0, yj - y0]
    L1 = (v1[0] ** 2 + v1[1] ** 2) ** 0.5
    L2 = (v2[0] ** 2 + v2[1] ** 2) ** 0.5
    cos_angle = (v1[0] * v2[0] + v1[1] * v2[1]) / (L1 * L2)
    theta = np.arccos(cos_angle)
    return theta


def left_or_right(img):
    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape
    results = hands.process(img)
    handness_str = ""
    if results.multi_hand_landmarks:
        for h_idx, hand in enumerate(results.multi_hand_landmarks):
            draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
            # get 21 key points of hand
            hand_info = results.multi_hand_landmarks[h_idx]
            # log left and right hands info
            temp_handness = results.multi_handedness[h_idx].classification[0].label
            handness_str += temp_handness
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.putText(
        img, handness_str, (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 0, 0), 2
    )
    return handness_str, img


def finger_count(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape
    results = hands.process(img)
    finger_count = 0
    if results.multi_hand_landmarks:
        for h_idx, hand in enumerate(results.multi_hand_landmarks):
            draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
            # get 21 key points of hand
            hand_info = results.multi_hand_landmarks[h_idx]
            # log left and right hands info
            temp_handness = results.multi_handedness[h_idx].classification[0].label

            tip_indexes = [(5, 8), (9, 12), (13, 16), (17, 20)]
            for tipi, tipj in tip_indexes:
                # 判断该手指是否伸直
                joint0 = hand_info.landmark[0]
                jointi = hand_info.landmark[tipi]
                jointj = hand_info.landmark[tipj]

                theta = angle(jointi, joint0, jointj)
                if tipi == 5:
                    img = cv2.putText(
                        img,
                        str(theta),
                        (25, 190),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.6,
                        (255, 0, 255),
                        2,
                    )
                if theta > math.pi / 180 * 150:
                    finger_count += 1
            tipi = 2
            tipj = 4
            joint0 = hand_info.landmark[0]
            jointi = hand_info.landmark[tipi]
            jointj = hand_info.landmark[tipj]

            theta = angle(jointi, joint0, jointj)
            if theta > math.pi / 180 * 150:
                finger_count += 1
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.putText(
        img,
        str(finger_count),
        (25, 260),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.6,
        (255, 0, 255),
        2,
    )
    return finger_count, img
