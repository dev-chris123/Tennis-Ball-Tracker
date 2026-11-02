import numpy as np

def calculate_speed(position1, position2, fps, frame_difference):
    # Calculates pixel displacement
    distance_pixels = np.linalg.norm(
        np.array(position2) - np.array(position1)
    )

    # Calculates elapsed time
    elapsed_time = frame_difference / fps

    # Calculates image-plane speed
    speed_pixels_per_second = distance_pixels / elapsed_time

    return speed_pixels_per_second
