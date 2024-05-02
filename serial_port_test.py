import serial
import time
#import serial.tools.list_ports

class SerialTest:
    def __init__(self):
        self.arduino_port = 'COM10'
        self.arduino_speed = 115200
        self.timeout = 1
        
    def listen_to_arduino(self):
        try:
            self.active_serial_port = serial.Serial(self.arduino_port, self.arduino_speed)
            time.sleep(1)
            print("serial port connected")
            while True:
                try:
                    data = self.active_serial_port.read(1)
                    if data:
                        if data == b'\xAA':
                            button_state = self.active_serial_port.read(1)
                            if button_state == b'\x01':
                                self.button_state = True
                                #self.start_recording_signal.emit(event=None)
                                print(self.button_state)
                            elif button_state == b'\x00':
                                self.button_state = False
                                #self.stop_recording_signal.emit(event=None)
                                print(self.button_state)
                except Exception as e:
                    print(f"Error: {e}")
                    break        
        except Exception as e:
            print(f"couldn't connect to serial port: {e}")
            
if __name__ == '__main__':
    serial_tester = SerialTest()    
    serial_tester.listen_to_arduino()