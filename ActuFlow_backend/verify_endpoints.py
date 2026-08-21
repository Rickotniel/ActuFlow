#!/usr/bin/env python
"""
Script de vérification rapide des endpoints
"""
import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("🧪 Vérification des endpoints...")
print("-" * 50)

endpoints = [
    "/articles/",
    "/categories/",
    "/comments/",
    "/favorites/",
    "/notifications/",
    "/audit/",
    "/users/",
    "/roles/roles/",
    "/token/",
]

for endpoint in endpoints:
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        status = "✅" if response.status_code in [200, 401, 403] else "❌"
        print(f"{status} {endpoint:<20} → Status {response.status_code}")
    except Exception as e:
        print(f"❌ {endpoint:<20} → Erreur: {str(e)}")

print("-" * 50)
print("✅ Vérification terminée")
