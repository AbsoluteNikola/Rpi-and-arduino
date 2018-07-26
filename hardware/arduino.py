import serial
import sys
import json
import time


SENSORS_NUMBER = 3


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
            print(_hash)
            num = (num * 23) % mod
            _hash = (_hash + num * self.data[i]) % mod
        return _hash

    def recv_msg(self) -> str:
        ack = False
        while not ack:
            self.byte = b''
            self.data = b''
            while self.byte != b'\x00':
                self.data += self.byte
                self.byte = self.s.read(1)
                print(self.byte, end='')
            print(self.data)

            _hash = int.from_bytes(self.s.read(4), 'little')
            ack = (_hash == self.hash_msg())

            print('msg:', self.data, _hash, self.hash_msg(data))
            if ack:
                self.s.write('A')
            else:
                self.s.write('R')
        return self.data.decode()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('run program with usb tty in args ("/dev/ttyACM0")')
        exit(1)

    arduino = ArduinoConn(sys.argv[1])
    while True:
        results = {}
        for i in range(SENSORS_NUMBER):
            msg = arduino.recv_msg()
            sensor, val = msg.split(':', maxsplit=1)
            results[sensor] = float(val)
        print(results)
