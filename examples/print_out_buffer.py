import machine
from IRRemote import IRRemoteSAO

device_i2c_address = 0x08 

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

tvRemoteSAO = IRRemoteSAO( i2c, device_i2c_address, debug_logs=True)
size = tvRemoteSAO.get_ir_recieve_buffer_size()

if size < 1: 
    tvRemoteSAO.enable_ir_recieve_buffer(1)
    print("Recieve Buffer Enabled")
else: 
    size = tvRemoteSAO.get_ir_recieve_buffer_size()
    for x in range(0, size):
        val = tvRemoteSAO.read_ir_byte()
        print(val)
