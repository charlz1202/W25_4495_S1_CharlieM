from dotenv import load_dotenv
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os



# Local API key from Yelp Fusion API
load_dotenv()
API_KEY = os.environ.get('YELP_API_KEY')

# Check if API key is provided
if not API_KEY:
    raise ValueError("No API key provided for Yelp Fusion API. Set the API_KEY environment variable.")

# Yelp API Base URL
BASE_URL = "https://api.yelp.com/v3/businesses/search"

def search_yelp(term, location, category="pets"):
    headers = {
        "Authorization":f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    params = {
        "term": term,
        "location": location,
        "categories": category,
        "limit": 5
    }

    print(f"Sending request to Yelp API with parameters: {params}")
    print(f"API_KEY: {API_KEY}")

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from Yelp API. Status code: {response.text}")
        return {
            "error": f"Failed to fetch data from Yelp API. Status code: {response.status_code}"
        }