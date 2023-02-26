import speech_recognition as sr
import os


def bytearray_to_text(audio_bytes, sample_rate= 16000):
    # Initialize a recognizer object
    r = sr.Recognizer()

    # Convert the bytearray to an AudioData object
    audio = sr.AudioData(audio_bytes, sample_rate=sample_rate, sample_width=2)

    # Use the recognizer object to recognize speech in the audio data
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ("Speech recognition could not understand audio")
    except sr.RequestError as e:
        return (f"Could not request results from Google Speech Recognition service; {e}")





if __name__ == "__main__":
    # Example bytearray (replace with your own)
    audio_bytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')

    # Call the function and print the result
    result = bytearray_to_text(audio_bytes)
    print(result)
