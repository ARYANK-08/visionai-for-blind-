import os
import chainlit as cl
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

os.environ['API_KEY'] = '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'
model_id = 'tiiuae/falcon-7b-instruct'

falcon_llm = HuggingFaceHub(huggingfacehub_api_token=os.environ['API_KEY'],
                            repo_id=model_id,
                            model_kwargs={"temperature":0.8,"max_new_tokens":8000})

template = """
You are an AI assistant that provides helpful answers to user queries.
{question}
"""
prompt = PromptTemplate(template=template, input_variables=['question'])

falcon_chain = LLMChain(llm=falcon_llm,
                        prompt=prompt,
                        verbose=True)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='en')  # Recognize speech using Google's API
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."

def speak(text):
    tts = gTTS(text, lang='hi')  # Create a gTTS object
    tts.save('output.mp3')  # Save the synthesized speech as an MP3 file
    playsound('output.mp3')
    os.remove('output.mp3')  # Play the audio directly

# Example usage
input_text = listen()
print("You said:", input_text)
response = falcon_chain.run(input_text)
from englisttohindi.englisttohindi import EngtoHindi
trans = EngtoHindi(response)
text = trans.convert 
print(text)
speak(text)
