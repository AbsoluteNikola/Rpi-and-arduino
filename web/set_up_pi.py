from Rpi import GPIO


pins = [3, 5]


def set_up():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)