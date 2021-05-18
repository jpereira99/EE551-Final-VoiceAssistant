# Jayden Pereira
# EE 551 Final Project

import speech_recognition as sr  # Speech recognition interface
from gtts import gTTS  # Google Text-to-Speech interface
import os  # Delete temporary audio file
import pygame  # To play TTS audio file
from googlesearch import search  # Google search parser
import wikipedia as wiki  # Wikipedia parser
pygame.init()

# Method to take string and return Google TTS audio
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "audio.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    os.remove(filename)

# Method to play musical chime
def chime():
    pygame.mixer.init()
    pygame.mixer.music.load("chime.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()

# Obtain audio from user
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Waiting for voice...")
    chime()
    audio = r.listen(source)

try:
    userRequest = r.recognize_google(audio)
    print("\nGoogle Speech Recognition: " + userRequest)
    # Google search user request
    arrOfResults = search(userRequest)
    # Iterate through requests to find one or the first Wikipedia page
    entryFound = False
    for element in arrOfResults:
        if 'https://en.wikipedia.org/wiki/' in element:
            # Format url to
            article = element.replace("https://en.wikipedia.org/wiki/", "")
            article = article.replace("_", " ")
            try:
                summary = wiki.summary(article, sentences=2)
                entryFound = True
                print('\nFound article pertaining to search: ' + article)
                speak("According to Wikipedia " + summary)
                break
            except:
                continue


    # Wiki page not found, return sorry message
    if not entryFound:
        speak("Sorry, I couldn't find what you were looking for")

# An error occurred when transcribing speech
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

