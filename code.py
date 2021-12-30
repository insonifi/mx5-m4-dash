
from adafruit_is31fl3731.matrix_11x7 import Matrix11x7
import board
import busio
from light import LightSensor
from math import log
from random import randint
from render import RenderNum
import time

light = LightSensor(board.A0)
i2c = busio.I2C(board.SCL, board.SDA)
disp_right = Matrix11x7(i2c)
disp_left = Matrix11x7(i2c, address=0x77)
ctrl_right = RenderNum(disp_right)
ctrl_left = RenderNum(disp_left)

ctrls = [ctrl_left, ctrl_right]

for ctrl in ctrls:
    ctrl.brightness = 2
    ctrl.offset(0, 1)

i = 0
while True:
    t = time.monotonic_ns()
    l = light.get_avg()
    ctrl_left.render(int(t / 10 ** 8 % 10 ** 3), want_zeros=True)
    ctrl_right.render(l)

    i = (i + 1) % 5

    if i == 0:
        ctrl_left.set_brightness(l)

    time.sleep(0.02)

