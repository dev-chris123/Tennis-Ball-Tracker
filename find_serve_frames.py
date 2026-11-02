import cv2

video = cv2.VideoCapture("serve_video.mp4")

fps = video.get(cv2.CAP_PROP_FPS)
frame_number = 160

mouse_x, mouse_y = 0, 0

def show_coordinates(event, x, y, flags, param):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

cv2.namedWindow("Find Serve Frames")
cv2.setMouseCallback("Find Serve Frames", show_coordinates)

while True:
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = video.read()

    if not success:
        break

    display = frame.copy()

    cv2.putText(
        display,
        f"Frame: {frame_number} | Time: {frame_number / fps:.3f}s",
        (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
    )

    cv2.putText(
        display,
        f"Mouse: ({mouse_x}, {mouse_y})",
        (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
    )

    cv2.imshow("Find Serve Frames", display)

    key = cv2.waitKey(30) & 0xFF

    if key == ord("d"):
        frame_number += 1
    elif key == ord("a"):
        frame_number = max(0, frame_number - 1)
    elif key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()