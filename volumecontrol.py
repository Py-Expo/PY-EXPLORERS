import cv2 
import mediapipe as mp 
from math import hypot 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np 

def adjust_volume(thumb_coord, middle_finger_coord):
    # Calculate the distance between thumb and middle finger
    L = hypot(middle_finger_coord[0] - thumb_coord[0], middle_finger_coord[1] - thumb_coord[1])
    
    # Map the distance to the volume range (15 - 220) to (0 - 100)
    volume_level = np.interp(L, [15, 220], [0, 100])
    
    # Set the system volume
    devices = AudioUtilities.GetSpeakers() 
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) 
    volume = cast(interface, POINTER(IAudioEndpointVolume)) 
    volume.SetMasterVolumeLevelScalar(volume_level / 100, None)

# Initializing the Model 
mpHands = mp.solutions.hands 
hands = mpHands.Hands( 
    static_image_mode=False, 
    model_complexity=1, 
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75, 
    max_num_hands=2) 

Draw = mp.solutions.drawing_utils 

# Start capturing video from webcam 
cap = cv2.VideoCapture(0) 

while True: 
    # Read video frame by frame 
    _, frame = cap.read() 
    
    # Flip image 
    frame = cv2.flip(frame, 1) 
    
    # Convert BGR image to RGB image 
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    
    # Process the RGB image 
    Process = hands.process(frameRGB) 
    
    landmarkList = [] 
    # if hands are present in image(frame) 
    if Process.multi_hand_landmarks: 
        # detect handmarks 
        for handlm in Process.multi_hand_landmarks: 
            for _id, landmarks in enumerate(handlm.landmark): 
                # store height and width of image 
                height, width, color_channels = frame.shape 
                
                # calculate and append x, y coordinates 
                # of handmarks from image(frame) to lmList 
                x, y = int(landmarks.x * width), int(landmarks.y * height)			 
                landmarkList.append([_id, x, y]) 
            
            # draw Landmarks 
            Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS) 
    
    # If landmarks list is not empty 
    if landmarkList: 
        # store x, y coordinates of (tip of) thumb 
        thumb_coord = landmarkList[4][1], landmarkList[4][2]
        
        # store x, y coordinates of (tip of) middle finger 
        middle_finger_coord = landmarkList[12][1], landmarkList[12][2]
        
        # draw circle on thumb and middle finger tip 
        cv2.circle(frame, thumb_coord, 7, (0, 255, 0), cv2.FILLED) 
        cv2.circle(frame, middle_finger_coord, 7, (0, 255, 0), cv2.FILLED) 
        
        # draw line from tip of thumb to tip of middle finger 
        cv2.line(frame, thumb_coord, middle_finger_coord, (0, 255, 0), 3) 
        
        # Adjust system volume based on thumb and middle finger coordinates
        adjust_volume(thumb_coord, middle_finger_coord)
    
    # Display Video and when 'q' is entered, 
    # destroy the window 
    cv2.imshow('Image', frame) 
    if cv2.waitKey(1) & 0xff == ord('q'): 
        break

# Release the camera and close all OpenCV windows
cap.release() 
cv2.destroyAllWindows()
