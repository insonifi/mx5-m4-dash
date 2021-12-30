from render import RenderNum
import time
from adafruit_is31fl3731.matrix_11x7 import Matrix11x7
import board
import busio
from random import randint, choice

i2c = busio.I2C(board.SCL, board.SDA)
display0 = Matrix11x7(i2c)
display1 = Matrix11x7(i2c, address=0x77)
rn0 = RenderNum(display0)
rn1 = RenderNum(display1)

rns = [rn0, rn1]

for rn in rns:
    rn.brightness = 0
    rn.offset(0, 1)

while True:
    rn0.render(time.localtime().tm_sec)
    rn1.render(60 - time.localtime().tm_sec)

    if rn0.brightness < 4:
        for rn in rns:
            rn.chg_brightness(1)

    time.sleep(0.1)

