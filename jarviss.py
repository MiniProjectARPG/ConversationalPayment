import pyttsx3
import datetime
import speech_recognition as sr  
import wikipedia
import webbrowser

engine =pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("..Good Morning")

    elif hour>=12 and hour<18:
        speak("..Good Afternoon")

    else:
        speak("..Good evening")

    speak("i am jarvis..How may i help you")

def takeCommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)
        
    try:
        print("Recognising...")
        query=r.recognize_google(audio,language="en-in")
        print(f"User said: {query}\n")

        
    except Exception as e:
        print(e)
        print("Say that again please...")
        return"None"

    return query

if __name__=="__main__":
    wishMe()

    while True:
        query=takeCommand().lower()

        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query=query.replace("wikipedia"," ")
            results=wikipedia.summary(query,sentences=2)
            speak("Accoarding to wikipedia")
            speak(results)


        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
            

        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")

        elif 'open spotify' in query:
            speak("opening spotify")
            webbrowser.open("spotify.com")

        elif 'the time' in query:
            speak("time is")
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            webbrowser.open("youtube.com")

        elif 'open whatsapp' in query:
            speak("opening whatsapp")
            webbrowser.open("whatsapp.com")

        elif 'open instagram' in query:
            speak("opening instagram")
            webbrowser.open("instagram.com")

        elif 'open google-Docs' in query:
            speak("opening google docs")
            webbrowser.open("docs.google.com")

        elif 'open paytm' in query:
            speak("opening paytm")
            webbrowser.open("paytm.com")
        
     

