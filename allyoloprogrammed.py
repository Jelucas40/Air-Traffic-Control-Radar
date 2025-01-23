import cv2
import torch

# Load the YOLOv5 model (can be yolov5s, yolov5m, or your custom trained model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # You can change yolov5s to yolov5m or yolov5l if needed

# Initialize the webcam (0 is usually the default webcam, adjust if necessary)
cap = cv2.VideoCapture(0)

# Set the frame width and height (optional, you can change these)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

while True:
    # Read the frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Perform object detection with YOLOv5
    results = model(frame)  # Pass the frame to YOLOv5 model for detection

    # Render the results
    frame_with_boxes = results.render()[0]

    # Display the frame with detections in a popup window
    cv2.imshow("YOLOv5 Detection", frame_with_boxes)

    # Wait for key press, if 'q' is pressed, close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

