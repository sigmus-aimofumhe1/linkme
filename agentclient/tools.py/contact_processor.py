import json
import re
import smtplib
import psycopg2
from email.mime.text import MIMEText
from openai import OpenAI
from twilio.rest import Client as TwilioClient

# CONFIGS
XAI_API_KEY = "xai-..."  # replace with your real key
TWILIO_SID = "AC7e2a875541c9bafa6ae6fc91ee980a0d"
TWILIO_AUTH_TOKEN = "ea06ddaa7661e1f7e1908fa63ebd2988"
TWILIO_PHONE = "+1234567890"  # your Twilio number
EMAIL_USER = "eshiobomhesigmusaimofumhe04@gmail.com"
EMAIL_PASSWORD = "Sigmu$100"

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "dydxdydx1000",
    "host": "localhost",
    "port": 5432
}

# OpenAI client
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# Twilio client
twilio_client = TwilioClient(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Extract contact values (very simple regexes)
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'(\+?\d[\d\s-]{7,})', text)
    return match.group().strip() if match else None

# Email sender
def send_email(recipient, body):
    msg = MIMEText(body)
    msg["Subject"] = "Hello from your assistant"
    msg["From"] = EMAIL_USER
    msg["To"] = recipient

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
    print("✅ Email sent to", recipient)

# SMS sender
def send_sms(recipient, body):
    twilio_client.messages.create(
        body=body,
        from_=TWILIO_PHONE,
        to=recipient
    )
    print("✅ SMS sent to", recipient)

# Main detection and flow logic
def detect_and_store(text):
    prompt = f"""
Check if the following text contains:
- Email
- Phone number
- LinkedIn profile link

Text: "{text}"

Respond in JSON like: {{"email": true/false, "phone": true/false, "linkedin": true/false}}
"""

    response = client.chat.completions.create(
        model="grok-3-beta",
        messages=[
            {"role": "system", "content": "You are Grok, a highly intelligent assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        result = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print("❌ Bad JSON response:", response.choices[0].message.content)
        return

    # Insert the raw text into database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO mitai (text) VALUES (%s)", (text,))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Inserted into DB:", text)

    # Optional message
    message = "Hey there! Thanks for sharing your contact info."

    # Send email if present
    if result.get("email"):
        email = extract_email(text)
        if email:
            send_email(email, message)

    # Send SMS if present
    if result.get("phone"):
        phone = extract_phone(text)
        if phone:
            send_sms(phone, message)

# Example usage
detect_and_store("Reach me at emeka2025@yahoo.com or call +14155552671 or visit linkedin.com/in/emeka-ai")
