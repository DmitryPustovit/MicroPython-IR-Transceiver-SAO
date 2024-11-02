from machine import Pin
from utime import sleep
from machine import Timer

import machine
from IRRemote import IRRemoteSAO

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
device_i2c_address = 0x08 
tvRemoteSAO = IRRemoteSAO(i2c, device_i2c_address, False)

tvRemoteSAO.set_ir_mode(0)
tvRemoteSAO.enable_ir_recieve_buffer(0)

count = 0 
polling_interval = 2000  # 2 seconds

def poll_ir(timer):
    global count
    if tvRemoteSAO.get_ir_buffer_size() > 0:
        number = int.from_bytes(tvRemoteSAO.read_ir_byte(), "little")
        if 0 < number < 10:
            print("Recieved: ", number)
            count += number
    print("Current Count:", count)
    tvRemoteSAO.write_ir_byte(0, bytes([count]))

timer = Timer()
timer.init(period=polling_interval, mode=Timer.PERIODIC, callback=poll_ir)

# Check for KeyboardInterrupt
try:
    while True:
        sleep(0.1)  # Minimal blocking sleep
except KeyboardInterrupt:
    print("Interrupted")

finally:
    timer.deinit()