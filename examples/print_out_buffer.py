import machine
from IRRemote import IRRemoteSAO

device_i2c_address = 0x08 

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

tvRemoteSAO = IRRemoteSAO( i2c, device_i2c_address, debug_logs=False )
size = tvRemoteSAO.get_byte_count_in_ir_receive_buffer()

if size < 1: 
    tvRemoteSAO.enable_ir_receive_buffer(1)
    print("Recieve Buffer Enabled")

size = tvRemoteSAO.get_byte_count_in_ir_receive_buffer()
for x in range(0, size):
    val = tvRemoteSAO.read_ir_byte()
    print(val)
