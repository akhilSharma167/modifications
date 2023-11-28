from email.mime.text import MIMEText
from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer
import imutils
import dlib
import cv2
import smtplib
import time
import html

mixer.init()
mixer.music.load("music1.wav")  # Use a different sound for taking rest alert
ten = mixer.Sound("break.wav")  # Use a different sound for taking rest alert

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap = cv2.VideoCapture(0)
flag = 0
alarm_count = 0  # Initialize the alarm count
last_alert_time = time.time()  # Initialize the last alert time
start_time = time.time()



# Function to send an email
def send_email(receiver_email, subject, body):
    # Email configuration
    sender_email = 'akhilsharma1672k@gmail.com'
    sender_password = 'hlty sgwd gylq ddko'

    # Create a connection to the SMTP server
    smtp_server = 'smtp.gmail.com'  # Use your email provider's SMTP server
    smtp_port = 587  # Port for TLS/STARTTLS
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Log in to your email account
    server.login(sender_email, sender_password)

    # Compose the email
    msg = MIMEText(body, 'plain')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Send the email
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)

    # Quit the server
    server.quit()


    print(f'Email sent successfully to {receiver_email}!')
# Function to generate a link for the user to input their latitude and longitude
def generate_input_link():
    # Replace with the actual URL of your input form
    text = "This is some text. Click 'https://www.google.com/search?q=hotel+nearby+me&oq=hotel+nearby+me&aqs=chrome..69i57j0i131i273i433i457i650j0i402i650l2j0i10i512l11.10385j1j4&client=ms-android-samsung-ga-rev1&sourceid=chrome-mobile&ie=UTF-8'> to go to Example.com."
    escaped_text = html.escape(text)
    return text

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        if ear < thresh:
            flag += 1
            if flag >= frame_check:
                cv2.putText(frame, "****************Wake up!****************", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "****************ALERT!****************", (10, 325),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                if flag == frame_check:
                    alarm_count += 1  # Increment the alarm count by one
                mixer.music.play()
        else:
            flag = 0
        elapsed_time = int(time.time() - start_time)
        cv2.putText(frame, f"Time: {elapsed_time}s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the alarm count on the frame
    cv2.putText(frame, f"Alarms: {alarm_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Check if 20 seconds have passed since the last alert
    current_time = time.time()
    if current_time - last_alert_time >= 20:
        # Play the rest alert sound
        ten.play()
        
        # Send an email with the hotel link
        link = generate_input_link()

        # Compose the email subject and body
        email_subject = 'Take a Break and Find a Nearby Hotel'
        email_body = f'Hello,\n\nYou can find a hotel nearby your location by entering your latitude and longitude here:\n {link}'

        # Specify the receiver's email address
        receiver_email = 'as8492876950@gmail.com'

        # Send the email
        send_email(receiver_email, email_subject, email_body)
       
        
        
        # Update the last alert time
        last_alert_time = current_time

    if alarm_count == 5:  # Check if alarm_count is equal to 5
        # Get the live location using a geolocation service
        # Implement this function to fetch the location

        # Compose an alert message
        email_subject = 'Driver Alert: Sleepy'
        email_body = 'Driver is feeling sleepy. Please check on them.'

        # Specify the receiver's email address for the second email
        second_receiver_email = 'shamasharma883@gmail.com'  # Replace with the second receiver's email address

        # Send the second email
        send_email(second_receiver_email, email_subject, email_body)
        
        # Reset the alarm count
        alarm_count = 0

    cv2.imshow("DriverGuard\nPress q to exit", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

print("Total alarms triggered:", alarm_count)  # Print the total alarm count
cv2.destroyAllWindows()
cap.release()
