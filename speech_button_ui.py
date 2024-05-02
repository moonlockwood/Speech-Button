import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

class SpeechButtonUI(QMainWindow):
    start_recording_signal = pyqtSignal()
    stop_recording_signal = pyqtSignal()
    stop_application_signal = pyqtSignal()
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.init_ui()
        
    @property
    def window_width(self):
        return self.settings["window_width"]

    @property
    def window_height(self):
        return self.settings["window_height"]

    @property
    def corner_radius(self):
        return self.settings["corner_radius"]
    
    def press_button(self):
        #print('press_button')
        self.send_start_recording_signal()

    def release_button(self):
        #print('release_button')
        self.send_stop_recording_signal()

    def init_ui(self):
        self.setGeometry(8, 8, self.window_width, self.window_height)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Create the widget
        self.widget = QWidget(self)
        self.widget.setStyleSheet("background-color: rgb(255,255,255); border-radius: 10px;")
        self.widget.setGeometry(0, 0, self.window_width, self.window_height)

        # Event handlers for mouse events
        self.widget.mousePressEvent = self.on_press
        self.widget.mouseReleaseEvent = self.on_release
        self.widget.mouseMoveEvent = self.on_motion
        self.widget.mouseDoubleClickEvent = self.on_double_click
        self.dragging = False
    
    def on_motion(self, event):
        if self.dragging:
            global_pos = event.globalPosition().toPoint()  # Convert globalPosition to QPoint
            self.move(int(global_pos.x() - self.start_drag_x), int(global_pos.y() - self.start_drag_y))
            event.accept()
            
    def on_press(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
                self.dragging = True
                self.start_drag_x = event.position().x()
                self.start_drag_y = event.position().y()
                event.accept()
            else:
                self.send_start_recording_signal()
                
    def on_release(self, event):
        if self.dragging and QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
            self.dragging = False
            event.accept()
        elif event.button() == Qt.MouseButton.LeftButton:
            self.send_stop_recording_signal()
            
    def send_start_recording_signal(self):
        self.widget.setStyleSheet("background-color: rgb(169,169,169); border-radius: 10px;")  # Set to dark gray
        self.start_recording_signal.emit()        
               
    def send_stop_recording_signal(self):
        self.widget.setStyleSheet("background-color: rgb(255,255,255); border-radius: 10px;")  # Set to dark gray
        self.stop_recording_signal.emit()        
                       
    def on_start_processing(self):
        print('processing')
                 
    def on_done_processing(self):
        print('processing')
        
    def on_double_click(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
                self.stop_application()  
                          
    def stop_application(self):
        self.close()
        self.stop_application_signal.emit()
    
    