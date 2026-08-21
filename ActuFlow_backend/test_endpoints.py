#!/usr/bin/env python
"""
Script de test pour les endpoints ActuFlow
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("="*70)
print("🧪 TEST DES ENDPOINTS ACTUFLOW")
print("="*70)

# 1. Test token
print("\n1️⃣  OBTENIR UN TOKEN")
print("-"*70)
response = requests.post(
    f"{BASE_URL}/token/",
    json={"email": "admin@example.com", "password": "admin123"}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    tokens = response.json()
    access_token = tokens['access']
    print("✅ Token obtenu !")
    print(f"   Access Token: {access_token[:50]}...")
else:
    print(f"❌ Erreur: {response.json()}")
    access_token = None

# 2. Test Swagger
print("\n2️⃣  VÉRIFIER LES ENDPOINTS SWAGGER")
print("-"*70)
response = requests.get(f"{BASE_URL}/../swagger/")
if response.status_code == 200:
    print("✅ Swagger accessible à /swagger/")
else:
    print(f"❌ Erreur d'accès à Swagger: {response.status_code}")

# 3. Test endpoints CRUD disponibles
if access_token:
    print("\n3️⃣  TEST DES ENDPOINTS CRUD")
    print("-"*70)
    
    endpoints_to_test = [
        ("/users/", "GET", "Lister les utilisateurs"),
        ("/articles/", "GET", "Lister les articles"),
        ("/categories/", "GET", "Lister les catégories"),
        ("/comments/", "GET", "Lister les commentaires"),
        ("/favorites/", "GET", "Lister les favoris"),
        ("/notifications/", "GET", "Lister les notifications"),
        ("/audit/", "GET", "Lister les logs d'audit"),
        ("/roles/roles/", "GET", "Lister les rôles"),
    ]
    
    for endpoint, method, description in endpoints_to_test:
        try:
            response = requests.request(
                method,
                f"{BASE_URL}{endpoint}",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            status_ok = response.status_code in [200, 400, 403]
            symbol = "✅" if status_ok else "❌"
            print(f"{symbol} {description}: {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: Erreur de connexion")

print("\n" + "="*70)
print("✅ TESTS TERMINÉS - Accédez à http://127.0.0.1:8000/swagger/")
print("="*70)
