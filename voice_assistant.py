import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
from newsapi import NewsApiClient
from datetime import datetime
import pyowm
import geocoder
from twilio.rest import Client
import wikipedia
import requests  # Import the requests module

owm_api_key = #Your OWM API key
owm = pyowm.OWM(owm_api_key)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error connecting to Google API: {e}")
        return None


def speak(text):
    engine.say(text)
    engine.runAndWait()


def open_website(url):
    webbrowser.open(url)


def open_spotify_and_play(song_name):
    base_url = "https://open.spotify.com/search/"
    search_query = urllib.parse.quote(song_name)
    spotify_url = f"{base_url}{search_query}"
    webbrowser.open(spotify_url)
    speak(f"Searching for {song_name} on Spotify. Enjoy listening!")
    return True  # Indicate that the song was opened successfully


def read_news_headlines(topic):
    newsapi = NewsApiClient(api_key=#newsapi API Key)  
    headlines = newsapi.get_top_headlines(q=topic, language='en')

    print("News API Response:", headlines)  # Add this line for debugging

    if headlines and 'articles' in headlines:
        speak(f"Here are the top headlines on {topic}:")

        for idx, article in enumerate(headlines['articles']):
            if idx == 5:  # Read only the top 5 headlines for brevity
                break
            speak(article['title'])
    else:
        speak(f"Sorry, I couldn't retrieve news on {topic}. Please try again.")


def get_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}.")


def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    speak(f"Today's date is {current_date}.")


def get_weather():
    speak("Please tell me the city for which you want to know the weather.")
    city = recognize_speech()

    if city:
        observation = owm.weather_manager().weather_at_place(city)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        status = w.detailed_status

        speak(f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't understand the city. Please try again.")


def get_current_location():
    location = geocoder.ip('me')
    speak(f"Your current location is {location.city}, {location.country}.")


def wish_me():
    hour = datetime.now().hour
    if 0 <= hour < 12:
        print("Hello, Good Morning")
        speak("Hello, Good Morning")
    elif 12 <= hour < 18:
        print("Hello, Good Afternoon")
        speak("Hello, Good Afternoon")

    else:
        print("Hello, Good Evening")
        speak("Hello, Good Evening")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


def search_for_place(place_name):
    # Use requests to send a POST request to the server to perform the search
    response = requests.post('http://localhost:5000/search_for_place', data={'place_name': place_name})
    print(response.text)  # Print the server response for debugging


def start_speech_recognition():
    while True:
        user_input = take_command()

        if user_input:
            print("You said:", user_input)
            if "search for a place" in user_input.lower():
                speak("Sure, tell me the place you want to search for.")
                place_name = recognize_speech()
                if place_name:
                    search_for_place(place_name)
                    reply = f"Searching for {place_name}."
                else:
                    reply = "Sorry, I couldn't understand the place name. Please try again."
            elif "hello" in user_input.lower():
                reply = "Hello! I hope you are having a wonderful day."
            elif "how are you" in user_input.lower():
                reply = "I am good. How about you?"
            elif "fine" in user_input.lower() or "I am good as well" in user_input.lower() or "great" in user_input.lower():
                reply = "Glad to hear."
            elif "not fine" in user_input.lower() or "I am not good" in user_input.lower() or "bad" in user_input.lower():
                reply = "Sorry to hear that. I hope you will be fine."
            elif "open a website" in user_input.lower():
                print("Please say the website URL.")
                speak("Please say the website URL.")
                website_url = recognize_speech()
                if website_url:
                    open_website(website_url)
                    reply = f"Opening {website_url}."
                else:
                    reply = "Sorry, I couldn't understand the website URL. Please try again."
            elif "play a song" in user_input.lower():
                print("Sure, please tell me the name of the song you want to play.")
                speak("Sure, please tell me the name of the song you want to play.")
                song_name = recognize_speech()
                if song_name:
                    success = open_spotify_and_play(song_name)
                    if success:
                        reply = f"Playing {song_name} on Spotify."
                    else:
                        reply = "Sorry, I couldn't play the song. Please try again."
            elif "read me the news" in user_input.lower():
                speak("Sure, please tell me the topic you want to hear the news about.")
                news_topic = recognize_speech()
                if news_topic:
                    read_news_headlines(news_topic)
                    reply = f"Done Reading news on {news_topic}."
                else:
                    reply = "Sorry, I couldn't understand the news topic. Please try again."
            elif "what is the current time" in user_input.lower():
                get_current_time()
                reply = "I told you the current time."
            elif "what is the current date" in user_input.lower():
                get_current_date()
                reply = "I told you the current date."
            elif "how is the weather today" in user_input.lower():
                get_weather()
                reply = "I told you the current weather."
            elif "what is my current location" in user_input.lower():
                get_current_location()
                reply = "I told you your current location."
            elif "bye" in user_input.lower():
                reply = "Goodbye! Have a great day."
                speak(reply)
                exit()  # Exit the loop when "goodbye" is said
            else:
                reply = "I didn't understand that. Can you please repeat?"

            print("Reply:", reply)
            speak(reply)


wish_me()
print("Welcome! I am your virtual assistant. What can I assist you with today.")
speak("Welcome! I am your virtual assistant. What can I assist you with today.")

# Start speech recognition loop
start_speech_recognition()
