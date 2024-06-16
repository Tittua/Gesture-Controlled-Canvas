import cv2
import numpy as np
from hand_tracking import capture_hand, hand_callback
import gemini
import pyautogui

def main():
    # Capture video from webcam
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = pyautogui.size()
    # Set camera resolution to match screen resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

    # Create a named window
    cv2.namedWindow('Live Drawing', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Live Drawing', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Initialize a canvas for drawing
    canvas = None

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        image = frame
        image_height, image_width, _depth = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output_hands = capture_hand.process(rgb_image)
        all_hands = output_hands.multi_hand_landmarks
        if all_hands:
            for hand in all_hands:
                hand_callback(hand.landmark, image_width, image_height, canvas)

        # Initialize the canvas to be the same size as the frame
        if canvas is None:
            canvas = np.zeros_like(frame) * 255

        # Combine the frame and canvas
        combined_frame = cv2.addWeighted(frame, 1, canvas, 1, 0)

        # Display the combined frame
        cv2.imshow("Live Drawing", combined_frame)

        key = cv2.waitKey(1)
        if key == 27:  # Press 'ESC' to exit
            break
        elif key == ord('r'):  # Press 'r' to reset the drawing
            canvas = np.zeros_like(frame) * 255  # Reset the canvas
        elif key == ord('k'):
            cv2.imwrite('canvas.png', canvas)
            text_response = gemini.file_upload('canvas.png')
            print(text_response)
            cv2.putText(canvas, text_response, (35, 35), fontScale=1, color=(0, 128, 0), thickness=2, fontFace=cv2.FONT_HERSHEY_DUPLEX)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
