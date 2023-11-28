import speech_recognition as sr
from gtts import gTTS
import pygame
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class FreyaAssistant:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.recognizer = sr.Recognizer()
        self.initialize_pygame()

    def initialize_pygame(self):
        pygame.init()
        pygame.mixer.init()

    def listen(self):
        with sr.Microphone() as source:
            print("Freya: Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            user_input = self.recognizer.recognize_google(audio)
            print("You:", user_input)
            return user_input
        except sr.UnknownValueError:
            print("Freya: Sorry, I didn't catch that. Can you repeat?")
            return ""
        except sr.RequestError as e:
            print(f"Freya: There was an error with the speech recognition service: {e}")
            return ""

    def generate_response(self, user_input):
        # Ensure user input ends with a question mark
        if not user_input.endswith("?"):
            user_input += "?"

        input_ids = self.tokenizer.encode(user_input, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=50, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=1)

        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    def speak(self, text):
        # Use gTTS for text-to-speech synthesis
        tts = gTTS(text, lang='en', slow=False)  # You can set slow to True for a more natural pace
        tts.save("output.mp3")

        # Play the audio file using pygame
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        # Wait for the end of the audio playback
        pygame.event.wait()

        # Delete the audio file
        os.remove("output.mp3")

if __name__ == "__main__":
    freya = FreyaAssistant()

    # Speak the initial greeting
    freya.speak("Hi! I'm Freya, your virtual assistant.")

    while True:
        user_input = freya.listen()
        if user_input.lower() == 'quit':
            break
        response = freya.generate_response(user_input)
        print("Freya:", response)
        freya.speak(response)
