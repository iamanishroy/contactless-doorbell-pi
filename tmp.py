# Libraries
import RPi.GPIO as GPIO
import time
import requests
import cv2
import base64
from io import BytesIO
import base64
from PIL import Image


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def get_data(self, api):
    response = requests.get(f"{api}")
    if response.status_code == 200:
        print("sucessfully fetched the data")
        self.formatted_print(response.json())
    else:
        print(
            f"Hello person, there's a {response.status_code} error with your request")


def im_2_b64(image):
    img_str = None
    try:
        buff = BytesIO()
        image.save(buff, format="JPEG")
        img_str = base64.b64encode(buff.getvalue())
    except Exception as e:
        print("err", e)

    return img_str


def compressMe(file, verbose=False):

    # Get the path of the file
    # filepath = os.path.join(os.getcwd(),
    #                         file)

    # open the image
    picture = Image.open("/home/pi/code/dp1.png")

    # Save the picture with desired quality
    # To change the quality of image,
    # set the quality variable at
    # your desired level, The more
    # the value of quality variable
    # and lesser the compression
    picture.save("dp2", "PNG", optimize=True, quality=5)
    return


def clickDickPick():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    result, image = cam.read()
    if result:
        print(image)
        print('sending DP')
        # cv2.imwrite("dp.png", image)
        cv2.imwrite("dp1.png", image)

        compressMe(image)
        #img = cv2.imread("/home/pi/code/dp2.png")
        # b64 = im_2_b64(image)
        #im_bytes = image.tobytes()
        # print(im_bytes)
        #im_b64 = base64.b64encode(im_bytes)
        #b64 = base64.b64encode(img)
        # print(b64.decode())
        # print(len(b64.decode()))
        URL_ENDPOINT = 'https://anish.requestcatcher.com/test'
        with open('dp2', 'rb') as f:
            r = requests.post(url=URL_ENDPOINT, files={'dp2': f})
        # data = {'image': im_b64}
        '''params = {'id': b64.decode()}
        # files = {'media': open('dp.png', 'rb')}
        try:
            r = requests.post(url=URL_ENDPOINT, json=params)
            print(r)
        except Exception as e:
            print(e)
        # requests.post(url=URL_ENDPOINT, data=data)
'''
    else:
        print("No image detected. Please! try again")


def alertServer():
    URL_ENDPOINT = 'https://rose-peppered-turner.glitch.me/notify'
    # URL_ENDPOINT = 'https://anish.requestcatcher.com/test'
    PARAMS = {'msg': 'chud gaye'}
    r = requests.get(url=URL_ENDPOINT, params=PARAMS)
    if r.status_code == 201:
        print('clicking DP')
        clickDickPick()


def run():
    try:
        while True:
            dist = distance()
            dist = round(dist, 1)
            if dist < 50.0:
                alertServer()
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


if __name__ == '__main__':
    run()
