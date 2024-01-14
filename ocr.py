import cv2
import pytesseract
import pyttsx3

class Read():
    # Load the video
    # Replace with the path to your video file
    cap = cv2.VideoCapture(0)

    # Create a TTS engine
    engine = pyttsx3.init()

    # Set up Tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = r"C:\Python\Lib\site-packages\Tesseract-OCR\tesseract.exe"

    while True:
        # Capture a frame from the video
        ret, frame = cap.read()

        if not ret:
            # Break the loop if end of video
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        
        # Perform text detection using Tesseract OCR
        detected_text = pytesseract.image_to_string(gray)

        # Remove leading/trailing whitespaces and filter out empty lines
        detected_text = '\n'.join(line.strip() for line in detected_text.split('\n') if line.strip())
        print(detected_text)
        # Display the grayscale frame
        cv2.imshow('Video', gray)

        # Use TTS to read the detected text
        engine.say(detected_text)
        engine.runAndWait()

        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
