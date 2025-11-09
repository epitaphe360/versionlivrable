"""Tester la connexion avec un compte de test"""
import requests
import json

# URL du backend
API_URL = "http://localhost:8001"

# Compte de test
TEST_EMAIL = "admin@getyourshare.com"
TEST_PASSWORD = "Test123!"

print(f"=== TEST DE CONNEXION ===")
print(f"Email: {TEST_EMAIL}")
print(f"Password: {TEST_PASSWORD}\n")

# Requête de connexion
try:
    response = requests.post(
        f"{API_URL}/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ CONNEXION RÉUSSIE!")
        print(f"Token: {data.get('access_token', 'N/A')[:50]}...")
        print(f"User: {data.get('user', {})}")
    else:
        print(f"❌ ÉCHEC DE CONNEXION")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERREUR: {e}")
