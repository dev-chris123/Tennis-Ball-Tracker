
import cv2
import numpy as np
import pandas as pd

from court_calibration import calibrate_court, transform_point

VIDEO_PATH = "serve_video.mp4"
CSV_PATH = "tracked_positions.csv"

DEPARTURE_FRAME = 162
LANDING_FRAME = 176

# Read video FPS
video = cv2.VideoCapture(VIDEO_PATH)
fps = video.get(cv2.CAP_PROP_FPS)
video.release()

# Load tracked ball coordinates
data = pd.read_csv(CSV_PATH)

start = data[data["Frame"] == DEPARTURE_FRAME]
end = data[data["Frame"] == LANDING_FRAME]

if start.empty or end.empty:
    raise ValueError("Missing ball coordinates for departure or landing.")

start_pixel = (start.iloc[0]["X"], start.iloc[0]["Y"])
end_pixel = (end.iloc[0]["X"], end.iloc[0]["Y"])

# Calibrate court
result = calibrate_court(VIDEO_PATH)

if result is None:
    raise ValueError("Court calibration failed.")

matrix, image_points = result

# Project both ball positions onto the court plane
start_ground = transform_point(start_pixel, matrix)
end_ground = transform_point(end_pixel, matrix)

# Calculate projected distance in feet
distance_feet = np.linalg.norm(end_ground - start_ground)

# Calculate elapsed time
elapsed_time = (LANDING_FRAME - DEPARTURE_FRAME) / fps

# Calculate projected average speed
speed_fps = distance_feet / elapsed_time
speed_mph = speed_fps * 0.681818

print("\n--- ALPHA SPEED ESTIMATE ---")
print("Flight time:", round(elapsed_time, 3), "seconds")
print("Projected distance:", round(distance_feet, 2), "feet")
print("Projected speed:", round(speed_mph, 2), "mph")
print("WARNING: Ground-plane projection; not validated true ball speed.")
