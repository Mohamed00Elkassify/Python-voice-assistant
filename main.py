import speech_recognition as sr
import pyttsx3
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import os

# Initialize text_to_speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

# Initialize system volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# function to convert text to speech
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# function to convert speech to text
def recognize_speech():
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=7)
            command = r.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            speak("I'm having trouble accessing the speech service.")
            return None
        except sr.WaitTimeoutError:
            speak("I'm sorry, i didn't hear you.")
            return None

# function to control system volume
def control_volume(command):
    if "volume up" in command:
        current_volume = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current_volume + 0.1, 1.0), None)
        speak("Volume increased.")
    elif "volume down" in command:
        current_volume = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current_volume - 0.1, 1.0), None)
        speak("Volume decreased.")

# function to open applications
def open_app(command):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "spotify": "spotify.exe"
    }
    for app in apps:
        if app in command:
            speak(f"Opening {app}.")
            os.system(apps[app])
            return True
    return False