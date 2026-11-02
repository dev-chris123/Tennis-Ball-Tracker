import cv2
# Imports OpenCV for image processing
import numpy as np
# Imports NumPy for numerical operations and coordinate arrays

from get_points import get_points
# Imports the function responsible for collecting court reference points

real_points = np.array([
    [0, 0],
    [13.5, 0],
    [13.5, 21],
    [0, 21]
], dtype=np.float32)
# Establishes real-world points representing the four corners of selected service boxes
def calibrate_court(video_path):
    image_points = get_points(video_path)
    # Calls the get_points function and stores returned coordinates
    if image_points is None:
        return None
    # None is returned if no valid selection is provided
    image_points = np.array(image_points, dtype=np.float32)
    # Converts image_points into a NumPy array
    matrix = cv2.getPerspectiveTransform(image_points, real_points)
    # Calculates a 3x3 matrix that maps four source points to their corresponding destination points
    return matrix, image_points
    # Returns the 3x3 matrix and the selected points

def transform_point(point, matrix):
    point = np.array([[point]], dtype=np.float32)
    # Converts the coordinate into a NumPy array
    transformed_point = cv2.perspectiveTransform(point, matrix)
    # Converts pixel coordinates into court-plane coordinates
    return transformed_point[0][0]
    # Returns the transformed coordinate

def test_calibration(image_points, matrix):
    test_points = np.array(image_points, dtype=np.float32).reshape(-1, 1, 2)
    # The four test points are formatted as a NumPy array
    transformed_points = cv2.perspectiveTransform(test_points, matrix)
    # Transforms original pixel court coordinates and coverts them to real-world court coordinates in feet
    print("Expected coordinates:")
    print(real_points)
    # Prints the real-world court coordinates
    print("\nTransformed coordinates:")
    print(transformed_points.reshape(-1, 2))
    # Prints the transformed coordinate points
def test_additional_point(matrix, image_point, expected_point):
    transformed_point = transform_point(image_point, matrix)
    # Converts one pixel coordinate into its corresponding court coordinate
    print("Expected position:", expected_point)
    print("Actual position:", transformed_point)
    # Print the expected real-world coordinate and the transformed coordinate from footage
    error = np.linalg.norm(
        transformed_point - np.array(expected_point)
    )
    # Calculates the distance between the transformed point and the expected point
    print("Position error:", error, "feet")
    # Prints the error amount in feet
if __name__ == "__main__":
    video_path = "serve_video.mp4"
    result = calibrate_court(video_path)

    if result is not None:
        matrix, image_points = result

        test_calibration(image_points, matrix)

        test_additional_point(
            matrix,
            (910, 661),
            (6.75, 10.5)
        )