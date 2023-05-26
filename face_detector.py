import cv2
from djitellopy import Tello

# Tracker Types
# tracker = cv2.TrackerBoosting_create()
# tracker = cv2.TrackerMIL_create()
# tracker = cv2.TrackerKCF_create()
# tracker = cv2.TrackerTLD_create()
# tracker = cv2.TrackerMedianFlow_create()
# tracker = cv2.TrackerCSRT_create()
tracker = cv2.TrackerKCF_create()

# Initialize Tello
tello = Tello()

# Connect to Tello
tello.connect()

# Start video stream
tello.streamon()

# Create an OpenCV window
cv2.namedWindow("Tracking")

# Select object to track
frame = tello.get_frame_read().frame
bbox = cv2.selectROI("Tracking", frame, False)
tracker.init(frame, bbox)

# Main loop
while True:
    # Read frame from video stream
    frame = tello.get_frame_read().frame

    # Update tracker
    success, bbox = tracker.update(frame)

    if success:
        

        # Draw bounding box
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 3)

        # Calculate center of the bounding box
        center_x = x + w // 2
        center_y = y + h // 2

        # Move the drone based on the center position
        # You'll need to adjust these values according to your specific drone and requirements
        if center_x < frame.shape[1] // 2 - 20:
            tello.move_left(20)
        elif center_x > frame.shape[1] // 2 + 20:
            tello.move_right(20)
        
        if center_y < frame.shape[0] // 2 - 20:
            tello.move_up(20)
        elif center_y > frame.shape[0] // 2 + 20:
            tello.move_down(20)

    # Display frame
    cv2.imshow("Tracking", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Disconnect from Tello
#tello.streamoff()
tello.disconnect()

# Close OpenCV windows
cv2.destroyAllWindows()