# MicroPython-IR-Transceiver-SAO
Send and Recieve IR data with your SAO easily!   

Driver for the [IR-Transceiver-SAO](https://github.com/alecjprobst/IR-Transceiver-SAO).  
For specific docs about the the IR-Transceiver-SAO, head over the IR-Transceiver-SAO project.

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

## Development
- Install Pico VS Code Extension: https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico
- Upload `src/IRRemote.py` to pico
- Now you can run any of the sample programs on the pico


