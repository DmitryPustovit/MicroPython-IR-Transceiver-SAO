# MicroPython-IR-Transceiver-SAO
Driver for the [IR-Transceiver-SAO](https://github.com/alecjprobst/IR-Transceiver-SAO).  
Send and Recieve IR data with your SAO easily!  

## Getting Started

A basic test to verify your SAO and I2C is working can be done with the `ping` command.
```python
import machine
from IRRemote import IRRemoteSAO

device_i2c_address = 0x08 

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

tvRemoteSAO = IRRemoteSAO(i2c, device_i2c_address )
print(tvRemoteSAO.ping())
```
