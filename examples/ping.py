import machine
from src.IRRemote import IRRemoteSAO

device_i2c_address = 0x08 
device_IR_address = 0

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

tvRemoteSAO = IRRemoteSAO(i2c, device_i2c_address, device_IR_address )
print(tvRemoteSAO.ping())