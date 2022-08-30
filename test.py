from turtle import xcor
import cv2
import mediapipe as mp
import math

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)
        image_rows, image_cols, _ = image.shape

        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            all_look_forward = True
            for detection in results.detections:
               
                # mp_drawing.draw_detection(image, detection)
                location = detection.location_data
                if location.format != mp.solutions.drawing_utils.location_data_pb2.LocationData.RELATIVE_BOUNDING_BOX:
                    raise ValueError( 'LocationData must be relative for this drawing funtion to work.')
                # Draws keypoints.
                xy_points = []
                count = 0
                for keypoint in location.relative_keypoints:
                    count = count + 1
                    # print("keypoint", keypoint)
                    keypoint_px = mp.solutions.drawing_utils._normalized_to_pixel_coordinates(keypoint.x, keypoint.y, image_cols, image_rows)
                    # cv2.circle(image, keypoint_px, 1, (255,5,255), 2)
                    # print("keypoint_px", keypoint_px)
                    xy_points.append(keypoint_px)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(image, str(count), keypoint_px, font, 1, (255, 5, 255), 2, cv2.LINE_AA)
                    # right eye, left eye, nose tip, mouth center, right ear tragion, and left ear tragion
                # print("xy_points", xy_points[5][1])
                distance3_5 = math.dist(xy_points[2], xy_points[4])
                distance3_6 = math.dist(xy_points[2], xy_points[5])                
                if (xy_points[5][0] < xy_points[1][0] or xy_points[4][0] > xy_points[0][0]):
                    all_look_forward = False
                else:
                    all_look_forward = True               
            # all look forward
            if all_look_forward  == True:
                print("Take a photo")
            else:
                print("Doesn't take a photo")
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
