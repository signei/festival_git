import pyaudio
import wave
import os
import test_inference_update
import asyncio

path = 'C:/Users/bio/Documents/festival/'

def start_recording(filename, t):  # filename = 학번?
    filename = filename[0]
    CHUNK = 44100  # Buffer size for each audio frame.
    # Data type. paInt16 is a common format for WAV files.
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # Stereo audio.
    # Sample rate equals to CHUNK size to make each loop run for about one second.
    RATE = CHUNK

    duration = 5

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, duration):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    # Create a directory if it doesn't exist.
    directory = f"./data/{filename}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the file in the created directory.
    filename = f"{filename}_{t}.wav"
    wf = wave.open(os.path.join(directory, filename), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


async def async_start_recording(filename, t):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, start_recording, filename, t)


def predict(name, filename):  # 얘는 폴더를 집어넣어요 학번으로 되어있는
    path = f"./data/{filename}/"
    # Make sure this function is defined and returns a score.
    score = test_inference_update.inference(name, path)
    return score
