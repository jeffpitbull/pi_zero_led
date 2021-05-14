import time
from math import atan2, degrees
import board
import busio
import adafruit_mpu6050

from adafruit_is31fl3731.charlie_bonnet import CharlieBonnet as Display


gyroi2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_mpu6050.MPU6050(gyroi2c)

ledi2c = busio.I2C(board.SCL, board.SDA)

display = Display(ledi2c)

display.fill(0)


# Given a point (x, y) return the angle of that point relative to x axis.
# Returns: angle in degrees


def vector_2_degrees(x, y):

    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle


# Given an accelerometer sensor object return the inclination angles of X/Z and Y/Z
# Returns: tuple containing the two angles in degrees


def get_inclination(_sensor):
    x, y, z = _sensor.acceleration
    return vector_2_degrees(x, z), vector_2_degrees(y, z)

def remap(value, min=0, max=180, new_min = 0, new_max = 7):
    int_value = int(value)
    return int((((int_value - min) * (new_max - new_min)) / (max - min)) + new_min)


iterations = 0
while iterations < 250:
    angle_xz, angle_yz = get_inclination(sensor)
    xz_pixel = remap(angle_xz, new_max=15)
    yz_pixel = remap(angle_yz)
    display.fill(0)
    display.pixel(xz_pixel, yz_pixel, 50)
    print("XZ angle = {:6.2f}deg   YZ angle = {:6.2f}deg".format(angle_xz, angle_yz))
    iterations += 1
    time.sleep(0.2)