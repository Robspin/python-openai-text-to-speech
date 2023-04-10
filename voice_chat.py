import openai
import pyttsx3
import speech_recognition as sr

openai.api_key = ""


engine = pyttsx3.init()
voice = engine.getProperty('voices')


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(e)


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        # Wait for user to say "akira"
        print("Say 'gpt' to start recording")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "gpt":
                    # Record audio
                    filename = "input.wav"
                    print("State your question...")
                    with sr.Microphone() as question_source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(question_source, phrase_time_limit=None, timeout=None)
                        print(audio)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        # Generate response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        # Read response using text-to-speak
                        speak_text(response)
            except KeyboardInterrupt:
                print("exited...")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()

