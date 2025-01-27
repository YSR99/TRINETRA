import cv2
import mediapipe as mp
import time
import random
import numpy as np
from twilio.rest import Client  # Import Twilio for sending SMS

class FaceDetector():
    def __init__(self, minDetectionCon=0.5):
        # Initializing the FaceDetector with the minimum detection confidence threshold
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection  # Mediapipe's face detection module
        self.mpDraw = mp.solutions.drawing_utils  # For drawing bounding boxes
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)  # Face detection object

    def send_alert(self, message):
        """
        Sends an alert SMS to a specified phone number using Twilio
        :param message: The message to be sent
        """
        # Twilio credentials
        account_sid = ''  # Replace with your Twilio Account SID
        auth_token = ''    # Replace with your Twilio Auth Token
        from_number = ''  # Replace with your Twilio phone number
        to_number = ''  # Replace with the recipient phone number

        # Initialize Twilio client and send SMS
        client = Client(account_sid, auth_token)  # Create Twilio client
        client.messages.create(body=message, from_=from_number, to=to_number)  # Send SMS

    def findFaces(self, img, draw=True):
        """
        Detect faces in the image, draw bounding boxes, and send alerts if Bed 1 is not detected.
        :param img: The input image for face detection
        :param draw: Boolean to determine whether to draw bounding boxes on faces
        :return: The image with bounding boxes and a list of detected bounding boxes
        """
        # Convert the image to RGB for Mediapipe processing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)  # Process the image for face detection
        bboxs = []  # List to store bounding boxes
        bed1_detected = False  # Flag to check if Bed 1 is detected

        if self.results.detections:  # If faces are detected
            for id, detection in enumerate(self.results.detections):  # Iterate through detections
                bboxC = detection.location_data.relative_bounding_box  # Get bounding box coordinates
                ih, iw, ic = img.shape  # Get image height, width, and channels
                # Calculate bounding box coordinates in pixels
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])  # Append bounding box information to the list

                if draw:  # If drawing is enabled
                    img = self.fancyDraw(img, bbox)  # Draw bounding boxes on the image

                    # Create labels and heart rate for the faces detected
                    label = f"Bed.{id + 1}"  # Label each detected bed (e.g., Bed.1, Bed.2)
                    heart_rate = f"Heart Rate: {np.random.randint(70, 81)} BPM"  # Random heart rate for the label

                    # Draw the label and heart rate on the image near the bounding box
                    cv2.putText(img, label, (bbox[0], bbox[1] - 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    cv2.putText(img, heart_rate, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    # Check if Bed 1 is detected
                    if label == "Bed.1":
                        bed1_detected = True  # Set the flag to True if Bed 1 is detected

        # If Bed 1 is not detected, send an alert
        if not bed1_detected:
            self.send_alert("Alert: Bed 1 is not detected!")  # Send alert SMS

        return img, bboxs  # Return the processed image and bounding boxes

    def fancyDraw(self, img, bbox, l=30, t=5, rt=1):
        """
        Draws a fancy bounding box around the detected face.
        :param img: The image to draw on
        :param bbox: The bounding box coordinates (x, y, width, height)
        :param l: Length of the lines at the corners of the bounding box
        :param t: Thickness of the lines at the corners
        :param rt: The thickness of the rectangle
        :return: The image with the drawn bounding box
        """
        x, y, w, h = bbox  # Get the coordinates and dimensions of the bounding box
        x1, y1 = x + w, y + h  # Calculate the bottom-right corner of the bounding box

        # Draw a rectangle around the bounding box
        cv2.rectangle(img, bbox, (255, 0, 255), rt)

        # Draw lines at the top-left corner
        cv2.line(img, (x, y), (x + l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y + l), (255, 0, 255), t)
        # Draw lines at the top-right corner
        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + l), (255, 0, 255), t)
        # Draw lines at the bottom-left corner
        cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
        # Draw lines at the bottom-right corner
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)

        return img  # Return the image with the fancy bounding box

def main():
    # Open the webcam
    cap = cv2.VideoCapture(0)  # 0 for default webcam

    # Check if the webcam is opened
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    pTime = 0  # Variable to store previous time for FPS calculation
    detector = FaceDetector()  # Initialize the face detector

    while True:
        success, img = cap.read()  # Read a frame from the webcam
        if not success:
            print("Error: Could not read frame.")
            break

        img, bboxs = detector.findFaces(img)  # Detect faces and draw bounding boxes on the image
        print(bboxs)  # Print bounding boxes (for debugging)

        # Calculate FPS (frames per second)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        # Display the image with bounding boxes
        cv2.imshow("Live Face Detection", img)  # Display frame in local window

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close the OpenCV windows

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
