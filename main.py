import os
import spacy
import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import datetime

class NLPModule:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        # Start with a greeting
        self.speak_output("greet", None)

    def process_text(self, user_input):
        doc = self.nlp(user_input)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        intent = self.determine_intent(doc)
        return intent, entities

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
                    self.speak_output(intent, entities)
                    return intent, entities
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand your voice. Please try again.")

    def determine_intent(self, doc):
        greetings = ["hello", "hi", "hey"]
        goodbyes = ["bye", "goodbye", "see you", "farewell"]
        reminder = ["remind", "reminder"]
        weather = ["weather"]
        joke = ["joke"]
        president = ["president"]
        capital = ["capital"]
        timer = ["timer"]
        calendar = ["calendar", "appointment"]
        text_message = ["text", "message"]
        call = ["call"]
        directions = ["directions", "traffic"]
        play_music = ["play"]
        movies = ["movies", "playing"]
        story = ["story"]
        smart_home = ["turn off", "set the thermostat", "lock the front door"]
        shopping_list = ["shopping list", "add"]
        to_do_list = ["to-do list"]
        order_online = ["order"]
        translation = ["translate", "say"]
        search_web = ["search the web", "population", "define"]
        calculations = ["calculate"]
        health = ["calories", "workout routine"]
        riddle = ["riddle"]
        roll_dice = ["roll a dice"]
        sing_song = ["sing a song"]

        for token in doc:
            if token.text.lower() in greetings:
                return "greet"
            elif token.text.lower() in goodbyes:
                return "goodbye"
            elif token.text.lower() in reminder:
                return "reminder"
            elif token.text.lower() in weather:
                return "weather"
            elif token.text.lower() in joke:
                return "joke"
            elif token.text.lower() in president:
                return "president"
            elif token.text.lower() in capital:
                return "capital"
            elif token.text.lower() in timer:
                return "timer"
            elif token.text.lower() in calendar:
                return "calendar"
            elif token.text.lower() in text_message:
                return "text_message"
            elif token.text.lower() in call:
                return "call"
            elif token.text.lower() in directions:
                return "directions"
            elif token.text.lower() in play_music:
                return "play_music"
            elif token.text.lower() in movies:
                return "movies"
            elif token.text.lower() in story:
                return "story"
            elif token.text.lower() in smart_home:
                return "smart_home"
            elif token.text.lower() in shopping_list:
                return "shopping_list"
            elif token.text.lower() in to_do_list:
                return "to_do_list"
            elif token.text.lower() in order_online:
                return "order_online"
            elif token.text.lower() in translation:
                return "translation"
            elif token.text.lower() in search_web:
                return "search_web"
            elif token.text.lower() in calculations:
                return "calculations"
            elif token.text.lower() in health:
                return "health"
            elif token.text.lower() in riddle:
                return "riddle"
            elif token.text.lower() in roll_dice:
                return "roll_dice"
            elif token.text.lower() in sing_song:
                return "sing_song"

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
        elif intent == "weather":
            self.get_weather()
        elif intent == "joke":
            self.tell_joke()
        elif intent == "president":
            self.get_president_info()
        elif intent == "capital":
            self.get_capital_info()
        elif intent == "timer":
            self.set_timer(entities)
        elif intent == "calendar":
            self.get_calendar_info()
        elif intent == "text_message":
            self.send_text_message(entities)
        elif intent == "call":
            self.make_call(entities)
        elif intent == "directions":
            self.get_directions(entities)
        elif intent == "play_music":
            self.play_music(entities)
        elif intent == "movies":
            self.get_movies_info()
        elif intent == "story":
            self.tell_story()
        elif intent == "smart_home":
            self.control_smart_home(entities)
        elif intent == "shopping_list":
            self.add_to_shopping_list(entities)
        elif intent == "to_do_list":
            self.get_to_do_list_info()
        elif intent == "order_online":
            self.order_online(entities)
        elif intent == "translation":
            self.translate_text(entities)
        elif intent == "search_web":
            self.search_web(entities)
        elif intent == "calculations":
            self.perform_calculations(entities)
        elif intent == "health":
            self.get_health_info(entities)
        elif intent == "riddle":
            self.tell_riddle()
        elif intent == "roll_dice":
            self.roll_dice()
        elif intent == "sing_song":
            self.sing_song()
        else:
            self.google_tts("I'm not sure how to respond to that.")

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

    def get_weather(self):
        # Implement weather functionality
        self.google_tts("I'm sorry, I don't have the weather information right now.")

    def tell_joke(self):
        # Implement joke functionality
        joke_text = "Why don't scientists trust atoms? Because they make up everything!"
        self.google_tts(joke_text)

    def get_president_info(self):
        # Implement president information functionality
        self.google_tts("I'm sorry, I don't have information about the president right now.")

    def get_capital_info(self):
        # Implement capital information functionality
        self.google_tts("I'm sorry, I don't have information about capitals right now.")

    def set_timer(self, entities):
        # Implement timer functionality
        duration = 0
        for ent, label in entities:
            if label == "TIME":
                duration = int(ent.split()[0])
                break

        if duration > 0:
            self.google_tts(f"Sure, I will set a timer for {duration} minutes.")
        else:
            self.google_tts("I'm sorry, I couldn't understand the timer duration.")

    def get_calendar_info(self):
        # Implement calendar information functionality
        self.google_tts("I'm sorry, I don't have calendar information right now.")

    def send_text_message(self, entities):
        # Implement sending text message functionality
        contact = None
        message = None

        for ent, label in entities:
            if label == "CONTACT":
                contact = ent
            elif label == "MESSAGE":
                message = ent

        if contact and message:
            self.google_tts(f"Sure, I will send a text to {contact} saying: {message}")
        else:
            self.google_tts("I'm sorry, I couldn't understand the contact or message.")

    def make_call(self, entities):
        # Implement making a call functionality
        contact = None

        for ent, label in entities:
            if label == "CONTACT":
                contact = ent

        if contact:
            self.google_tts(f"Sure, I will call {contact}.")
        else:
            self.google_tts("I'm sorry, I couldn't understand the contact.")

    def get_directions(self, entities):
        # Implement getting directions functionality
        location = None

        for ent, label in entities:
            if label == "LOCATION":
                location = ent

        if location:
            self.google_tts(f"Sure, I will give you directions to {location}.")
        else:
            self.google_tts("I'm sorry, I couldn't understand the location.")

    def play_music(self, entities):
        # Implement playing music functionality
        song = None
        for ent, label in entities:
            if label == "SONG":
                song = ent

        if song:
            self.google_tts(f"Sure, I will play {song} on your preferred music service.")
            # Implement the logic to play the specified song on the music service of your choice
        else:
            self.google_tts("I'm sorry, I couldn't understand the song.")

    def get_movies_info(self):
        # Implement movies information functionality
        self.google_tts("I'm sorry, I don't have information about movies right now.")

    def tell_story(self):
        # Implement telling a story functionality
        story_text = "Once upon a time, in a land far, far away..."
        self.google_tts(story_text)

    def control_smart_home(self, entities):
        # Implement smart home control functionality
        action = None

        for ent, label in entities:
            if label == "SMART_HOME_ACTION":
                action = ent

        if action:
            self.google_tts(f"Sure, I will {action} in your smart home.")
            # Implement the logic to control your smart home devices
        else:
            self.google_tts("I'm sorry, I couldn't understand the smart home action.")

    def add_to_shopping_list(self, entities):
        # Implement adding to shopping list functionality
        item = None

        for ent, label in entities:
            if label == "SHOPPING_ITEM":
                item = ent

        if item:
            self.google_tts(f"Sure, I will add {item} to your shopping list.")
            # Implement the logic to add the item to the shopping list
        else:
            self.google_tts("I'm sorry, I couldn't understand the shopping item.")

    def get_to_do_list_info(self):
        # Implement getting to-do list information functionality
        self.google_tts("I'm sorry, I don't have information about your to-do list right now.")

    def order_online(self, entities):
        # Implement online ordering functionality
        product = None
        store = None

        for ent, label in entities:
            if label == "PRODUCT":
                product = ent
            elif label == "ONLINE_STORE":
                store = ent

        if product and store:
            self.google_tts(f"Sure, I will order {product} from {store} for you.")
            # Implement the logic to place an order online
        else:
            self.google_tts("I'm sorry, I couldn't understand the product or online store.")

    def translate_text(self, entities):
        # Implement language translation functionality
        text = None
        target_language = None

        for ent, label in entities:
            if label == "TRANSLATION_TEXT":
                text = ent
            elif label == "TARGET_LANGUAGE":
                target_language = ent

        if text and target_language:
            self.google_tts(f"Sure, I will translate '{text}' to {target_language}.")
            # Implement the logic to perform language translation
        else:
            self.google_tts("I'm sorry, I couldn't understand the text or target language.")

    def search_web(self, entities):
        # Implement web search functionality
        query = None

        for ent, label in entities:
            if label == "SEARCH_QUERY":
                query = ent

        if query:
            self.google_tts(f"Sure, I will search the web for '{query}'.")
            # Implement the logic to perform a web search
        else:
            self.google_tts("I'm sorry, I couldn't understand the search query.")

    def perform_calculations(self, entities):
        # Implement calculations functionality
        math_expression = None

        for ent, label in entities:
            if label == "MATH_EXPRESSION":
                math_expression = ent

        if math_expression:
            try:
                result = eval(math_expression)
                self.google_tts(f"The result is {result}.")
            except Exception as e:
                self.google_tts("I'm sorry, there was an error in the calculation.")
        else:
            self.google_tts("I'm sorry, I couldn't understand the math expression.")

    def get_health_info(self, entities):
        # Implement health information functionality
        query = None

        for ent, label in entities:
            if label == "HEALTH_QUERY":
                query = ent

        if query:
            self.google_tts(f"I'm sorry, I don't have information about '{query}' right now.")
        else:
            self.google_tts("I'm sorry, I couldn't understand the health query.")

    def tell_riddle(self):
        # Implement telling a riddle functionality
        riddle_text = "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?"
        self.google_tts(riddle_text)

    def roll_dice(self):
        # Implement rolling a dice functionality
        import random
        result = random.randint(1, 6)
        self.google_tts(f"The dice rolled and you got {result}.")

    def sing_song(self):
        # Implement singing a song functionality
        song_lyrics = "I'm sorry, I don't know any songs. How about I tell you a joke instead?"
        self.google_tts(song_lyrics)

    # Example usage
    if __name__ == "__main__":
        NLPModule = NLPModule()

        while True:
            intent, entities = NLPModule.process_voice()

            # If voice input wasn't understood, prompt for text input
            if intent is None:
                user_input = input("You (text): ")
                intent, entities = NLPModule.process_text(user_input)

            user_exit = input("Enter 'exit' to quit, or press Enter to continue: ")
            if user_exit.lower() == 'exit':
                print("shutting down...!")
                break
