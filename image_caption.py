# b50e409e075440618ff3cd08708e013e

# b50e409e075440618ff3cd08708e013e

from newsapi import NewsApiClient
from gtts import gTTS
import os
from googletrans import Translator
from playsound import playsound
translator = Translator()
# Define a function to speak the text
def speak(text):
    tts = gTTS(text, lang='hi')  # Create a gTTS object
    tts.save('output.mp3')  # Save the synthesized speech as an MP3 file
    playsound('output.mp3')
    os.remove('output.mp3') 
# Initialize the News API client with your API key
newsapi = NewsApiClient(api_key='b50e409e075440618ff3cd08708e013e')  # Replace with your actual API key

# Define keywords related to visual impairment, blindness, and eye health
keywords = 'Braille OR visual-impairment OR blindness OR eyecare OR blind OR low-vision OR visually-impaired OR vision-loss OR eye-health OR ophthalmology OR optometry OR assistive-technology OR accessibility OR inclusive-design OR guide-dog OR white-cane OR retinal-disease OR cataracts OR glaucoma'

# Get top news articles from Indian sources related to the specified keywords
articles = newsapi.get_everything(q=keywords, language='en')

# Process and speak the articles
for i, article in enumerate(articles['articles'][:5], 1):
    print(f"Article {i}:")
    print("Title:", article['title'])
    translation = translator.translate(article['title'], src='en', dest='mr').text

    # Translate title to Marathi
    title_translation = translator.translate(article['title'], src='en', dest='mr').text
    print("Marathi Title:", title_translation)

    # Speak the Marathi title
    speak(title_translation)

    print("Description:", article['description'])

    # Translate description to Marathi
    description_translation = translator.translate(article['description'], src='en', dest='mr').text
    print("Marathi Description:", description_translation)

    # Speak the Marathi description
    speak(description_translation)

    print("Source:", article['source']['name'])
    print("URL:", article['url'])
    print('-' * 30)
