import requests
import json

url = "http://127.0.0.1:8000/api/best-price/bulk"
payload = {
    "queries": ["milk", "chocolate", "eggs", "apple", "carrots", "Ice-cream", "ORANGES"],
    "email": "myash299@gmail.com"
}

try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Email Sent:", response.json().get("email_sent"))
except Exception as e:
    print("Error:", e)
