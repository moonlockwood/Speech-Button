import os
import sys
import win32api
import win32gui
import win32con
import pyperclip
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot, QObject
from speech_button_ui import SpeechButtonUI
from speech_button_arduino import ArduinoThread
from speech_button_transcriber import OpenAIThread
import speech_button_audio_recorder

class MainClass(QObject):
    def __init__(self):
        super().__init__()
        self.init_settings()
        self.init_openai()
        self.init_arduino()
        self.init_ui()   
        self.arduino_thread.arduino_object.button_state_changed.connect(self.handle_button_state)
        self.ui.start_recording_signal.connect(self.start_recording)
        self.ui.stop_recording_signal.connect(self.stop_recording)
        self.ui.stop_application_signal.connect(self.stop_application)
 
    @pyqtSlot()
    def start_recording(self):
        speech_button_audio_recorder.start_recording()

    @pyqtSlot()
    def stop_recording(self):
        audio_filename = 'recording.wav'
        speech_button_audio_recorder.stop_recording(audio_filename)
        text_output = self.openai_thread.transcribe_audio(audio_filename)
        print(text_output)
        os.remove('recording.wav')
        self.send_paste(text_output)
        
    def send_paste(self, text):
        pyperclip.copy(text)
        # Simulate a key press event for Ctrl+V
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.keybd_event(0x56, 0, 0, 0) # VK_V is not working, so we use 0x56 instead
        win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
  
    @pyqtSlot(bool)
    def handle_button_state(self, new_state):
        if new_state:
            self.ui.send_start_recording_signal()
        else:
            self.ui.send_stop_recording_signal()

    def init_settings(self):
        # Read settings from the file
        self.settings = {}
        with open("data/button_settings.txt", "r") as settings_file:
            for line in settings_file:
                key, value = line.strip().split("=")
                self.settings[key] = int(value)

    def init_openai(self):
        print('init openai')
        self.openai_thread = OpenAIThread()

    def init_arduino(self):
        self.arduino_thread = ArduinoThread()
        self.arduino_thread.start()

    def init_ui(self):
        self.ui = SpeechButtonUI(self.settings)
        self.ui.show()
        
    def stop_application(self):
        QApplication.quit()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_class = MainClass()
    sys.exit(app.exec())
