import os
import spacy
import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import requests

class NLPModule:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        # Start with a greeting
        self.speak_output("greet", None)

    def process_voice(self):
        recognizer = sr.Recognizer()

        while True:
            with sr.Microphone() as source:
                print("Say something:")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    voice_input = recognizer.recognize_google(audio)
                    print("You said:", voice_input)
                    intent, entities = self.process_text(voice_input)
                    self.perform_action(intent, entities)
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand your voice. Please try again.")

    def process_text(self, user_input):
        doc = self.nlp(user_input)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        intent = self.determine_intent(doc)
        return intent, entities

    def determine_intent(self, doc):
        greetings = ["hello", "hi", "hey"]
        goodbyes = ["bye", "goodbye", "see you", "farewell"]
        reminder = ["remind", "reminder"]
        email = ["email", "send email", "read email"]
        news = ["news", "latest news", "headlines"]

        for token in doc:
            if token.text.lower() in greetings:
                return "greet"
            elif token.text.lower() in goodbyes:
                return "goodbye"
            elif token.text.lower() in reminder:
                return "reminder"
            elif token.text.lower() in email:
                return "email"
            elif token.text.lower() in news:
                return "news"

        return "unknown"

    def speak_output(self, intent, entities):
        if intent == "greet":
            self.google_tts("Hi! How can I assist you today?")
        elif intent == "goodbye":
            self.google_tts("Goodbye! Have a great day!")
        elif intent == "reminder":
            if entities:
                # Assuming you are interested in specific entity types (e.g., DATE)
                date_entities = [ent[0] for ent in entities if ent[1] == "DATE"]
                if date_entities:
                    reminder_date = date_entities[0]
                    self.google_tts(f"Sure, I will remind you on {reminder_date}")
                else:
                    self.google_tts("Sure, I will set a reminder for you.")
            else:
                self.google_tts("Sure, I will set a reminder for you.")
        elif intent == "email":
            self.google_tts("Sorry, email functionality is not implemented yet.")
        elif intent == "news":
            self.get_news()
        else:
            self.google_tts("I'm not sure how to respond to that.")

    def get_news(self):
        # Use a news API to get the latest headlines
        news_api_key = "YOUR_NEWS_API_KEY"
        news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"

        response = requests.get(news_url)
        data = response.json()

        if data.get("status") == "ok":
            articles = data.get("articles", [])
            if articles:
                headlines = [article["title"] for article in articles[:5]]  # Get the first 5 headlines
                news_text = ". ".join(headlines)
                self.google_tts(f"Here are the latest headlines: {news_text}")
            else:
                self.google_tts("Sorry, I couldn't fetch the latest news.")
        else:
            self.google_tts("Sorry, I couldn't fetch the latest news.")

    def perform_action(self, intent, entities):
        self.speak_output(intent, entities)

    def google_tts(self, text):
        tts = gTTS(text=text, lang="en")
        tts.save("output.mp3")

        # Use pygame to play the audio
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Clean up the temporary audio file
        time.sleep(2)  # Adjust as needed
        pygame.mixer.quit()
        pygame.time.delay(1000)  # Ensure previous audio finishes playing
        pygame.mixer.init()

        # then delete the file
        os.remove("output.mp3")

# Example usage
if __name__ == "__main__":
    nlp_module = NLPModule()
    nlp_module.process_voice()
