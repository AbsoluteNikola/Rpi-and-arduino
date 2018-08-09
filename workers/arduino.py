import serial
import sys
import json
import time


SENSORS_NUMBER = 7


class ArduinoConn:

    def __init__(self, tty: str):
        if not tty.startswith('/dev/ttyACM'):
            raise ValueError('tty must be like /dev/tty/ACM0')
        self.s = serial.Serial(tty)
        self.data = b''
        self.byte = b''

    def hash_msg(self):
        _hash = 0
        num = 23
        mod = 10**9 + 7
        _hash = self.data[0] * num
        for i in range(1, len(self.data)):
            num = (num * 23) % mod
            _hash = (_hash + num * self.data[i]) % mod
        return _hash

    def recv_msg(self) -> str:
        ack = False
        # data\00hash -> A ? R
        while not ack:
            self.byte = b''
            self.data = b''
            while self.byte != b'\x00':
                self.data += self.byte
                self.byte = self.s.read(1)
            _hash = int.from_bytes(self.s.read(4), 'little')
            ack = (_hash == self.hash_msg())

            # print('msg:', self.data, _hash, self.hash_msg())
            if ack:
                self.s.write(b'A')
            else:
                self.s.write(b'R')
        return self.data.decode()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('run program with usb tty in args ("/dev/ttyACM0")')
        exit(1)

    arduino = ArduinoConn(sys.argv[1])
    arduino.s.write(b'A')
    while True:
        results = {}
        for i in range(SENSORS_NUMBER):
            msg = arduino.recv_msg()
            sensor, val = msg.split(':', maxsplit=1)
            results[sensor] = float(val)
        print(results)
