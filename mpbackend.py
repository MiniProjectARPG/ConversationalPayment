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