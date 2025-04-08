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

def search_yelp(term="pet services", location="Vancouver, BC", category=None, attributes=None):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    params = {
        "term": term,
        "location": location,
        "limit": 5
    }

    if category:
        params["categories"] = category
    if attributes:
        params["attributes"] = attributes

    print(f"Yelp Search Params: {params}")

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Yelp API Error: {response.status_code} | {response.text}")
        return {
            "error": f"Failed with status {response.status_code}",
            "details": response.json()
        }