import cv2
import numpy as np


# Drawing Shapes

def ImageProcessing():
    image = np.zeros((512, 512, 3), np.uint8)

    # cv2.line(image, (20, 200), (200, 20), (0, 0, 255), 5)
    cv2.rectangle(image, (250, 110), (70, 210), (170, 2, 2), 3)
    cv2.circle(image, (140, 120), 40, (140, 200, 160), 4)

    cv2.imshow('Black Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


ImageProcessing()