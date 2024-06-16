import cv2
import numpy as np
import pyautogui
import mediapipe as mp
import math
import gemini


capture_hand = mp.solutions.hands.Hands(max_num_hands=1)
drawing_option = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()


import textwrap

def draw_text(canvas, text, position, fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale=1, color=(0, 128, 0), thickness=2, line_height=30, max_width=50):

    x, y = position

    # Wrap the text into lines
    wrapped_text = textwrap.wrap(text, width=15)

    # Draw each line on the canvas
    for line in wrapped_text:
        cv2.putText(canvas, line, (x, y), fontFace, font_scale, color, thickness)
        y += line_height  # Move to the next line


drawing = False
ix, iy = -1, -1





def draw_freehand(x, y, canvas,color,thickness):
    global ix, iy, drawing

    if drawing:  # If drawing is active
        cv2.line(canvas, (ix, iy), (x, y), color=color, thickness=thickness)
    ix, iy = x, y

def hand_callback(hand_landmarks, image_width, image_height, canvas):
    global drawing, ix, iy

    x1 = y1 = x2 = y2 = x3 = y3 = 0

    for id, lm in enumerate(hand_landmarks):
        x = int(lm.x * image_width)
        y = int(lm.y * image_height)
        #For mouse cordiates and canvas reset
        if id == 8:
            x1 = x
            y1 = y
        #for mouse down action    
        if id == 4:
            x2 = x
            y2 = y
        #For mouse down action    
        if id == 10:
            x3 = x
            y3 = y
        #For resetting the canvas    
        if id == 12:
            x4 = x
            y4 = y
        if id == 20:
            x5=x
            y5=y
        if id == 16:
            x6=x
            y6=y

    distance_draw = math.dist((x2, y2), (x3, y3))
    canvas_reset=math.dist((x1, y1), (x5, y5))
    trigger_gemini_1=math.dist((x6, y6), (x2, y2))
    trigger_gemini_2=math.dist((x1, y1), (x4, y4))
    erase_trigger_1=math.dist((x2, y2), (x5, y5))
    #calling the loop for drawing 
    if distance_draw < 30:
        if not drawing:
            drawing = True
            ix, iy = x1, y1  # Reset the starting position
        draw_freehand(x1, y1, canvas,color=(0, 0, 255),thickness=6)
    else:
        drawing = False

    
   


    if canvas_reset<15:
        canvas[:,:]=0
        print('canvas reset')
        #cv2.putText(canvas,str(trigger_gemini),(50,50),fontScale=1,thickness=2,color=(0, 128, 0),fontFace=cv2.FONT_HERSHEY_DUPLEX)
    if trigger_gemini_1<15 and trigger_gemini_2<15:
        cv2.imwrite('canvas.png', canvas)
        text_response = gemini.file_upload('canvas.png')
        print(text_response)
        draw_text(canvas, text_response, (35, 35), color=(0, 128, 0), thickness=2, fontFace=cv2.FONT_HERSHEY_DUPLEX)
