import cv2


# image acquisition and processing
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # opens camera stream

while True:  # press q to quit
    pressed_key = cv2.waitKey(10) & 0xFF  # read keyboard input
    image_background = cv2.imread("image_background.jpg", cv2.IMREAD_GRAYSCALE)  # read gray scale background
    ret, image = camera.read()  # get camera image
    cv2.imshow("Raw image", image)  # show image
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert image to gray scale
    cv2.imshow("Gray scale image", image_gray)  # show gray scale image
    image_inverted = cv2.bitwise_not(image_gray)  # invert image
    cv2.imshow("Inverted image", image_inverted)  # show inverted image
    image_subtracted = cv2.subtract(image_inverted, image_background)  # image subtracting
    cv2.imshow("Substracted image", image_subtracted)  # show subtracted image
    ret, image_threshold = cv2.threshold(image_subtracted, 110, 255, cv2.THRESH_BINARY)  # image threshold
    cv2.imshow("Thresholded image", image_threshold)  # show threshold image
    contours, hierarchy = cv2.findContours(image_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours

    for contour in contours:
        contour_area = cv2.contourArea(contour)  # estimate contour area
        if contour_area > 100:
            cv2.drawContours(image, [contour], 0, (0, 255, 0), 3)  # draw contour into color image
    cv2.imshow("Image with contours", image)  # show original image with desired contours

    if pressed_key == ord("b"):  # get background for subtraction
        cv2.imwrite("image_background.jpg", image_inverted)  # save new background image
        print("new background obtained")  # print message

    elif pressed_key == ord("q"):  # quit
        print("terminating....")  # print message
        camera.release()  # stop camera stream
        cv2.destroyAllWindows()  # close all windows correctly
        break
