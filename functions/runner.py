import uuid
from functions.adapter import Adapter
from functions.helpers.capture import capture
from functions.helpers.distance import distance


class Runner(Adapter):
    def __init__(self, range=50) -> None:
        Adapter.__init__(self)
        self.range = range
        self.run()
        pass

    def run(self):
        while True:
            inRange = self.check()
            if inRange:
                self.handleInRange()
                break

    def check(self):
        d = distance()
        return d < self.range

    def handleInRange(self):
        if(self.check()):
            _id = str(uuid.uuid1())
            self.sendNotification(arrived=True, id=_id)
            image = capture()
            if image:
                self.sendImage(image=image, id=_id)
            while True:
                if not self.check():
                    self.sendNotification(arrived=False, id=_id)
                    break
            self.run()
        else:
            self.run()

            # notify
            # check if out of range
            # then switch again and send out message


def test():
    Runner()


if __name__ == '__main__':
    print('running tests...')
    test()
