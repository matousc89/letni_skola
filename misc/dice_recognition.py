import numpy as np
import cv2
import sys
import uuid
import os
from sklearn.neighbors import KNeighborsClassifier
import mahotas


def main(argv):
    neighbours_classifier = KNeighborsClassifier(n_neighbors=6)
    training_done = False
    saving_commands = [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6")]
    dices_intensity = np.zeros(6)
    calibration_number = 1
    cap = cv2.VideoCapture(0)
    print(argv)
    # ziskani pozadi
    print('Ziskej pozadi a stiskni q')
    image_background = cv2.imread(os.path.join('data', 'background.jpg'), cv2.IMREAD_GRAYSCALE)
    dot_template = cv2.imread(os.path.join('data', 'template', 'dot_template.jpg'), cv2.IMREAD_GRAYSCALE)
    w, h = dot_template.shape[::-1]
    while True:
        ret, image = cap.read()
        cv2.imshow('Preprocessed image', image)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_inverted = cv2.bitwise_not(image_gray)
        image_sub = cv2.subtract(image_inverted, image_background)
        image_sub[image_sub < 110] = 0
        retval, image_thresholded = cv2.threshold(image_sub, 255, 255, cv2.THRESH_BINARY)
        cv2.imshow('Substracted image', image_sub)
        pressed_key = cv2.waitKey(10) & 0xFF
        if pressed_key == ord('b'):
            background = image_inverted
            cv2.imwrite(os.path.join('data', 'background.jpg'), background)

        elif pressed_key == ord('x'):
            print(image_sub)
            break

        elif pressed_key in saving_commands:
            cv2.imwrite(os.path.join('data', 'images', chr(pressed_key), str(uuid.uuid4())) + ".jpg", image_sub)
            print("image of {dice_number} registered".format(dice_number=chr(pressed_key)))

        elif pressed_key == ord('t'):
            # classifier training
            train_data = []
            train_labels = []
            # prepare training data
            for subdir, dirs, files in os.walk("./data/images"):
                for file in files:
                    filepath = subdir + os.sep + file
                    normalized_path = os.path.normpath(filepath)
                    path_components = normalized_path.split(os.sep)
                    print(path_components)
                    train_image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                    feature_hu = cv2.HuMoments(cv2.moments(train_image)).flatten()
                    feature_haralick = mahotas.features.haralick(train_image).mean(axis=0)
                    train_data.append(np.hstack([feature_hu, feature_haralick]))
                    train_labels.append(str(path_components[2]))
            train_labels_arr = np.asarray(train_labels)
            train_data_arr = np.asarray(train_data)
            print(train_data_arr.shape)
            neighbours_classifier.fit(train_data_arr, train_labels_arr)
            training_done = True


        elif pressed_key == ord('c'):
            # classify image
            hu = cv2.HuMoments(cv2.moments(image_sub)).flatten()
            haralick = mahotas.features.haralick(image_sub).mean(axis=0)
            global_feature = np.hstack([hu, haralick])

            print(neighbours_classifier.predict(global_feature.reshape(1, -1)))


        elif pressed_key == ord('p'):
            # template matching
            templates_number = 0
            res = cv2.matchTemplate(image_sub, dot_template, cv2.TM_CCOEFF_NORMED)
            np.savetxt('template_result.txt', res)
            threshold = 0.5
            loc = np.where(res >= threshold)
            loc_filter = [0, 0]
            for pt in zip(*loc[::-1]):
                # print(abs(pt[0] - loc_filter[0]), abs(pt[1] - loc_filter[1]))
                if abs(pt[0] - loc_filter[0]) > 12 and abs(pt[1] - loc_filter[1]) > 12:
                    templates_number += 1
                    cv2.rectangle(image_sub, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
                    loc_filter[0] = pt[0]
                    loc_filter[1] = pt[1]

            pass
            print(str(templates_number))
            cv2.imshow('Template result', image_sub)


        elif pressed_key == ord('k'):
            contours, hierarchy = cv2.findContours(image_sub, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(image_sub, contours, -1, (255, 0, 0), 2)

            # print(contours)
            dice_number = 0
            c = max(contours, key=cv2.contourArea)
            for contour in contours:

                if cv2.contourArea(contour) > 100:
                    # contours_to_draw.append(contour)
                    dice_number += 1
                    # cv2.drawContours(image_sub, contours, k, (255, 0, 0), 2)
                    cv2.drawContours(image_sub, [contour], 0, (255, 0, 0), 2)

            cv2.imshow('Contours result', image_sub)
            print("dice number: ", dice_number)


if __name__ == '__main__':
    main(sys.argv)

