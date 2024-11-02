# MicroPython-IR-Transceiver-SAO
Send and Recieve IR data with your SAO easily!   

Driver for the [IR-Transceiver-SAO](https://github.com/alecjprobst/IR-Transceiver-SAO).  
For specific docs about the the IR-Transceiver-SAO, head over the IR-Transceiver-SAO project.

## Getting Started
Interfacing with the SAO can be done by using `IRRemoteSAO`.  
The SAO is set to I2C address `0x08` by default.  
```python
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
tvRemoteSAO = IRRemoteSAO( i2c, 0x08 )
```

`debug_logs` is an optional parameter that prints raw byte values sent and recieved over I2C.  
Default value is `False`. 
```python
tvRemoteSAO = IRRemoteSAO( i2c, 0x08, debug_logs=True)
```

`seconds_delay` is an optional parameter that configures the delay between I2C commands.  
Default value is `.5`.
```python
tvRemoteSAO = IRRemoteSAO( i2c, 0x08, seconds_delay=.5)
```


A basic test to verify your SAO and I2C is working can be done with the `ping` command.
```python
import machine
from IRRemote import IRRemoteSAO

device_i2c_address = 0x08 

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

tvRemoteSAO = IRRemoteSAO(i2c, device_i2c_address )
print(tvRemoteSAO.ping())
```

## Sending and Recieving Data

When IR data is recieved by the SAO, the data is stored in a buffer.  
By default, only one byte is sent.  
This example will print out data in the buffer. One the data is send over I2C, it is removed from the buffer. 
```python
import machine
from IRRemote import IRRemoteSAO

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
tvRemoteSAO = IRRemoteSAO( i2c, 0x08 )
size = tvRemoteSAO.get_ir_recieve_buffer_size()

if size > 1: 
    val = tvRemoteSAO.read_ir_byte()
    print(val)
```

The buffer can be enabled to store multiple values with `enable_ir_recieve_buffer`.  
The SAO has a max recieve buffer of 128 bytes.  
```python
tvRemoteSAO.enable_ir_recieve_buffer(1)
```

Writing data is simple. The following will transmit the number 1 to 10.  
```python
import machine
from IRRemote import IRRemoteSAO

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
tvRemoteSAO = IRRemoteSAO( i2c, 0x08 )

for x in range(0, 10): 
    tvRemoteSAO.write_ir_data_byte(0, x)
```

## Development
- Install Pico VS Code Extension: https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico
- Upload `src/IRRemote.py` to pico
- Now you can run any of the sample programs on the pico


