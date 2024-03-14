import cv2 
import mediapipe as mp 
import pyautogui
from math import hypot 
import numpy as np 

def scroll_up_or_down(y_coordinates):
    # Calculate the average y-coordinate of all fingers except the thumb
    avg_y = sum(y_coordinates) / len(y_coordinates)
    
    # Define a threshold for determining scroll direction
    threshold = 250
    
    # Determine scrolling direction based on the average y-coordinate
    if avg_y < threshold:
        pyautogui.scroll(50)  # Scroll up
    elif avg_y > threshold:
        pyautogui.scroll(-50)  # Scroll down

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
    
    y_coordinates = []  # List to store y-coordinates of all fingers (except thumb)
    
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
                
                if _id != 4:  # Exclude thumb
                    y_coordinates.append(y)  # Store y-coordinate
                    
                landmarkList.append([_id, x, y]) 
            
            # draw Landmarks 
            Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS) 
    
    # If landmarks list is not empty 
    if y_coordinates: 
        # Scroll up or down based on finger positions
        scroll_up_or_down(y_coordinates)
    
    # Display Video and when 'q' is entered, 
    # destroy the window 
    cv2.imshow('Image', frame) 
    if cv2.waitKey(1) & 0xff == ord('q'): 
        break

# Release the camera and close all OpenCV windows
cap.release() 
cv2.destroyAllWindows()
