import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import qrcode
from transformers import pipeline

# Initialize the speech recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice to female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Personal Data
personal_data = {
    'name': 'Muhammed Adnan',
    'age': 19,
    'location': 'Kerala, India',
    'profession': 'Front-End Developer & PWA Specialist',
    'agency': 'Ad Web Comic Agency',
}

# AI Model initialization (Placeholder using GPT-2 as an example)
ai_model = pipeline("text-generation", model="gpt2")  # Adjust if using a specific API

def talk(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listens for a voice command and returns it as text."""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            if 'tejo' in command:  # Replace 'tejo' with your activation keyword
                command = command.replace('tejo', '').strip()
            return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def generate_qr_code(data):
    """Generates a QR Code and saves it as an image file."""
    try:
        img = qrcode.make(data)
        img.save("qrcode.png")
        talk("QR Code generated successfully!")
    except Exception as e:
        print(f"Error generating QR Code: {e}")
        talk("Failed to generate the QR Code.")

def ai_message(input_text):
    """Uses AI to generate a response."""
    try:
        response = ai_model(input_text, max_length=100, num_return_sequences=1)
        return response[0]['generated_text']
    except Exception as e:
        print(f"AI model error: {e}")
        return "I'm unable to process that request right now."

def run_tejo():
    """Main function to process voice commands."""
    command = take_command()
    if not command:
        return True

    print(f"Command: {command}")

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time}")
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        try:
            info = wikipedia.summary(person, sentences=1)
            talk(info)
            print(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results. Please specify.")
            print(f"DisambiguationError: {e}")
        except wikipedia.exceptions.PageError:
            talk("I couldn't find information on that.")
    elif 'date' in command:
        talk("Sorry, I have a headache.")
    elif 'are you single' in command:
        talk("I am in a relationship with WiFi.")
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        print(joke)
    elif 'name' in command:
        talk(f"My name is {personal_data['name']}")
    elif 'age' in command:
        talk(f"I am {personal_data['age']} years old.")
    elif 'location' in command:
        talk(f"I am from {personal_data['location']}.")
    elif 'profession' in command:
        talk(f"I am a {personal_data['profession']}.")
    elif 'agency' in command:
        talk(f"I work at {personal_data['agency']}.")
    elif 'qr code' in command:
        talk("What should the QR Code contain?")
        data = take_command()
        if data:
            generate_qr_code(data)
    elif 'ask' in command:
        talk("What would you like to ask?")
        question = take_command()
        if question:
            answer = ai_message(question)
            talk(answer)
            print(answer)
    elif 'exit' in command or 'stop' in command:
        talk("Goodbye!")
        return False
    else:
        talk("I didn't understand that. Please try again.")
    
    return True

def main():
    """Main loop to continuously listen for commands."""
    talk("Tejo is ready. How can I assist you?")
    while True:
        if not run_tejo():
            break

if __name__ == "__main__":
    main()
