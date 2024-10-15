import cv2
import numpy as np

# Open the regular visible camera (Integrated Camera)
camera = cv2.VideoCapture('/dev/video2')  # Adjust if needed to /dev/video3

# Open the infrared camera (Integrated IR Camera)
ir_sensor = cv2.VideoCapture('/dev/video0')  # Adjust if needed to /dev/video1

# Check if both devices opened successfully
if not camera.isOpened():
    print("Error: Could not open regular camera.")
    exit()

if not ir_sensor.isOpened():
    print("Error: Could not open infrared camera.")
    exit()

while True:
    # Capture frame-by-frame from the regular camera
    ret, frame = camera.read()
    if not ret:
        print("Error: Failed to capture frame from regular camera.")
        break

    # Capture frame-by-frame from the IR sensor
    ret_ir, ir_frame = ir_sensor.read()
    if not ret_ir:
        print("Error: Failed to capture frame from infrared camera.")
        break

    # Combine the regular and IR images (simple overlay technique)
    # Convert the IR frame to 3-channel (RGB) if it is grayscale
    if len(ir_frame.shape) == 2:  # If IR frame is grayscale
        ir_frame = cv2.cvtColor(ir_frame, cv2.COLOR_GRAY2BGR)

    # Optionally, adjust brightness/contrast of IR to blend it better with visible frame
    ir_frame = cv2.convertScaleAbs(ir_frame, alpha=1.0, beta=50)  # Adjust the brightness of IR

    # Combine the frames: you can tweak the weights as needed
    combined_frame = cv2.addWeighted(frame, 0.7, ir_frame, 0.3, 0)

    # Show the combined video
    cv2.imshow("Night Vision", combined_frame)

    # Break on pressing 'q' or closing the window
    if cv2.waitKey(1) & 0xFF == ord('q') or not cv2.getWindowProperty("Night Vision", cv2.WND_PROP_VISIBLE):
        break

# Release the video capture objects and close the display window
camera.release()
ir_sensor.release()
cv2.destroyAllWindows()

