import machine
from IRRemote import IRRemoteSAO

device_i2c_address = 0x08 
device_IR_address = 0

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

tvRemoteSAO = IRRemoteSAO(i2c, device_i2c_address, False)
tvRemoteSAO.write_data_byte_to_ir_write_buffer(3)
buffer_used_bytes = tvRemoteSAO.get_byte_count_in_ir_write_buffer()
print(tvRemoteSAO.get_ir_write_buffer(buffer_used_bytes))