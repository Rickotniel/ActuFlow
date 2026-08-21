"""
Commande Django : populate_db
------------------------------
Peuple la base de données EasyX avec des données de test réalistes
(rôles, utilisateurs, catégories, sous-catégories, articles, commentaires, likes).

Installation :
    pip install Faker

Emplacement du fichier :
    <ton_app>/management/commands/populate_db.py
    (crée les dossiers management/ et management/commands/ avec un __init__.py vide dans chacun,
     si ce n'est pas déjà fait)

Utilisation :
    python manage.py populate_db
    python manage.py populate_db --users 50 --articles 200 --flush
"""

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from faker import Faker

# Adapte cet import au nom réel de ton app contenant les modèles
from actuflow.models import (
    Role,
    Utilisateur,
    Categorie,
    SousCategorie,
    Article,
    Commentaire,
    LikeArticle,
)

fake = Faker("fr_FR")

ROLES = [
    ("Administrateur", "Accès complet à la plateforme"),
    ("Redacteur", "Peut créer et soumettre des articles"),
    ("Moderateur", "Peut valider et publier les articles soumis"),
    ("Lecteur", "Peut consulter, commenter et aimer les articles"),
]

CATEGORIES = {
    "Politique": ["National", "International", "Institutions"],
    "Economie": ["Entreprises", "Marchés", "Finance"],
    "Sport": ["Football", "Basketball", "Athlétisme"],
    "Culture": ["Musique", "Cinéma", "Littérature"],
    "Technologie": ["Startups", "Intelligence Artificielle", "Télécoms"],
    "Sante": ["Prévention", "Recherche", "Système de santé"],
    "Societe": ["Education", "Environnement", "Faits divers"],
}

ARTICLE_STATUTS = ["Brouillon", "En attente", "Soumis", "Publie", "Archive"]
COULEURS = ["#e63946", "#2a9d8f", "#f4a261", "#264653", "#8338ec", "#3a86ff", "#ff006e"]


class Command(BaseCommand):
    help = "Peuple la base de données EasyX avec des données de test"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=30, help="Nombre d'utilisateurs à créer")
        parser.add_argument("--articles", type=int, default=120, help="Nombre d'articles à créer")
        parser.add_argument("--comments-max", type=int, default=8, help="Nb max de commentaires par article")
        parser.add_argument("--likes-max", type=int, default=15, help="Nb max de likes par article")
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Supprime les données existantes de ces tables avant de peupler",
        )

    def handle(self, *args, **options):
        nb_users = options["users"]
        nb_articles = options["articles"]
        comments_max = options["comments_max"]
        likes_max = options["likes_max"]

        if options["flush"]:
            self.stdout.write(self.style.WARNING("Suppression des données existantes..."))
            LikeArticle.objects.all().delete()
            Commentaire.objects.all().delete()
            Article.objects.all().delete()
            SousCategorie.objects.all().delete()
            Categorie.objects.all().delete()
            Utilisateur.objects.filter(is_superuser=False).delete()
            Role.objects.all().delete()

        with transaction.atomic():
            roles = self._create_roles()
            utilisateurs = self._create_utilisateurs(nb_users, roles)
            categories = self._create_categories()
            self._create_sous_categories(categories)
            articles = self._create_articles(nb_articles, utilisateurs, categories)
            self._create_commentaires(articles, utilisateurs, comments_max)
            self._create_likes(articles, utilisateurs, likes_max)

        self.stdout.write(self.style.SUCCESS("Base de données peuplée avec succès !"))
        self.stdout.write(f"  - {Role.objects.count()} rôles")
        self.stdout.write(f"  - {Utilisateur.objects.count()} utilisateurs")
        self.stdout.write(f"  - {Categorie.objects.count()} catégories")
        self.stdout.write(f"  - {SousCategorie.objects.count()} sous-catégories")
        self.stdout.write(f"  - {Article.objects.count()} articles")
        self.stdout.write(f"  - {Commentaire.objects.count()} commentaires")
        self.stdout.write(f"  - {LikeArticle.objects.count()} likes")

    # ------------------------------------------------------------------
    def _create_roles(self):
        self.stdout.write("Création des rôles...")
        roles = []
        for nom, description in ROLES:
            role, _ = Role.objects.get_or_create(
                nom=nom, defaults={"description": description, "est_actif": True}
            )
            roles.append(role)
        return roles

    def _create_utilisateurs(self, nb_users, roles):
        self.stdout.write(f"Création de {nb_users} utilisateurs...")
        utilisateurs = []
        for _ in range(nb_users):
            prenom = fake.first_name()
            nom = fake.last_name()
            email = fake.unique.email()

            user = Utilisateur.objects.create_user(
                email=email,
                password="Password123!",
                prenom=prenom,
                nom=nom,
            )
            user.biographie = fake.text(max_nb_chars=150)
            user.est_actif = random.random() > 0.05  # ~5% de comptes désactivés
            user.save()

            # Attribution de 1 à 2 rôles aléatoires
            user.roles.set(random.sample(roles, k=random.randint(1, 2)))
            utilisateurs.append(user)
        return utilisateurs

    def _create_categories(self):
        self.stdout.write("Création des catégories...")
        categories = {}
        for nom in CATEGORIES:
            cat, _ = Categorie.objects.get_or_create(
                nom=nom,
                defaults={
                    "slug": slugify(nom),
                    "description": fake.sentence(nb_words=12),
                    "icone": "folder",
                    "couleur": random.choice(COULEURS),
                },
            )
            categories[nom] = cat
        return categories

    def _create_sous_categories(self, categories):
        self.stdout.write("Création des sous-catégories...")
        for nom_cat, sous_noms in CATEGORIES.items():
            categorie = categories[nom_cat]
            for sous_nom in sous_noms:
                SousCategorie.objects.get_or_create(
                    nom=sous_nom,
                    id_categorie=categorie,
                    defaults={
                        "slug": slugify(f"{nom_cat}-{sous_nom}"),
                        "description": fake.sentence(nb_words=10),
                        "icone": "tag",
                        "couleur": random.choice(COULEURS),
                    },
                )

    def _create_articles(self, nb_articles, utilisateurs, categories):
        self.stdout.write(f"Création de {nb_articles} articles...")
        articles = []
        categories_list = list(categories.values())

        for _ in range(nb_articles):
            titre = fake.sentence(nb_words=8).rstrip(".")
            statut = random.choices(
                ARTICLE_STATUTS, weights=[10, 10, 15, 55, 10], k=1
            )[0]

            article = Article.objects.create(
                titre=titre,
                slug=slugify(titre) + "-" + fake.unique.lexify(text="????"),
                resume=fake.sentence(nb_words=25),
                contenu="\n\n".join(fake.paragraphs(nb=6)),
                statut=statut,
                nombre_vues=random.randint(0, 5000),
                date_publication=fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone())
                if statut == "Publie"
                else None,
                id_utilisateur=random.choice(utilisateurs),
                id_categorie=random.choice(categories_list),
            )
            articles.append(article)
        return articles

    def _create_commentaires(self, articles, utilisateurs, comments_max):
        self.stdout.write("Création des commentaires...")
        commentaires = []
        for article in articles:
            nb_comments = random.randint(0, comments_max)
            auteurs = random.sample(utilisateurs, k=min(nb_comments, len(utilisateurs)))
            for auteur in auteurs:
                commentaires.append(
                    Commentaire(
                        contenu=fake.paragraph(nb_sentences=2),
                        id_utilisateur=auteur,
                        id_article=article,
                    )
                )
        Commentaire.objects.bulk_create(commentaires)

    def _create_likes(self, articles, utilisateurs, likes_max):
        self.stdout.write("Création des likes...")
        likes = []
        for article in articles:
            nb_likes = random.randint(0, min(likes_max, len(utilisateurs)))
            fans = random.sample(utilisateurs, k=nb_likes)
            for fan in fans:
                likes.append(LikeArticle(id_utilisateur=fan, id_article=article))
        # ignore_conflicts protège le unique_together (id_utilisateur, id_article)
        LikeArticle.objects.bulk_create(likes, ignore_conflicts=True)
