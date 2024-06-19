import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
import digitalio

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x25)

sw1 = mcp.get_pin(0)
led1 = mcp.get_pin(1)

sw1.direction = digitalio.Direction.INPUT
sw1.pull = digitalio.Pull.UP
led1.direction = digitalio.Direction.OUTPUT

while True:
    if sw1.value:
        led1.value = True
    else:
        led1.value = False

    print(f"sw1: {sw1.value}")
    print(f"led1: {led1.value}")
