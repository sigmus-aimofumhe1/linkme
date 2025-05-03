# Added by Sigmus
# Message sending logic (with real integrations)

from twilio.rest import Client
from django.core.mail import send_mail
from django.conf import settings
import requests

# Twilio integration for sending SMS/WhatsApp messages
def send_phone_message(phone: str, message: str):
    print(f"Sending WhatsApp/SMS to {phone}: {message}")
    
    # Twilio credentials from your environment or Django settings
    twilio_sid = settings.TWILIO_SID
    twilio_auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(twilio_sid, twilio_auth_token)

    # Send SMS (for WhatsApp, use the 'whatsapp:' prefix before the phone number)
    client.messages.create(
        to=phone,
        from_=twilio_phone_number,
        body=message
    )

# Django email backend integration (using send_mail)
def send_email(email: str, message: str):
    print(f"Sending email to {email}: {message}")
    
    # Send the email using Django's built-in email backend
    send_mail(
        subject="Contact Information",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in settings.py
        recipient_list=[email],
        fail_silently=False,
    )

# LinkedIn message integration (mocked, as LinkedIn API requires special setup)
def send_linkedin_message(linkedin_url: str, message: str):
    print(f"Sending LinkedIn message to {linkedin_url}: {message}")

    # LinkedIn messaging API is restricted, so this part will need to use LinkedIn automation tools
    # or the LinkedIn API (you'll need OAuth2 authorization to send messages on behalf of users).
    
    # Placeholder for LinkedIn messaging logic
    # Example: Sending a LinkedIn message through LinkedIn's API would look something like this:

    access_token = settings.LINKEDIN_ACCESS_TOKEN  # OAuth access token for LinkedIn API
    linkedin_api_url = f"https://api.linkedin.com/v2/messages"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Define the message payload (this will vary depending on LinkedIn's API)
    message_payload = {
        "recipients": [{"person": {"id": linkedin_url}}],
        "body": message
    }

    # Make a POST request to send the message
    response = requests.post(linkedin_api_url, json=message_payload, headers=headers)
    
    if response.status_code == 200:
        print("LinkedIn message sent successfully!")
    else:
        print(f"Failed to send LinkedIn message: {response.status_code} - {response.text}")

