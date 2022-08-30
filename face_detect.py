from turtle import xcor
import cv2
import mediapipe as mp
import math
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# Kill the gphoto process that starts
# whenever we turn on the camera or
# reboot the raspberry pi

def distance_two_points(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
  
def killGphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    # Search for the process we want to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            # Kill that process!
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d") # This has been written to the while True loop.
# shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # This has been written to the while True loop.
picID = "PiShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "--delete-all-files", "-R"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Desktop/gphoto/images/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create new directory.")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print("Renamed the CR2")


killGphoto2Process()
gp(clearCommand)

 
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

'''
# For static images:
IMAGE_FILES = []
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Draw face detections of each face.
    if not results.detections:
      continue
    annotated_image = image.copy()
    for detection in results.detections:
      print('Nose tip:')
      print(mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
      mp_drawing.draw_detection(annotated_image, detection)
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
'''
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
                distance3_5 = distance_two_points(xy_points[2], xy_points[4])
                distance3_6 = distance_two_points(xy_points[2], xy_points[5])                
                if (xy_points[5][0] < xy_points[1][0] or xy_points[4][0] > xy_points[0][0]):
                    all_look_forward = False
                else:
                    all_look_forward = True               
            # all look forward
            if all_look_forward  == True:
                print("Take a photo")
                shot_date = datetime.now().strftime("%Y-%m-%d")
                shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                createSaveFolder()
                captureImages()
                renameFiles(picID)
            else:
                print("Doesn't take a photo")
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
