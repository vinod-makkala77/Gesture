import pickle
import cv2
import mediapipe as mp
import numpy as np
import smtplib
from email.message import EmailMessage
import threading


# Load trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Email credentials
YOUR_EMAIL = "makkalavinod70@gmail.com"
YOUR_PASSWORD = "qgjv xwrc upwp wzyi"  # app password

# Initialize camera
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Labels
labels_dict = {0: 'A', 1: 'M', 2: 'N', 3: 'S', 4: 'T'}

# Control
alert_sent = set()

def send_email(to_email, subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = YOUR_EMAIL
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(YOUR_EMAIL, YOUR_PASSWORD)
            smtp.send_message(msg)
        print(f"Email alert sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            data_aux = []
            x_ = []
            y_ = []

            for lm in hand_landmarks.landmark:
                x_.append(lm.x)
                y_.append(lm.y)

            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min(x_))
                data_aux.append(lm.y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) + 10
            y2 = int(max(y_) * H) + 10

            prediction = model.predict([np.asarray(data_aux)])
            letter = labels_dict[int(prediction[0])]

            # Only these letters trigger emails
            if letter in ['T', 'S', 'A', 'N'] and letter not in alert_sent:
                alert_sent.add(letter)

                if letter == 'T':
                    subject = "Theft Emergency Alert"
                    content = "Dear Sir/Madam, Someone is attempting to steal or break into my house. Please send immediate police assistance.Address: House No. 123, City: ABCKindly treat this as an urgent matter and help me stay safe.Thank you."
                    to_email = "pk6576367@gmail.com"
                elif letter == 'S':
                    subject = "Fire Emergency Alert"
                    content = "Dear Sir/Madam,There is a fire in my house, and it is spreading quickly. Please dispatch the fire department immediately.Address: House No. 123, City: ABCWe need urgent help to evacuate and control the fire. Thank you."
                    to_email = "darlingkk440@gmail.com"
                elif letter in ['A', 'N']:
                    subject = "Medical Emergency Alert"
                    content = "Dear Sir/Madam,I am facing a severe medical emergency (accident/pregnancy emergency). Immediate ambulance service is required. Please coordinate with the nearest hospital.Address: House No. 123, City: ABDKindly help me reach the hospital at the earliest possible.Thank you."
                    to_email = "makkalaramulu6@gmail.com"
                
                threading.Thread(target=send_email, args=(to_email, subject, content)).start()

            # draw
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, letter, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

    cv2.imshow("Hand Gesture Emergency System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
