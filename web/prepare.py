"""
disable all used pins on raspberry starts with Pi startup
"""

from RPi import GPIO
from web import Sync, pins

with Sync('pins') as sync:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([pin for _, pin in pins.items()], GPIO.OUT, initial=GPIO.LOW)
