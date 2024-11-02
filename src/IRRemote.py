import time

__version__ = "1.0.0"

class IRRemoteSAO():
    PING_COMMAND_ID=0
    SET_IGNORE_IR_REFLECTIONS_COMMAND_ID=1
    SET_IR_MODE_COMMAND_ID=2
    ENABLE_IR_RECEIVE_BUFFER_COMMAND_ID=3
    SET_IR_ADDRESS_COMMAND_ID=4
    GET_IR_ADDRESS_COMMAND_ID=5
    CLEAR_IR_RECEIVE_BUFFER_COMMAND_ID=6
    GET_IR_RECEIVE_BUFFER_AVALIABLE_BYTES_COMMAND_ID=7
    READ_IR_BYTE_COMMAND_ID=8
    WRITE_IR_BYTE_COMMAND_ID=9
    WRITE_TO_IR_WRITE_BUFFER_COMMAND_ID=10
    GET_IR_WRITE_BUFFER_COMMAND_ID=11
    GET_IR_WRITE_BUFFER_AVALIABLE_BYTES_COMMAND_ID=12
    CLEAR_IR_WRITE_BUFFER_COMMAND_ID=13
    SET_IR_WRITE_BUFFER_ADDRESS_COMMAND_ID=14
    GET_IR_WRITE_BUFFER_ADDRESS_COMMAND_ID=15


    def __init__(self, i2c, i2c_address=0x08, debug_logs=False, seconds_delay=1):
        self.i2c = i2c
        self.i2c_address = i2c_address
        self.debug_logs = debug_logs
        self.seconds_delay = seconds_delay

    def __send_i2c(self, bytes):
        if self.debug_logs:
            print( 'Sending Bytes: ' )
            print(bytes)
        self.i2c.writeto(self.i2c_address, bytes)

    def __read_i2c(self, byte_count):
        response = self.i2c.readfrom(self.i2c_address, byte_count)

        if self.debug_logs:
            print( 'Response Bytes: ' )
            print(response)

        return response


    def ping(self) -> str:
        """
        Send a Ping command to IR Remote SAO.
        Expects a "pong" string return.
        """
    
        command_send = IRRemoteSAO.PING_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)
        response = self.__read_i2c(4)
        pong = response.decode('utf-8').strip()
        return pong
    
    def set_ignore_ir_reflection(self, ir_mode) -> None:
        """
        Set the IR reflection ignore option.
        Prevents IR reciever from reading a transmission send by the SAO.

        0 = Disabled
        1 = Enable
        """
        if ir_mode not in (0, 1):
            raise ValueError("IR Reflection must be either 0 (Disabled) or 1 (Enabled).")

        send = bytes([IRRemoteSAO.SET_IGNORE_IR_REFLECTIONS_COMMAND_ID, ir_mode])
        self.__send_i2c(send)
        time.sleep(self.seconds_delay)
    
    def set_ir_mode(self, ir_mode) -> None:
        """
        Set the IR Mode.
        Public mode allows SAO to read all IR transmissions.
        Address mode requires a specific address to read transmissions.

        0 = Public Mode
        1 = Address Mode
        """
        if ir_mode not in (0, 1):
            raise ValueError("IR Mode must be either 0 (public mode) or 1 (address mode).")

        send = bytes([IRRemoteSAO.SET_IR_MODE_COMMAND_ID, ir_mode])
        self.__send_i2c(send)
        time.sleep(self.seconds_delay)

    def enable_ir_recieve_buffer(self, ir_mode) -> None:
        """
        Enables or disables the ability to buffer IR data on the ATTINY85.
        Used for both transimission and recieve.
        Note: clears the receive buffer when this is changed

        0 = Disabled
        1 = Enabled
        """
        if ir_mode not in (0, 1):
            raise ValueError("IR Buffer must be either 0 (Disabled) or 1 (Enabled).")

        send = bytes([IRRemoteSAO.ENABLE_IR_RECEIVE_BUFFER_COMMAND_ID, ir_mode])
        self.__send_i2c(send)
        time.sleep(self.seconds_delay)
    
    def set_ir_address(self, ir_address) -> None:
        """
        Set the IR Address.
        This sets and sends an address with all IR transmissions.
        When using Address mode, will only read data with the set address.
        """
        if (ir_address < 0 or ir_address > 255):
            raise ValueError("IR Address must be between 0 and 255.")

        send = bytes([IRRemoteSAO.SET_IR_ADDRESS_COMMAND_ID, ir_address])
        self.__send_i2c(send)
        time.sleep(self.seconds_delay)

    def get_ir_address(self) -> int:
        """
        Get the current set IR Address.
        """
        command_send = IRRemoteSAO.GET_IR_ADDRESS_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)
        response = self.__read_i2c(1)
        return int.from_bytes(response, 'little') 
    
    def clear_ir_recieve_buffer(self) -> None:
        """
        Clear IR recieve buffer.
        """
        command_send = IRRemoteSAO.CLEAR_IR_RECEIVE_BUFFER_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)


    def get_ir_recieve_buffer_size(self) -> int:
        """
        Get current size of IR recieve buffer.
        """
        command_send = IRRemoteSAO.GET_IR_RECEIVE_BUFFER_AVALIABLE_BYTES_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)
        response = self.__read_i2c(1)
        return int.from_bytes(response, 'little') 
    
    def read_ir_byte(self) -> bytes:
        """
        Read byte from SAO.
        This will remove the byte from the buffer.
        """
        command_send = IRRemoteSAO.READ_IR_BYTE_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)
        response = self.__read_i2c(1)
        return response
    
    def write_ir_byte(self, address, byte) -> None:
        """
        Use SAO to write an byte with IR Transmitter.
        """
        send = bytes([IRRemoteSAO.WRITE_IR_BYTE_COMMAND_ID, address]) + byte
        self.__send_i2c(send)
        time.sleep(1)   

    def write_byte_to_ir_write_buffer(self, byte) -> None:
        """
        Set SAO write cache address and byte.
        When Button is used, the IR Transmitter will send cached address and byte.
        Otherwise this cache is ignored.
        """
        send = bytes([IRRemoteSAO.WRITE_TO_IR_WRITE_BUFFER_COMMAND_ID]) + byte
        self.__send_i2c(send)
        time.sleep(1)   
    
    def get_ir_write_buffer_size(self) -> int:
        """
        Get current size of IR write buffer.
        """
        command_send = IRRemoteSAO.GET_IR_WRITE_BUFFER_AVALIABLE_BYTES_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)
        response = self.__read_i2c(1)
        return int.from_bytes(response, 'little') 

    def clear_ir_write_buffer(self) -> None:
        """
        Clear IR write buffer.
        """
        command_send = IRRemoteSAO.CLEAR_IR_WRITE_BUFFER_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)

    def set_ir_write_buffer_address(self, ir_address) -> None:
        """
        Set the IR Address used for write buffer.
        This sets and sends an address with IR transmission used by the write cache.
        When using Address mode, will only read data with the set address.
        """
        if (ir_address < 0 or ir_address > 255):
            raise ValueError("IR Address must be between 0 and 255.")

        send = bytes([IRRemoteSAO.SET_IR_WRITE_BUFFER_ADDRESS_COMMAND_ID, ir_address])
        self.__send_i2c(send)
        time.sleep(self.seconds_delay)

    def get_ir_write_buffer_address(self) -> int:
        """
        Get the current set IR Address for write buffer.
        """
        command_send = IRRemoteSAO.GET_IR_WRITE_BUFFER_ADDRESS_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)
        response = self.__read_i2c(1)
        return int.from_bytes(response, 'little') 



    # TODO
    def get_ir_write_buffer(self) -> bytes:
        """
        Get the SAO write cache.
        Returns as Byte array with two bytes.
        First Byte is Address, Second Byte is cache byte.
        """
        command_send = IRRemoteSAO.GET_IR_WRITE_BUFFER_COMMAND_ID.to_bytes(1, 'little')
        self.__send_i2c(command_send)
        time.sleep(self.seconds_delay)
        response = self.__read_i2c(10)
        return response
        
        
 