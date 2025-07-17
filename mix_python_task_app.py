import streamlit as st
import pywhatkit as kit
import smtplib
import requests
from bs4 import BeautifulSoup
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

# ========================
# ✅ Task 1: WhatsApp Sender
# ========================
def send_whatsapp():
    st.subheader("📱 WhatsApp Auto Message Sender")
    phone = st.text_input("📞 Enter WhatsApp Number (with country code)", value="+91")
    message = st.text_area("💬 Enter Message", value="Hello Krishan!")
    hour = st.number_input("🕐 Hour (0-23)", min_value=0, max_value=23, value=12)
    minute = st.number_input("🕓 Minutes (0-59)", min_value=0, max_value=59, value=30)

    st.markdown("### 📋 Message Summary")
    st.markdown(f"**Phone Number:** {phone}")
    st.markdown(f"**Message:** {message}")
    st.markdown(f"**Scheduled Time:** {hour:02d}:{minute:02d}")

    if st.button("📤 Send WhatsApp Message"):
        try:
            st.info("Opening WhatsApp Web. Please scan QR if not already logged in.")
            kit.sendwhatmsg(phone, message, hour, minute, wait_time=10, tab_close=True)
            st.success("✅ Message Scheduled Successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ========================
# ✅ Task 2: Working Email Sender (with MIME)
# ========================
def send_email():
    st.subheader("📧 Send Email via Gmail (with MIME)")
    sender_email = st.text_input("Your Gmail ID")
    app_password = st.text_input("Gmail App Password", type="password")
    receiver_email = st.text_input("Receiver's Email")
    subject = st.text_input("Subject")
    body = st.text_area("Body")

    if st.button("📨 Send Email"):
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

# ========================
# ✅ Task 3: SMS Sender using Twilio
# ========================
def send_sms():
    st.subheader("💬 Send SMS via Twilio")
    account_sid = st.text_input("Twilio Account SID")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Twilio Phone Number")
    recipient_number = st.text_input("Recipient Number", value="+91")
    message_body = st.text_area("SMS Message", value="Hello! This is a normal SMS sent from Krishan!")

    if st.button("📩 Send SMS"):
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=recipient_number
            )
            st.success(f"✅ SMS Sent Successfully! SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ========================
# ✅ Task 4: Phone Call using Twilio
# ========================
def phone_call():
    st.subheader("📞 Make a Phone Call with Twilio")
    account_sid = st.text_input("Twilio Account SID")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Your Twilio Phone Number")
    target_number = st.text_input("Receiver's Phone Number", value="+91")
    twiml_url = st.text_input("TwiML URL", value="http://demo.twilio.com/docs/voice.xml")

    if st.button("📞 Make Call"):
        try:
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                url=twiml_url,
                to=target_number,
                from_=twilio_number
            )
            st.success(f"✅ Call Initiated Successfully! SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Failed to make call: {e}")

# ========================
# ✅ Task 5: Google Search
# ========================
def open_google():
    st.subheader("🌐 Google Search")
    query = st.text_input("🔍 What do you want to search?")
    if st.button("🔎 Search"):
        webbrowser.open(f"https://www.google.com/search?q={query}")
        st.success("✅ Google opened!")

# ========================
# ✅ Task 6: Website HTML Downloader
# ========================
def download_website_data():
    st.subheader("🖥️ Download Website HTML")
    url = st.text_input("Enter Website URL")
    if st.button("Download HTML"):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            st.text_area("Website HTML Content", soup.prettify(), height=300)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ========================
# ✅ Task 7: Face Swapping
# ========================
def face_swap():
    st.subheader("🧠 Face Swapping")
    st.warning("This feature opens OpenCV window. It runs in command-line, not inside Streamlit UI.")
    run = st.button("📷 Start Face Swapping")
    if run:
        import cv2
        from cvzone.FaceDetectionModule import FaceDetector

        def capture_face(prompt_key):
            while True:
                success, frame = cap.read()
                frame = cv2.flip(frame, 1)
                cv2.imshow("Webcam", frame)
                key = cv2.waitKey(1)
                if key == ord(prompt_key):
                    return frame.copy()

        def perform_face_swap(face1, face2):
            face1 = cv2.resize(face1, (640, 480))
            face2 = cv2.resize(face2, (640, 480))

            face1_detected, bboxs1 = detector.findFaces(face1)
            face2_detected, bboxs2 = detector.findFaces(face2)

            if bboxs1 and bboxs2:
                x1, y1, w1, h1 = bboxs1[0]['bbox']
                x2, y2, w2, h2 = bboxs2[0]['bbox']

                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                w1, h1, w2, h2 = map(int, [w1, h1, w2, h2])

                crop1 = face1[y1:y1+h1, x1:x1+w1]
                crop2 = face2[y2:y2+h2, x2:x2+w2]

                target_w = min(w1, w2)
                target_h = min(h1, h2)

                crop1_resized = cv2.resize(crop1, (target_w, target_h))
                crop2_resized = cv2.resize(crop2, (target_w, target_h))

                face1[y1:y1+target_h, x1:x1+target_w] = crop2_resized
                face2[y2:y2+target_h, x2:x2+target_w] = crop1_resized

                cv2.imshow("Swapped Face 1", face1)
                cv2.imshow("Swapped Face 2", face2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("❌ Face not detected in one or both photos.")

        cap = cv2.VideoCapture(0)
        detector = FaceDetector()

        print("📸 Face Swapper Ready! Press 's' for face1, 'd' for face2, 'q' to quit.")

        while True:
            print("\n📸 Capture Face 1 (Press 's')")
            face1 = capture_face('s')
            print("✅ Face 1 captured.")

            print("📸 Capture Face 2 (Press 'd')")
            face2 = capture_face('d')
            print("✅ Face 2 captured. Swapping...")

            perform_face_swap(face1, face2)

            print("🔁 Press 'q' to quit or any other key to repeat.")
            key = cv2.waitKey(0)
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# ========================
# ✅ Task 8: Digital Image Generator Placeholder
# ========================
def digital_image():
    st.subheader("🖼️ Digital Image")
    st.info("🎨 Use PIL or DALL·E-style AI to generate digital art. Placeholder.")

# ========================
# ✅ Frontend Setup
# ========================
st.set_page_config(page_title="Menu Base Project", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>MENU BASE PROJECT</h1>
    <hr>
""", unsafe_allow_html=True)

# ========================
# ✅ Sidebar Task Selector
# ========================
choice = st.sidebar.selectbox("📋 Select a Task", (
    "1. Whatsapp Message",
    "2. Email",
    "3. SMS (Normal Text Message)",
    "4. Phone Call",
    "5. Google Open",
    "6. Website Data",
    "7. Face Swapping",
    "8. Digital Image"
))

# ========================
# ✅ Task Dispatcher
# ========================
if choice == "1. Whatsapp Message":
    send_whatsapp()
elif choice == "2. Email":
    send_email()
elif choice == "3. SMS (Normal Text Message)":
    send_sms()
elif choice == "4. Phone Call":
    phone_call()
elif choice == "5. Google Open":
    open_google()
elif choice == "6. Website Data":
    download_website_data()
elif choice == "7. Face Swapping":
    face_swap()
elif choice == "8. Digital Image":
    digital_image()
