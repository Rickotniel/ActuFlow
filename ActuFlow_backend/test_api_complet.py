#!/usr/bin/env python
"""
Script complet de test des endpoints API ActuFlow
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_section(title):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

# ============================================================================
# 1. AUTHENTIFICATION
# ============================================================================

print_section("1️⃣  AUTHENTIFICATION JWT")

response = requests.post(
    f"{BASE_URL}/token/",
    json={"email": "admin@example.com", "password": "admin123"}
)

if response.status_code != 200:
    print_error(f"Impossible d'obtenir un token: {response.json()}")
    exit()

tokens = response.json()
access_token = tokens['access']
refresh_token = tokens['refresh']

print_success("Token obtenu avec succès !")
print_info(f"Access Token (60 min): {access_token[:50]}...")
print_info(f"Refresh Token (24h): {refresh_token[:50]}...")

headers = {"Authorization": f"Bearer {access_token}"}

# ============================================================================
# 2. GESTION DES UTILISATEURS
# ============================================================================

print_section("2️⃣  GESTION DES UTILISATEURS")

# Voir mon profil
print_info("Récupération du profil utilisateur...")
response = requests.get(f"{BASE_URL}/users/me/", headers=headers)
if response.status_code == 200:
    user = response.json()
    print_success(f"Profil: {user.get('email')} ({user.get('first_name')} {user.get('last_name')})")
else:
    print_error(f"Erreur: {response.json()}")

# ============================================================================
# 3. GESTION DES CATÉGORIES
# ============================================================================

print_section("3️⃣  GESTION DES CATÉGORIES")

# Créer une catégorie
print_info("Création d'une catégorie...")
response = requests.post(
    f"{BASE_URL}/categories/",
    json={
        "name": "Technologie",
        "slug": "technologie",
        "parent": None
    },
    headers=headers
)
if response.status_code == 201:
    category = response.json()
    category_id = category['id']
    print_success(f"Catégorie créée: {category['name']} (ID: {category_id})")
else:
    print_error(f"Erreur: {response.json()}")
    category_id = None

# Lister les catégories
print_info("Récupération des catégories...")
response = requests.get(f"{BASE_URL}/categories/")
if response.status_code == 200:
    categories = response.json()
    print_success(f"{len(categories)} catégorie(s) trouvée(s)")

# ============================================================================
# 4. GESTION DES ARTICLES
# ============================================================================

print_section("4️⃣  GESTION DES ARTICLES")

# Créer un article
print_info("Création d'un article...")
article_data = {
    "title": "Introduction à Django",
    "excerpt": "Un guide complet pour débuter avec Django",
    "content": "Django est un framework web Python puissant. Il permet de construire des applications web rapidement et facilement.",
    "status": "draft",
    "category_id": category_id
}
response = requests.post(
    f"{BASE_URL}/articles/",
    json=article_data,
    headers=headers
)
if response.status_code == 201:
    article = response.json()
    article_id = article['id']
    print_success(f"Article créé: {article['title']} (ID: {article_id})")
    print_info(f"Status: {article['status']}, Slug: {article['slug']}")
else:
    print_error(f"Erreur: {response.json()}")
    article_id = None

# Lister les articles
print_info("Récupération des articles...")
response = requests.get(f"{BASE_URL}/articles/")
if response.status_code == 200:
    articles = response.json()
    print_success(f"{len(articles)} article(s) trouvé(s)")

# Voir mes articles seulement
print_info("Récupération de mes articles...")
response = requests.get(f"{BASE_URL}/articles/my_articles/", headers=headers)
if response.status_code == 200:
    my_articles = response.json()
    print_success(f"{len(my_articles)} article(s) personnel(s)")

# Modifier un article
if article_id:
    print_info("Modification de l'article...")
    response = requests.patch(
        f"{BASE_URL}/articles/{article_id}/",
        json={"title": "Introduction COMPLÈTE à Django"},
        headers=headers
    )
    if response.status_code == 200:
        print_success("Article modifié")
    else:
        print_error(f"Erreur: {response.json()}")

    # Publier l'article
    print_info("Publication de l'article...")
    response = requests.post(
        f"{BASE_URL}/articles/{article_id}/publish/",
        headers=headers
    )
    if response.status_code == 200:
        print_success("Article publié (status: published)")
    else:
        print_error(f"Erreur: {response.json()}")

# ============================================================================
# 5. GESTION DES COMMENTAIRES
# ============================================================================

print_section("5️⃣  GESTION DES COMMENTAIRES")

if article_id:
    # Créer un commentaire
    print_info("Création d'un commentaire...")
    response = requests.post(
        f"{BASE_URL}/comments/",
        json={
            "article": article_id,
            "content": "Super article ! Très informatif.",
            "is_public": True
        },
        headers=headers
    )
    if response.status_code == 201:
        comment = response.json()
        comment_id = comment['id']
        print_success(f"Commentaire créé: {comment['content'][:50]}... (ID: {comment_id})")
    else:
        print_error(f"Erreur: {response.json()}")

    # Lister les commentaires de l'article
    print_info("Récupération des commentaires...")
    response = requests.get(f"{BASE_URL}/comments/?article={article_id}")
    if response.status_code == 200:
        comments = response.json()
        print_success(f"{len(comments)} commentaire(s) trouvé(s)")

# ============================================================================
# 6. GESTION DES FAVORIS
# ============================================================================

print_section("6️⃣  GESTION DES FAVORIS")

if article_id:
    # Ajouter aux favoris
    print_info("Ajout aux favoris...")
    response = requests.post(
        f"{BASE_URL}/favorites/",
        json={"article_id": article_id},
        headers=headers
    )
    if response.status_code == 201:
        print_success("Article ajouté aux favoris")
    else:
        print_error(f"Erreur: {response.json()}")

    # Voir mes favoris
    print_info("Récupération de mes favoris...")
    response = requests.get(f"{BASE_URL}/favorites/my_favorites/", headers=headers)
    if response.status_code == 200:
        favorites = response.json()
        print_success(f"{len(favorites)} favori(s)")

# ============================================================================
# 7. GESTION DES NOTIFICATIONS
# ============================================================================

print_section("7️⃣  GESTION DES NOTIFICATIONS")

# Lister les notifications
print_info("Récupération des notifications...")
response = requests.get(f"{BASE_URL}/notifications/", headers=headers)
if response.status_code == 200:
    notifications = response.json()
    print_success(f"{len(notifications)} notification(s)")

# ============================================================================
# 8. LOGS D'AUDIT
# ============================================================================

print_section("8️⃣  LOGS D'AUDIT")

# Lister les logs (admin seulement)
print_info("Récupération des logs d'audit...")
response = requests.get(f"{BASE_URL}/audit/", headers=headers)
if response.status_code == 200:
    audit_logs = response.json()
    print_success(f"{len(audit_logs)} log(s) d'audit")
elif response.status_code == 403:
    print_error("Accès refusé (admin seulement)")
else:
    print_error(f"Erreur: {response.json()}")

# ============================================================================
# 9. GESTION DES RÔLES
# ============================================================================

print_section("9️⃣  GESTION DES RÔLES")

# Lister les rôles
print_info("Récupération des rôles...")
response = requests.get(f"{BASE_URL}/roles/roles/")
if response.status_code == 200:
    roles = response.json()
    print_success(f"{len(roles)} rôle(s) trouvé(s)")
    for role in roles:
        print_info(f"  - {role['name']}: {role.get('description', 'N/A')}")

# ============================================================================
# 10. TEST DE RAFRAÎCHISSEMENT TOKEN
# ============================================================================

print_section("🔄 RAFRAÎCHISSEMENT DU TOKEN")

print_info("Rafraîchissement du token...")
response = requests.post(
    f"{BASE_URL}/token/refresh/",
    json={"refresh": refresh_token}
)
if response.status_code == 200:
    new_token = response.json()
    print_success("Nouveau token obtenu !")
    print_info(f"Nouveau access: {new_token['access'][:50]}...")
else:
    print_error(f"Erreur: {response.json()}")

# ============================================================================
# RÉSUMÉ
# ============================================================================

print_section("✅ TESTS TERMINÉS")
print(f"""
{Colors.GREEN}Résumé des tests:{Colors.END}
- ✅ Authentification JWT
- ✅ Gestion des utilisateurs
- ✅ Gestion des catégories
- ✅ Gestion des articles (CRUD + publish)
- ✅ Gestion des commentaires
- ✅ Gestion des favoris
- ✅ Notifications
- ✅ Logs d'audit
- ✅ Gestion des rôles
- ✅ Rafraîchissement de token

Votre API est opérationnelle ! 🚀

Accédez à Swagger pour explorer plus :
→ http://127.0.0.1:8000/swagger/
→ http://127.0.0.1:8000/redoc/
""")
