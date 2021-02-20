
import cv2
import numpy as np
from tensorflow.keras.models import load_model

def preprocess(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_thres = cv2.Canny(img_gray, 60, 180)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_thres = cv2.adaptiveThreshold(img_blur, 255, 1, 1, 11, 2)
    return img_thres

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area

def reorder(points):
    points = points.reshape((4, 2))
    points_new = np.zeros((4, 1, 2), np.int32)
    add = points.sum(1)
    points_new[0] = points[np.argmin(add)]
    points_new[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    points_new[1] = points[np.argmin(diff)]
    points_new[2] = points[np.argmax(diff)]
    return points_new

def split_boxes(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes

def initialize_model():
    model = load_model("myModel.h5")
    return model

def get_prediction(boxes, model):
    result = []
    for image in boxes:
        img = np.asarray(image)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        predictions = model.predict(img)
        class_index = np.argmax(predictions, axis=-1)
        probability = np.amax(predictions)
        if probability > 0.8:
            result.append(class_index[0])
        else:
            result.append(0)
    return result

def display_numbers(img, numbers, color=(255, 0, 255)):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for x in range(0, 9):
        for y in range(0, 9):
            if numbers[(y * 9) + x] != 0:
                cv2.putText(img, str(numbers[(y * 9) + x]),
                            (x * secW + int(secW / 2) - 10, int((y + 0.8) * secH)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            2, color, 2, cv2.LINE_AA)
    return img