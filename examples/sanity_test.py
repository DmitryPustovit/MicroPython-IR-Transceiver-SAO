import machine, sys
from utime import sleep
from IRRemote import IRRemoteSAO


# Set IR SAO I2C Address
device_i2c_address = 0x08 

# Setup I2C for Pico
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

# Setup IR SAO
tvRemoteSAO = IRRemoteSAO(i2c, device_i2c_address)

def input_check(value):
    if value > 255 or value < 0:
        return False
    return True

def sanity_check():
    print("What IR Address do you want to be? (0-255)")
    this_sao_ir_address = int(sys.stdin.readline())
    if not input_check(this_sao_ir_address):
        print("Error: input must be an integer between 0 and 255")
        return
    print("What IR Address do you want to send to? (0-255)")
    target_sao_ir_address = int(sys.stdin.readline())
    if not input_check(target_sao_ir_address):
        print("Error: input must be an integer between 0 and 255")
        return
    if target_sao_ir_address == this_sao_ir_address:
        print("Warning: target_sao_address should not be equal to this_sao_address as reflections can cause false positives")
    print("What data do you want to send to the other SAO? (0-255)")
    data_to_send = int(sys.stdin.readline())
    if not input_check(data_to_send):
        print("Error: input must be an integer between 0 and 255")
        return
    print("What data do you want to receive from the other SAO? (0-255)")
    data_to_receive = int(sys.stdin.readline())
    if not input_check(data_to_receive):
        print("Error: input must be an integer between 0 and 255")
        return
    '''
    print("Are you sending data first? (y/n)")
    send_first_char = str(sys.stdin.readline())
    if send_first_char.strip().lower() == 'y':
        send_first = True
    elif send_first_char.strip().lower() == 'n':
        send_first = False
    else:
        print("Error: input must be 'y' or 'n'")
        return
    '''
    print("\n---SAO Setup---")
    # Test that SAO responds
    ping_response = tvRemoteSAO.ping()
    if ping_response == 'pong':
        print("Check that SAO Responds: True")
    else:
        print("Check that SAO Responds: False, received " + str(ping_response))

    # Setting IR Address
    print("Setting IR Addres to " + str(this_sao_ir_address))
    tvRemoteSAO.set_ir_address(this_sao_ir_address)

    # Disable IR Receive Buffer
    print("Disabling IR Receiver Buffer")
    tvRemoteSAO.enable_ir_receive_buffer(0)

    # Set IR Command Mode to Address
    print("Setting IR rceiver mode to address mode (1)")
    tvRemoteSAO.set_ir_mode(1)

    # Set Ignore Command Reflection to True
    print("Setting Ignore IR Command Reflections to True")
    tvRemoteSAO.set_ignore_ir_reflection(1)

    # Clear and Check Transmit Buffer
    print("Clearing Transmit Buffer of SAO")
    tvRemoteSAO.clear_ir_write_buffer()
    print("Number of Bytes in Transmit Buffer: " + str(tvRemoteSAO.get_byte_count_in_ir_receive_buffer()))

    # Clear and Check Receive Buffer
    print("Clearing Receive Buffer of SAO")
    tvRemoteSAO.clear_ir_receive_buffer()
    print("Number of Bytes in Receive Buffer: " + str(tvRemoteSAO.get_byte_count_in_ir_receive_buffer()))


    print("\n---SAO Sending/Receiving---")
    # Make sure receive data is always wrong the first check
    received_data = data_to_receive + 1

    # Constantly send IR data while seeing if we receive expected data back (Tests if the send and receive works )
    print("Sending IR data " + str(data_to_send) + " to IR Address " + str(target_sao_ir_address) + " and waiting for response of value " + str(data_to_receive)+ " at this SAO's address of " + str(this_sao_ir_address))
    try:
        while True:
            while(tvRemoteSAO.get_byte_count_in_ir_receive_buffer() < 1):
                tvRemoteSAO.write_ir_data_byte(target_sao_ir_address, data_to_send)
                print("Sending IR data " + str(data_to_send) + " to address " + str(target_sao_ir_address) + " again")
                sleep(0.5)
            
            received_data = int.from_bytes(tvRemoteSAO.read_ir_byte(), 'big')
            if received_data != data_to_receive:
                print("Incorrect received data of value " + str(received_data))
            else:
                print("Success! This IR SAO works correctly for receiving! Will continue to transmit, if the other SAO has sucess transmitting works as well!")
    except KeyboardInterrupt:
        print("Interrupted")

    '''
    else:
        # Constantly check to see if received IR data
        print("Waiting to receive IR data " + str(data_to_receive) + " at this SAO's address " + str(this_sao_ir_address))
        while(received_data != data_to_receive):
            while(tvRemoteSAO.get_byte_count_in_ir_receive_buffer() < 1):
                print("Waiting to receive data " + str(data_to_receive))
                sleep(0.5)
                
            received_data = int.from_bytes(tvRemoteSAO.read_ir_byte())
            if received_data != data_to_receive:
                print("Incorrect received data of value " + str(received_data))
            else:
                print("Received correct data of " + str(data_to_receive))
                # Make sure receive data is not equal to data_to_receive and buffer is clear
                received_data = data_to_receive + 1
                tvRemoteSAO.clear_ir_receive_buffer()
                sleep(0.5)
                # Constantly send IR data while seeing if we receive expected data back (Tests if the send and receive works )
                print("Sending IR data " + str(data_to_send) + " to IR Address " + str(target_sao_ir_address) + " and waiting for response of value " + str(data_to_receive)+ " at this SAO's address of " + str(this_sao_ir_address))
                while(received_data != data_to_receive):
                    while(tvRemoteSAO.get_byte_count_in_ir_receive_buffer() < 1):
                        tvRemoteSAO.write_ir_data_byte(target_sao_ir_address, data_to_send)
                        print("Sending IR data " + str(data_to_send) + " to address " + str(target_sao_ir_address) + " again")
                        sleep(0.5)
                    
                    received_data = int.from_bytes(tvRemoteSAO.read_ir_byte())
                    if received_data != data_to_receive:
                        print("Incorrect received data of value " + str(received_data))
                    else:
                        print("Success! Sanity Test Passed, IR SAO communication works correctly")
                        print("---END---")
    '''
sanity_check()