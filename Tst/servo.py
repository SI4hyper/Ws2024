from board import SCL, SDA
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
import digitalio
import time
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)
mcp = MCP23017(i2c, address=0x25)
pca = PCA9685(i2c)
pca.frequency = 50

servo = servo.Servo(pca.channels[0])

servo.angle = 0
time.sleep(1)

sw1 = mcp.get_pin(0)

sw1.direction = digitalio.Direction.INPUT
sw1.pull = digitalio.Pull.UP

while True:
    if sw1.value:
        servo.angle = 0
    else:
        servo.angle = 180

    print(f"sw1: {sw1.value}")
    print(f"servo: {servo.angle}")
