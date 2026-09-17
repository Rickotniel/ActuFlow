import urllib.request
import urllib.parse
import json
import uuid

BASE_URL = "http://127.0.0.1:8000/api"
session_id = str(uuid.uuid4())[:8]
email = f"test_{session_id}@example.com"
password = "TestPassword123!"

print(f"--- 1. Testing Registration for {email} ---")
reg_data = json.dumps({
    "email": email,
    "password": password,
    "prenom": "Test",
    "nom": "User"
}).encode('utf-8')

req = urllib.request.Request(f"{BASE_URL}/utilisateurs/", data=reg_data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print("Response:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("Error:", e.code, e.read().decode('utf-8'))
    exit(1)

print(f"\n--- 2. Testing Login ---")
login_data = json.dumps({
    "email": email,
    "password": password
}).encode('utf-8')

req = urllib.request.Request(f"{BASE_URL}/token/", data=login_data, headers={'Content-Type': 'application/json'})
token = None
try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        res_json = json.loads(response.read().decode('utf-8'))
        token = res_json.get('access')
        print("Got access token:", token is not None)
except urllib.error.HTTPError as e:
    print("Error:", e.code, e.read().decode('utf-8'))
    exit(1)

print(f"\n--- 3. Testing /me endpoint ---")
req = urllib.request.Request(f"{BASE_URL}/utilisateurs/me/", headers={'Authorization': f'Bearer {token}'})
try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        profile = json.loads(response.read().decode('utf-8'))
        print("Profile Email:", profile.get('email'))
        print("Profile Roles:", profile.get('role_names'))
except urllib.error.HTTPError as e:
    print("Error:", e.code, e.read().decode('utf-8'))
    exit(1)

print("\nALL TESTS PASSED!")
