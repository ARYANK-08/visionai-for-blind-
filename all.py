import cv2
import numpy as np
import pyttsx3
from playsound import playsound
from gtts import gTTS
import os 
import pyttsx3
import webbrowser
import datetime
from newsapi import NewsApiClient
from gtts import gTTS
import os
from googletrans import Translator
from playsound import playsound

# Load Yolo
net = cv2.dnn.readNet("dnn_model\yolov4-tiny.weights", "dnn_model\yolov4-tiny.cfg")
classes = []
with open("dnn_model\classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load Text-to-speech engine
engine = pyttsx3.init()

# Starting webcam
cap = cv2.VideoCapture(0)

def open_google_maps():
    # Specify the URL of Google Maps
    url = "https://www.google.com/maps/dir/19.0699698,72.8397314/Lodha+Orchid,+Khoni+-+Taloja+Rd,+Antarli,+Maharashtra+421204,+India/@19.069397,72.835469,16.32z/data=!4m10!4m9!1m1!4e1!1m5!1m1!1s0x3be795c20d83639f:0x6da0435bf2961bd2!2m2!1d73.1189468!2d19.1593427!3e2"
    # Open the URL in the default web browser
    webbrowser.open(url)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, None, fx=1.4, fy=1.4)
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            if label == 'person':
                # Draw rectangle around the person
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                # Calculate position of the person
                pos = ''
                if center_x < width//3:
                    pos = 'बहुत बाएं'
                elif center_x > 2*width//3:
                    pos = 'extreme right'
                elif center_x < width//2:
                    pos = 'बहुत दाएं '
                elif center_x > width//2:
                    pos = 'दाएं '
                else:
                    pos = 'बीच'

                # Calculate distance of the person
                dist = round((2*3.14 * 180) / (w+h*360) * 1000 + 3)

                # Generate sound output
                if dist < 4:               
                    output = f"इंसान {pos} दिखाई दे रहा है और {dist} centimetre दूरी में है"

                    # Create a gTTS object with Hindi as the language
                    language = 'hi'
                    tts = gTTS(output, lang=language, slow=False)
                    # Save the speech to an MP3 file
                    tts.save('output.mp3')

                    # Play the MP3 file using playsound
                    playsound('output.mp3')

                    os.remove('output.mp3')
            else:
                if center_x > width//2:
                    pos = 'दाएं '
                else:
                    pos = 'बीच'


                distance = round((2*3.14 * 180) / (w+h*360) * 1000 + 3)
                if distance < 5:

                    speak_text =f"{label} {pos} दिखाई दे रहा है और {dist} centimetre दूरी में है"
                    print(speak_text)
                    tts = gTTS(speak_text, lang='hi')
                    tts.save('output.mp3')
                    playsound('output.mp3')
                    os.remove('output.mp3')

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)
            cv2.putText(frame, f"Distance: {dist:.2f} cm", (x, y - 50), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    if cv2.waitKey(1) & 0xFF == ord('c'):
            import speech_recognition as sr

            
            # Initialize the speech recognizer and TTS engine
            r = sr.Recognizer()
            text_speech = pyttsx3.init()

            try:
                # Record audio from the microphone
                with sr.Microphone() as source:
                    print("Speak Anything:")
                    audio = r.listen(source)

                # Use speech recognition to recognize the speech
                recognized_text = r.recognize_google(audio)
                print("You said: {}".format(recognized_text))

                # Check if "time" or "open maps" is present in the recognized text
                if "time" in recognized_text.lower():
                    # Get the current time
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")

                    # Use TTS to speak the current time
                    text_speech.say("The current time is {}".format(current_time))
                    text_speech.runAndWait()

                elif "open maps" in recognized_text.lower():
                    # Call the function to open Google Maps
                    open_google_maps()

                elif "status" in recognized_text.lower():
                    speak_text =f"{label} {pos} दिखाई दे रहा है और {dist} centimetre दूरी में है"
                    print(speak_text)
                    tts = gTTS(speak_text, lang='hi')
                    tts.save('output.mp3')
                    playsound('output.mp3')
                    os.remove('output.mp3')

                elif "news" in recognized_text.lower():
                    # b50e409e075440618ff3cd08708e013e

                    # b50e409e075440618ff3cd08708e013e

             
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

                else:
                    print("No keyword 'time' or 'open maps' found in the recognized text.")

            except sr.UnknownValueError:
                print("Speech recognition could not understand the audio.")
            except sr.RequestError:
                print("Speech recognition service unavailable.")

        
    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
