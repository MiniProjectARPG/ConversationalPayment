from flask import Flask, request, jsonify
import razorpay
import requests
import hashlib
import json
import spacy
import re

app = Flask(_name_)

# Razorpay API Keys (replace with your actual Razorpay API Key ID and Secret)
RAZORPAY_KEY_ID = 'YOUR_RAZORPAY_KEY_ID'
RAZORPAY_KEY_SECRET = 'YOUR_RAZORPAY_KEY_SECRET'

# PhonePe API credentials (replace with your actual details)
PHONEPE_MERCHANT_ID = "YOUR_PHONEPE_MERCHANT_ID"
PHONEPE_MERCHANT_KEY = "YOUR_PHONEPE_MERCHANT_KEY"
PHONEPE_SALT_KEY = "YOUR_PHONEPE_SALT_KEY"
PHONEPE_BASE_URL = "https://api.phonepe.com/apis/hermes/v1/"  # Use sandbox or production based on environment

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Helper function to process user command
def process_command(command):
    doc = nlp(command)
    amount = None
    recipient = None
    payment_type = None

    # Extract relevant info using spaCy and regex
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            amount = re.findall(r'\d+', ent.text)[0]
        elif ent.label_ == "PERSON" or ent.label_ == "ORG":
            recipient = ent.text

    # Check for payment type in the command
    if "razorpay" in command.lower():
        payment_type = "razorpay"
    elif "phonepe" in command.lower():
        payment_type = "phonepe"

    return amount, recipient, payment_type

# Route to serve the frontend
@app.route('/')
def index():
    return "Payment Integration API Server Running"

# Route to initiate payment via Razorpay or PhonePe based on command
@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    command = data.get('command')  # Get user command

    # Process the command using NLP
    amount, recipient, payment_type = process_command(command)

    if not amount or not recipient or not payment_type:
        return jsonify({
            'error': 'Could not interpret the command. Please provide amount, recipient, and payment method.'
        }), 400

    # Call respective payment method based on the extracted payment type
    if payment_type == "razorpay":
        return razorpay_payment(amount, recipient)
    elif payment_type == "phonepe":
        return phonepe_payment(amount, recipient)
    else:
        return jsonify({'error': 'Payment method not recognized.'}), 400

# Function to handle Razorpay payment
def razorpay_payment(amount, recipient):
    # Create order in Razorpay
    order = razorpay_client.order.create({
        "amount": int(amount) * 100,  # Amount in paise
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify({
        'order_id': order['id'],
        'amount': amount,
        'recipient': recipient,
        'payment_link': f"https://checkout.razorpay.com/v1/checkout.js"
    })
