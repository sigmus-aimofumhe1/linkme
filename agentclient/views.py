from django.shortcuts import render

# Create your views here.
# Added by Sigmus
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .tools.contact_processor import extract_contact_details, classify_contact_type, save_contact
from .tools.messaging import send_phone_message, send_email, send_linkedin_message

@csrf_exempt
def process_contact(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")

        contact_data = extract_contact_details(message)
        contact_type = classify_contact_type(contact_data)
        contact = save_contact(contact_data)

        personalized_msg = f"Hi {contact.name}, great connecting with you!"

        if contact_type == "phone":
            send_phone_message(contact.phone, personalized_msg)
        elif contact_type == "email":
            send_email(contact.email, personalized_msg)
        elif contact_type == "linkedin":
            send_linkedin_message(contact.linkedin, personalized_msg)

        return JsonResponse({"status": "success", "contact_id": contact.id})
    
    return JsonResponse({"error": "Only POST method allowed"}, status=405)

