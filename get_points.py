import cv2
# Imports OpenCV for image processing software

def get_points(video_path):
    """
       Opens the first frame of a video and allows the user
       to select four court reference points.

       Args:
           video_path: Path to the video file.

       Returns:
           List of four (x, y) pixel coordinates,
           or None if selection fails or is cancelled.
       """
    capture = cv2.VideoCapture(video_path)
    # Initializes the OpenCV video capture object and opens the video file
    if not capture.isOpened():
        print("Error: Unable to open video.")
        return None
    # Checks if the video was successfully opened
    ret, frame = capture.read()
    # The first frame of the video is taken
    capture.release()

    if not ret:
        print("Error: Unable to read video.")
        return None
    # Checks if video was successfully read
    original_frame = frame.copy()
    # Creates an independent copy of the original frame object
    points = []
    # Creates a list for coordinate points to be stored in

    window_name = "Select Court Reference Points"

    def update_display():
        display = original_frame.copy()
        # Creates a copy of the original video frame
        for i, (x, y) in enumerate(points):
            cv2.circle(display, (x, y), 7, (0, 0, 255), -1)
        # Iterates through a list of selected points, and takes x and y values
            cv2.putText(
                display,
                str(i + 1),
                (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
        # Method that creates a number next to each selected point
        cv2.imshow(window_name, display)
        # Method displays the modified image in OpenCV window
    def click_event(event, x, y, flags, params):
        # 	Callback function triggered by mouse events
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) < 4:
                points.append((x, y))
                # If the amount of points selected is less than 4, the  coordinates will be appended to points
                print(f"Point {len(points)}: ({x}, {y})")
                update_display()
                #Prints the points then calls update_display function
            else:
                print("Four points already selected. Press R to reset.")
                # If more than 4 points are selected, console prompts the user to reset
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, click_event)
    # Registers the mouse callback function to the specified window
    # Function executes when a mouse event occurs
    print("\nSelect four court-line intersections:")
    print("1. Near-left corner")
    print("2. Near-right corner")
    print("3. Far-right corner")
    print("4. Far-left corner")
    print("\nIMPORTANT:")
    print("- Select intersections defining a known court region.")
    print("- All four points must lie on the court surface.")
    print("- Click approximately at the center of each intersection.")
    print("- Follow the specified order.")
    # Instructions ensure that the points of the court match real-world measurements
    print("\nControls:")
    print("U = Undo last point")
    print("R = Reset all points")
    print("ENTER = Confirm")
    print("ESC = Cancel")
    # Instructions for user interface
    update_display()
    #Calls the update display function
    while True:
    #Runs a while loop that checks for key input
        key = cv2.waitKey(20) & 0xFF
        # Waits up to 20 milliseconds for keyboard input and uses a bitwise AND operation
        # Extracts the lowest 8 bits of the returned key code.
        if key == ord('u'):

            if points:
                removed = points.pop()
                print(f"Removed: {removed}")
                update_display()
        # If the user inputs "u", the last element of the list is removed
        # The screen is then updated
        elif key == ord('r'):

            points.clear()
            print("Points reset.")
            update_display()
        # If "r" is inputted, all items in points are cleared
        # The screen is then updated
        elif key == 13:

            if len(points) == 4 and len(set(points)) == 4:
                break
                # If there are 4 points selected, the loop will break
            elif len(set(points)) != len(points):
                print("Duplicate points detected. Please reset or undo.")
                # Checks for duplicate points by checking for unique elements
            else:
                print(f"Select {4 - len(points)} more points.")
                # If the enter key is pressed, the program will ask to select remaining points
        elif key == 27:

            points.clear()
            break
        # When the escape key is pressed, the list of points is cleared and the loop breaks
    cv2.destroyAllWindows()
    # \Closes all OpenCV windows created by the program

    if len(points) != 4:
        print("Point selection cancelled.")
        return None
        # If the amount of points selected doesn't equal 4, the console prints a string
    print("\nFinal court coordinates:")
    print(points)
    # Prints the coordinates in the console
    return points
    # The list of points is returned
#court_points = get_points("serve_video.mp4")
# Court coordinates are taken from the video file in the parameter