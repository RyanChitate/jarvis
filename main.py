import spacy
import speech_recognition as sr

class NLPModule:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

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
                    return intent, entities
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand your voice. Please try again.")

    def determine_intent(self, doc):
        greetings = ["hello", "hi", "hey"]
        goodbyes = ["bye", "goodbye", "see you", "farewell"]
        reminder = ["remind","reminder",]

        for token in doc:
            if token.text.lower() in greetings:
                return "greet"
            elif token.text.lower() in goodbyes:
                return "goodbye"
            elif token.text.lower() in reminder:
                return "reminder"

        return "unknown"

# Example usage
if __name__ == "__main__":
    nlp_module = NLPModule()

    while True:
        intent, entities = nlp_module.process_voice()

        # If voice input wasn't understood, prompt for text input
        if intent is None:
            user_input = input("You (text): ")
            intent, entities = nlp_module.process_text(user_input)

        print("Intent:", intent)
        print("Entities:", entities)

        user_exit = input("Enter 'exit' to quit, or press Enter to continue: ")
        if user_exit.lower() == 'exit':
            print("shutting down...!")
            break
