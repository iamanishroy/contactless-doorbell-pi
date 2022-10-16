import cv2


def capture():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    result, image = cam.read()
    if result:
        return image
    return False
