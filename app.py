from email.mime.text import MIMEText
from flask import Flask, render_template, Response
import cv2
import imutils
from imutils import face_utils
from scipy.spatial import distance
import dlib
from pygame import mixer
import subprocess
import smtplib
import time
import html

# Initialize Flask
app = Flask(__name__)
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



def send_email(receiver_email, subject, body):
    # Email configuration
    sender_email = 'akhilsharma1672k@gmail.com'
    sender_password = 'hlty sgwd gylq ddko'

    # Create the email message
    msg = MIMEText(body, 'plain')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Connect to the SMTP server and send the email
    try:
        smtp_server = 'smtp.gmail.com'  # Use your email provider's SMTP server
        smtp_port = 587  # Port for TLS/STARTTLS
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

    # Log in to your email account
        server.login(sender_email, sender_password)    
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)


    # Quit the server
        server.quit()
        print(f'Email sent successfully to {receiver_email}!')
    except Exception as e:
        print(f"Error sending email: {str(e)}")
def generate_input_link():
    # Replace with the actual URL of your input form
    text = " Click 'https://www.google.com/search?q=hotel+nearby+me&oq=hotel+nearby+me&aqs=chrome..69i57j0i131i273i433i457i650j0i402i650l2j0i10i512l11.10385j1j4&client=ms-android-samsung-ga-rev1&sourceid=chrome-mobile&ie=UTF-8' "
    escaped_text = html.escape(text)
    return text

# Define your drowsiness detection logic and other functions here (e.g., `eye_aspect_ratio`, `send_email`, etc.).
# These functions are used for drowsiness detection and email alerts.


# Define your route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define your video streaming function
def generate_frames():
    # Capture video frames, perform drowsiness detection, and yield frames for streaming
    # This function should contain your drowsiness detection code as well.
    # Ensure you have the necessary imports and global variables here.
   
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

# Your existing code...

# Inside your main loop
# Inside your main loop

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
            email_body = f'Hello,\n\nYou can find a hotel nearby hotel:\n {link}'

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




# Define your video feed route
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Define a route to start the drowsiness detection in a separate window
@app.route('/start_detection')
def start_detection():
    # Execute the drowsiness_detection.py script in a separate process
    subprocess.Popen(['python', 'drowsiness_detection.py'])
    return generate_frames()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)







































# from flask import Flask, render_template,Response
# import subprocess


# app = Flask(__name__)

# # Your existing setup code...

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/start_detection')
# def start_detection():
#     # Execute the drowsiness detection script in a separate process
#     subprocess.Popen(['python', 'drowsiness_detection.py'])
#     return "Detection started in a separate window."

# # Your existing Flask app setup code...
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



# if __name__ == '__main__':
#     app.run(debug=True)
























































# from flask import Flask, render_template, Response
# import cv2
# import imutils
# from imutils import face_utils
# from scipy.spatial import distance
# import dlib
# from pygame import mixer

# app = Flask(__name__)
# mixer.init()
# mixer.music.load("music.wav")

# def eye_aspect_ratio(eye):
#     A = distance.euclidean(eye[1], eye[5])
#     B = distance.euclidean(eye[2], eye[4])
#     C = distance.euclidean(eye[0], eye[3])
#     ear = (A + B) / (2.0 * C)
#     return ear

# thresh = 0.25
# frame_check = 20
# detect = dlib.get_frontal_face_detector()
# predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
# cap = cv2.VideoCapture(0)
# flag = 0
# alarm_count = 0  # Initialize the alarm count


# # Your existing code for sending emails and other functions...

# @app.route('/')
# def index():
#     return render_template('index.html')

# def generate_frames():
#     while True:
#         ret, frame = cap.read()
#         frame = imutils.resize(frame, width=450)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         subjects = detect(gray, 0)
#         for subject in subjects:
#             shape = predict(gray, subject)
#             shape = face_utils.shape_to_np(shape)
#             leftEye = shape[lStart:lEnd]
#             rightEye = shape[rStart:rEnd]
#             leftEAR = eye_aspect_ratio(leftEye)
#             rightEAR = eye_aspect_ratio(rightEye)
#             ear = (leftEAR + rightEAR) / 2.0
#             leftEyeHull = cv2.convexHull(leftEye)
#             rightEyeHull = cv2.convexHull(rightEye)
#             cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
#             cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
#             if ear < thresh:
#                 flag += 1
#                 if flag >= frame_check:
#                     cv2.putText(frame, "****************Wake up!****************", (10, 30),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                     cv2.putText(frame, "****************ALERT!****************", (10, 325),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                     if flag == frame_check:
#                         # alarm_count += 1  # Increment the alarm count by one
#                       mixer.music.play()
#             else:
#                 flag = 0

#         # Display the alarm count on the frame
#         # cv2.putText(frame, f"Alarms: {alarm_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         # if alarm_count == 5:  # Check if alarm_count is equal to 5
#         #     # Get the live location using a geolocation service
#         #      # Implement this function to fetch the location

#         #     # Compose an alert message
#         #     alert_message = "Driver is feeling sleepy. Please check on them."

#         #     # Send an email notification with the alert and live location
#         #    # send_email(alert_message)
            
#         #     # Reset the alarm count
#         #     alarm_count = 0

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(debug=True)

