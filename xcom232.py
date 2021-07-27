from api import Xcom_API
import serial

class xcom232(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):      
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.uart = serial.Serial(port=self.port, baudrate=self.baudrate, parity= serial.PARITY_EVEN, timeout=self.timeout)
        self.api = Xcom_API(crc=True, source=1, destination=101)


    def __transmit(self, data: str):
        try:
            self.uart.write(data)
            #data = uart.read_until(expected=b'\x0D\x0A', size=100)
            #data = self.uart.read_until(expected=b'\x85Q', size=200)
            data = self.uart.read(30)
            #print(len(data))
            return data
        except:
            print ("Error Uart __receive", self.port)
            raise Exception 
            return ""

    def read_id(self, id:int):
        try:
            if self.uart.isOpen():
                self.uart.flushInput()
                self.uart.flushOutput()
                result = self.__transmit(self.api.get_read_frame(id))
                result = self.api.get_data_from_frame(result)
                if result[0] == True:
                    return self.api.get_text_from_error_id(result[2]) #vml. besser mit raise Event ?
                else:
                    return result[1]
            else:
                return ""
        except:
            print("Error UART read_id : " + str(id) )
            raise Exception
            return ""

    def write_id(self, id:int, data):
        try:
            if self.uart.isOpen():
                self.uart.flushInput()
                self.uart.flushOutput()
                result = self.__transmit(self.api.get_write_frame(id), data)
                return self.api.get_data_from_frame(result)[1]
            else:
                return ""
        except:
            print("Error UART write_id")
            raise Exception
            return ""


    def __del__(self):
        #print("del xcom object")
        if self.uart.isOpen():
            self.uart.close
        

# \xaace\x00\x00\x00\x01\x00\x00\x00\x0e\x00\xd6J\x02\x01\x01\x00\xc3\x0b\x00\x00\x01\x00\x00\x00rC\x87U


