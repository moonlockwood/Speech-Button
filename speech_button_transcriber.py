import openai
from PyQt6.QtCore import QThread

class OpenAIThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.init_openai()
    
    def init_openai(self):
        with open('data/openaikey.txt', 'r') as key_file:
            api_key = key_file.readline().strip()
        openai.api_key = api_key

    def transcribe_audio(self, audio_filename, model='whisper-1'):
        with open(audio_filename, 'rb') as f:
            transcription = openai.audio.transcriptions.create(model=model, file=f)
        return transcription.text

