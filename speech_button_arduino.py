import serial
import time
from PyQt6.QtCore import pyqtSignal, QObject, QThread

class ArduinoThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.arduino_object = ArduinoTools()
 
    def run(self):
        self.arduino_object.listen_to_arduino()
        return self.arduino_object
   
class ArduinoTools(QObject):
    button_state_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.arduino_port = 'COM5' 
        self.arduino_speed = 115200
        self.timeout = 1

    def listen_to_arduino(self):
        try:
            self.active_serial_port = serial.Serial(self.arduino_port, self.arduino_speed, timeout=self.timeout)
            time.sleep(1)
            print("serial port connected")
            self.active_serial_port.reset_input_buffer()
            self.button_state=False
            
            while True:
                try:
                    data = self.active_serial_port.read(1)
                    if data:
                        if data == b'\xAA':
                            button_state = self.active_serial_port.read(1)
                            if button_state == b'\x01' and not self.button_state:
                                self.button_state = True
                            elif button_state == b'\x00' and self.button_state:
                                self.button_state = False
                            self.button_state_changed.emit(self.button_state)
                                
                except Exception as e:
                    self.button_state = False
                    self.button_state_changed.emit(self.button_state)
                    print(f"Error: {e}")
                    break
                
        except Exception as e:
            print(f"couldn't connect to serial port: {e}")
