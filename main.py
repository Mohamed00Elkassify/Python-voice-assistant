import speech_recognition as sr
import pyttsx3

# Initialize text_to_speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

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
