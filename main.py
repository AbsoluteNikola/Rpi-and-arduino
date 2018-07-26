import sys
from hardware import ArduinoConn


class DataServer():

    def __init__(self):
        self.arduino = ArduinoConn(sys.argv[1])


if __name__ == '__main__':
    print('start serving...')
    serve()