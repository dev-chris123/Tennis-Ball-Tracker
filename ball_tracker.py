import cv2
# Imports OpenCV for image processing
import os
print("CSV save location:", os.getcwd())
import numpy as np
# Imports NumPy for numerical operations and arrays
from speed_calculation import calculate_speed
import csv
def detect_ball(frame, previous_frame):
    # Detects potential tennis ball locations in an individual frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Converts the frame from BGR to HSV color space

    lower_yellow = np.array([22, 100, 120])
    upper_yellow = np.array([38, 255, 255])
    # Establishes the HSV boundaries for the tennis ball

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # Creates a binary mask identifying matching yellow pixels
    # Calculates the difference between the current and previous frame
    difference = cv2.absdiff(frame, previous_frame)

    # Converts the difference image to grayscale
    gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    # Identifies pixels that have changed
    _, movement_mask = cv2.threshold(
        gray_difference, 15, 255, cv2.THRESH_BINARY
    )

    # Combines yellow detection with movement detection
    # mask = cv2.bitwise_and(mask, movement_mask)
    cv2.imshow("Yellow Mask", mask)

    contours, hierarchy = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # Identifies separate objects within the binary mask
    print("Total contours:", len(contours))
    filtered_contours = []

    for contour in contours:
        area = cv2.contourArea(contour)
        # Calculates the contour's area

        x, y, w, h = cv2.boundingRect(contour)
        # Finds the bounding rectangle
        # print("Area:", area, "X:", x)

        if 20 < area < 500:
            filtered_contours.append(contour)
    return filtered_contours, mask
    # Returns the filtered contours and binary mask


video_path = "serve_video.mp4"
# Establishes the video file path

capture = cv2.VideoCapture(video_path)
fps = capture.get(cv2.CAP_PROP_FPS)
print("Video FPS:", fps)
print("Frame count:", capture.get(cv2.CAP_PROP_FRAME_COUNT))

duration = capture.get(cv2.CAP_PROP_FRAME_COUNT) / fps
print("Video duration:", duration, "seconds")
# Opens the video file
ret, previous_frame = capture.read()
frame_index = 0
previous_position = None
# Stores the ball's previous position

tracked_positions = []
# Stores the ball's coordinates throughout the video

missing_frames = 0
# Counts consecutive frames where the ball isn't detected

max_missing_frames = 5
# Allows the ball to disappear for up to five frames
frame_index = 0
while capture.isOpened():
    ret, frame = capture.read()
    # Reads the next video frame
    frame_index += 1
    if not ret:
        break
        # Exits when the video ends

    contours, mask = detect_ball(frame, previous_frame)
    # Detects potential tennis ball locations

    output = frame.copy()
    # Creates a copy for displaying detections

    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        center_x = x + w // 2
        center_y = y + h // 2

        candidates.append((center_x, center_y))

        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(output, (center_x, center_y), 4, (255, 0, 0), -1)

    print("Candidates:", candidates)


    if candidates:

        if previous_position is None:
            ball_position = candidates[0]

        else:
            distances = [
                np.linalg.norm(
                    np.array(candidate) - np.array(previous_position)
                )
                for candidate in candidates
            ]

            closest_index = np.argmin(distances)
            ball_position = candidates[closest_index]

        previous_position = ball_position
        tracked_positions.append((frame_index, ball_position))

        missing_frames = 0

        cv2.circle(output, ball_position, 5, (0, 0, 255), -1)

    else:
        missing_frames += 1

        if missing_frames > max_missing_frames:
            previous_position = None
    previous_frame = frame.copy()
    cv2.imshow("Ball Tracking", output)
    # Displays the processed video

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        # Press Q to exit
print("Tracked positions:")
for frame_number, position in tracked_positions:
    print(frame_number, position)
with open("tracked_positions.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Frame", "X", "Y"])

    for frame_number, position in tracked_positions:
        writer.writerow([frame_number, position[0], position[1]])
start_frame = 165
end_frame = 170

serve_positions = [
    (frame, position)
    for frame, position in tracked_positions
    if start_frame <= frame <= end_frame
]

if len(serve_positions) >= 2:
    first_frame, first_position = serve_positions[0]
    last_frame, last_position = serve_positions[-1]

    frame_difference = last_frame - first_frame

    speed = calculate_speed(
        first_position,
        last_position,
        fps,
        frame_difference
    )

    print("Serve speed:", round(speed, 2), "pixels/second")
else:
    print("Not enough detections during serve.")
capture.release()
# Releases the video capture object

cv2.destroyAllWindows()
# Closes all OpenCV windows
