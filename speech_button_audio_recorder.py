import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

sample_rate = 44100  # in Hz

recording = []
stream = None

def callback(indata, frames, time, status):
    global recording
    recording.append(indata.copy())

def start_recording():
    global stream
    global recording
    recording = []

    # Query for available devices
    devices = sd.query_devices()
    preferred_device_name = None
    if preferred_device_name is None:
        device_id = sd.default.device[0]  # Default input device
    else:
        device_id = None
        # Search for the device by name or other criteria
        for idx, device in enumerate(devices):
            if preferred_device_name in device['name']:
                device_id = idx
                break
        # Fallback to default device if not found
        if device_id is None:
            print(f"Device '{preferred_device_name}' not found. Using default.")
            device_id = sd.default.device[0]  # Default input device

    stream = sd.InputStream(device=device_id, samplerate=sample_rate, channels=1, callback=callback)
    stream.start()

def stop_recording(filename):
    global stream
    global recording

    if stream is not None:
        stream.stop()
        stream.close()

    if recording:
        audio_data = np.concatenate(recording, axis=0)
        write(filename, sample_rate, audio_data)
