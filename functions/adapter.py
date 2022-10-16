import requests
import json

SERVER_ENDPOINT = 'https://contactless-doorbell-api.glitch.me'


class Adapter:

    def __init__(self):
        self.SERVER_ENDPOINT = SERVER_ENDPOINT
        if not self.ping():
            raise Exception(
                "Sorry, device connection cannot reach to the server...")

    def ping(self):
        response = requests.request("GET", self.url('/ping'))
        return response.text == 'pong'

    def url(self, route):
        return self.SERVER_ENDPOINT + route

    def sendNotification(self, arrived, id):
        payload = json.dumps({
            "msg": "Someone Arrived" if arrived else "Someone Left",
            "id": id
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST",
            self.url('/notify'),
            headers=headers,
            data=payload
        )

        print(payload, '\n', response.text)

    def sendImage(self, image, _id):
        payload = {}
        files = [
            ('file', ('image.png', image, 'image/png'))
        ]
        headers = {}

        response = requests.request(
            "POST", self.url('/upload-image/' + _id), headers=headers, data=payload, files=files)

        print(response.text)


def test():
    a = Adapter()
    a.sendNotification(True)
    a.sendNotification(False)
    import uuid
    _id = str(uuid.uuid1())

    print(_id)
    a.sendImage(open('op.png', 'rb'), _id)


if __name__ == '__main__':
    print('running tests...')
    test()
