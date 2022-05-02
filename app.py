#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import csv
import itertools
import cv2
import mediapipe as mp
from model import KeyPointClassifier


def camera():

    # Camera preparation ###############################################################
    cap = cv2.VideoCapture(0) #was 4
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    # Model load #############################################################
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode='store_true',
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )

    keypoint_classifier = KeyPointClassifier()

    # Read labels ###########################################################
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    #  ########################################################################


    while True:

        #don't need this anymore
        key = cv2.waitKey(10)
        if key == 27:  # ESC
            break

        # Camera capture #####################################################
        ret, image = cap.read()
        #can edit this
        if not ret:
            break
        image = cv2.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation #############################################################
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        #  ####################################################################
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):

                # Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)
                imagec, fs, count = fingers(image, results, mp_hands)
                image_details = [imagec, fs, count]
                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                hand_gesture = keypoint_classifier_labels[hand_sign_id]
                input_hand = handedness.classification[0].label[0:].lower()

                pic_image = cv2.imread('img/%s/%s.png' % (input_hand, hand_gesture.lower()), 0)
                pic_image = cv2.cvtColor(pic_image, cv2.COLOR_BGR2RGB)
                results2 = hands.process(pic_image)

                if results2.multi_handedness is not None:
                    pic, fs2, count2 = fingers(pic_image, results2, mp_hands)
                    pic_details = [pic, fs2, count2]
                    finger_diff = compare_input(pic_details, image_details, input_hand)
                else:
                    # finger_diff = compare_close(image_details[1])
                    finger_diff = {}

                # Drawing part
                debug_image = draw_info_text(
                    debug_image,
                    handedness,
                    keypoint_classifier_labels[hand_sign_id]
                )

        # Screen reflection #############################################################
        cv2.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv2.destroyAllWindows()


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


#might be able to get rid of this
def draw_info_text(image, handedness, hand_sign_text):

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
        cv2.putText(image, "Finger Gesture:" + info_text, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                   cv2.LINE_AA)

    return image

def fingers(image, results, hands):
    height, width, _ = image.shape
    #if gesture != None:
    #    output_image = cv2.imread('img/'+gesture.lower()+'.png',0)
    #    print("load")
    #else:
    output_image = image.copy()
    count = {'RIGHT': 0, 'LEFT': 0}
    fingers_tips_ids = [hands.HandLandmark.INDEX_FINGER_TIP, hands.HandLandmark.MIDDLE_FINGER_TIP,
                        hands.HandLandmark.RING_FINGER_TIP, hands.HandLandmark.PINKY_TIP]

    fingers_statuses = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                        'RIGHT_PINKY': False, 'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                        'LEFT_RING': False, 'LEFT_PINKY': False}

    for hand_index, hand_info in enumerate(results.multi_handedness):
        hand_label = hand_info.classification[0].label
        hand_landmarks = results.multi_hand_landmarks[hand_index]

        for tip_index in fingers_tips_ids:
            finger_name = tip_index.name.split("_")[0]
            if (hand_landmarks.landmark[tip_index].y < hand_landmarks.landmark[tip_index - 2].y):
                fingers_statuses[hand_label.upper() + "_" + finger_name] = True
                count[hand_label.upper()] += 1

        thumb_tip_x = hand_landmarks.landmark[hands.HandLandmark.THUMB_TIP].x
        thumb_mcp_x = hand_landmarks.landmark[hands.HandLandmark.THUMB_TIP - 2].x

        if (hand_label == 'Right' and (thumb_tip_x < thumb_mcp_x)) or (
                hand_label == 'Left' and (thumb_tip_x > thumb_mcp_x)):
            fingers_statuses[hand_label.upper() + "_THUMB"] = True
            count[hand_label.upper()] += 1

    return output_image, fingers_statuses, count

def compare_input(img_details, input_details, hand):
    pic_frame = img_details[0]
    pic_status = img_details[1]
    pic_count = img_details[2]

    input_frame = input_details[0]
    input_status = input_details[1]
    input_count = input_details[2]


    mis_match = {}
    #false means closed and true means
    for i in pic_status.keys():
        if hand.upper() in i:
            if pic_status[i] != input_status[i]:
                #print(pic_status[i], input_status[i])
                mis_match[i] = pic_status[i]
    #print(mis_match)
    return mis_match

def compare_close(input_status):
    fingers_statuses = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                        'RIGHT_PINKY': False, 'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                        'LEFT_RING': False, 'LEFT_PINKY': False}
    mis_match = {}
    for i in fingers_statuses.keys():
        if fingers_statuses[i] != input_status[i]:
            #print(pic_status[i], input_status[i])
            mis_match[i] = input_status[i]

    return mis_match

def checkfingers(fs):
    fingers_statuses = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                        'RIGHT_PINKY': False, 'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                        'LEFT_RING': False, 'LEFT_PINKY': False}
    closed = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                        'RIGHT_PINKY': False, 'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                        'LEFT_RING': False, 'LEFT_PINKY': False}
    l_good_status ={'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                        'RIGHT_PINKY': False, 'LEFT_THUMB': True, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                        'LEFT_RING': False, 'LEFT_PINKY': False}

    if l_good_status == fs:
        print("matches")
    else:
        print('not matching')


def count_pred(l):
    count = 0
    multi = False
    myset = set(l)
    for value in myset:
        if l.count(value) > count:
            count = l.count(value)
            res = value
            multi = False
        elif l.count(value) == count:
            multi = True
            res = False

    return res

#if __name__ == '__main__':
#    main()

#camera()