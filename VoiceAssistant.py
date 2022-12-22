from __future__ import print_function
import warnings
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import datetime
import calendar
import webbrowser
import pyjokes
import os.path

import customtkinter
import threading

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


warnings.filterwarnings("ignore")


def rec_audio():
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        # Turn the icon BLUE
        print("Listening...")
        audio = recog.listen(source)
    data = " "

    try:
        data = recog.recognize_google(audio)
        print("You said: " + data)
    # except sr.UnknownValueError:
    except sr.UnknownValueError:
        return "NULL"
    except sr.RequestError as ex:
        print("Request error from Google Speech Recognition"+ex)
    return data

# Function to output as Audio


def response(text):
    print(text)

    tts = gTTS(text=text, lang="en")

    audio = 'audio.mp3'
    tts.save(audio)
    label.configure(fg="green")
    playsound.playsound(audio)
    label.configure(fg="white")
    os.remove(audio)

# Function to check for Action Word for the assistant


def AssistCall(text):
    actionWord = "assistant"
    text = text.lower()

    if actionWord in text:
        return True
    return False

# Function to know today's day and date:


def today():
    current = datetime.datetime.now()
    date = datetime.datetime.today()
    week = calendar.day_name[date.weekday()]
    month = current.month
    day = current.day
    year = current.year
    Lmonths = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    Lday = [
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th",
        "11th",
        "12th",
        "13th",
        "14th",
        "15th",
        "16th",
        "17th",
        "18th",
        "19th",
        "20th",
        "21st",
        "22nd",
        "23rd",
        "24th",
        "25th",
        "26th",
        "27th",
        "28th",
        "29th",
        "30th",
        "31st"
    ]
    return f"Today is {week},{Lday[day-1]} {Lmonths[month-1]} {year}"
# Function to know current time:


def currentTime():
    now = datetime.datetime.now()
    if now.hour > 12:
        postf = "p.m."
    else:
        postf = "a.m."
    if now.minute < 10:
        minute = "0"+str(now.minute)
    else:
        minute = str(now.minute)
    t = "Right now the time is "+str(now.hour)+":"+minute+" "+postf
    return t

# Function to greet first:


def greet():
    now = datetime.datetime.now()
    if now.hour < 12:
        response("Good Morning")
    elif now.hour >= 12 and now.hour < 16:
        response("Good Afternoon")
    else:
        response("Good Evening")


def TellAJoke():
    joke = pyjokes.get_joke(language="en", category="all")
    return joke

# -------------------------------------------------------------------------------------------------


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def google_calendar(num):

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        response(f'Getting the upcoming {num} events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=num, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            response('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            events_today = (event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(':')[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(':')[0])-12)
                start_time = start_time+"pm"
            response(f'{events_today} at {start_time}')


    except HttpError as error:
        response("Could not connect to the internet. Please try again later.")
# -------------------------------------------------------------------------------------------------
# main Program


def main():
    run = 1
    greet()
    while run:

        try:
            text1 = rec_audio()
            speak = ""
            if text1 != "NULL":
                if AssistCall(text1):  # if the action word is said

                    # Condition to know today's date
                    if "date" in text1 or "day" in text1:
                        todayData = today()
                        speak = speak + " " + todayData

                    # Condition to know current time
                    elif "time" in text1:
                        speak = speak + currentTime()

                    # Condition to search on YoTube
                    elif "youtube" in text1.lower():

                        ind = text1.lower().split().index("youtube")
                        search = text1.split()[ind+1:]
                        webbrowser.open(
                            "https://www.youtube.com/results?search_query=" +
                            "+".join(search)
                        )
                        speak = speak + "Searching" + \
                            str(search) + " on YouTube"

                    # Condition to search on Google
                    elif "google" in text1.lower():
                        ind = text1.lower().split().index("google")
                        search = text1.split()[ind+1:]
                        webbrowser.open(
                            "https://www.google.com/search?q=" +
                            "+".join(search)
                        )
                        speak = speak + "Searching" + \
                            str(search) + " on Google"

                    # Condition to play on Spotify
                    elif "spotify" in text1.lower():
                        ind = text1.lower().split().index("spotify")
                        play = text1.split()[2:ind-1]
                        webbrowser.open(
                            "https://open.spotify.com/search/" +
                            "+".join(play)
                        )
                        speak = speak + "Playing" + str(play) + "on Spotify"

                    # Condition to tell a joke
                    elif "joke" in text1.lower():
                        joke = TellAJoke()
                        speak = speak + joke

                    #Condition to check calendar
                    elif "calendar" in text1.lower():
                        google_calendar(10)
                        speak = speak + "That is it"
                    # Condition to exit the Assistant
                    elif "see you later" in text1.lower():
                        speak = speak + "good bye"
                        run = 0
                    response(speak)

            else:
                # Add conditions as project evolves
                response("Could you please repeat")
        except:
            txt = "I did not quite understand you"
            response(txt)


def startThread():
    threading.Thread(target=main).start()


customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")
root = customtkinter.CTk()
root.geometry("500x500")
root.title("Voice Assistant")
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)
label = customtkinter.CTkLabel(
    master=frame, text="🤖", text_font=("Aerial", 200))
label.pack(pady=10, padx=10)
startButton = customtkinter.CTkButton(master=frame, text="START", text_font=(
    "Aerial", 24), command=startThread)
startButton.pack(pady=10, padx=10)

root.mainloop()
