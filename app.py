#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import csv
import itertools
import cv2
import mediapipe as mp
from model import KeyPointClassifier


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

# Draws label on the image
def draw_info_text(image, handedness, hand_sign_text):
    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
        cv2.putText(image, "Finger Gesture:" + info_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                    cv2.LINE_AA)

    return image


# Get the statuses of what fingers are straight or closed based fingertip and the mid join
def fingers(results, mp_hands):
    count = {'RIGHT': 0, 'LEFT': 0}
    finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                   mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]

    finger_stats = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                    'RIGHT_PINKY': False, 'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                    'LEFT_RING': False, 'LEFT_PINKY': False}

    for hand_index, hand_info in enumerate(results.multi_handedness):
        hand = hand_info.classification[0].label
        hand_landmarks = results.multi_hand_landmarks[hand_index]

        for i in finger_tips:
            finger_name = i.name.split("_")[0]
            if hand_landmarks.landmark[i - 2].y > hand_landmarks.landmark[i].y:
                finger_stats[hand.upper() + "_" + finger_name] = True
                count[hand.upper()] += 1

        thumb_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
        thumb_mcp_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP - 2].x

        if (hand == 'Right' and (thumb_tip_x < thumb_mcp_x)) or (
                hand == 'Left' and (thumb_tip_x > thumb_mcp_x)):
            finger_stats[hand.upper() + "_THUMB"] = True
            count[hand.upper()] += 1

    return finger_stats, count


# Compares 2 sets of dict
def compare_input(pic_status, input_status, hand):
    mis_match = {}
    # false means closed and true means
    for i in pic_status.keys():
        if hand.upper() in i:
            if pic_status[i] != input_status[i]:
                mis_match[i] = pic_status[i]

    return mis_match


# Count for the highest occurring prediction
def count_pred(l):
    count = 0
    myset = set(l)
    for value in myset:
        if l.count(value) > count:
            count = l.count(value)
            res = value
        elif l.count(value) == count:
            res = False

    return res


# Retrieves all the label names
def get_dictionary():
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    return keypoint_classifier_labels
