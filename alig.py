import cv2

face_detection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def haar(img):
    faces = face_detection.detectMultiScale(img)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return img
def stand_img(img):
    img = cv2.resize(img,(600,400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
def function_2(img1):
    img1 = cv2.resize(img1,(600,400))
    img1 = haar(img1)
    img1 = stand_img(img1)
    return img1


