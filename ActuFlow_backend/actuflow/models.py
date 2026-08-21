import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from .managers import UserManager


class Role(models.Model):
    id_role = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'role'
        verbose_name = 'Rôle'

    def __str__(self):
        return self.nom


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    id_utilisateur = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    # Django utilise 'password' pour mot_de_passe nativement via AbstractBaseUser
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    biographie = models.TextField(blank=True, null=True)
    photo_profil = models.ImageField(upload_to='profiles/', blank=True, null=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Permission management fields from PermissionsMixin
    is_staff = models.BooleanField(default=False)
    
    # Table de jonction pour Utilisateur_Role
    roles = models.ManyToManyField(Role, related_name='utilisateurs', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom', 'nom']

    class Meta:
        db_table = 'utilisateur'
        verbose_name = 'Utilisateur'

    @property
    def is_active(self):
        return self.est_actif

    def __str__(self):
        return self.email


class Categorie(models.Model):
    id_categorie = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=100, blank=True, null=True)
    couleur = models.CharField(max_length=20, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categorie'
        verbose_name = 'Catégorie'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class SousCategorie(models.Model):
    id_sous_categorie = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=100, blank=True, null=True)
    couleur = models.CharField(max_length=20, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    id_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='sous_categories', db_column='id_categorie')

    class Meta:
        db_table = 'sous_categorie'
        verbose_name = 'Sous-Catégorie'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Article(models.Model):
    STATUT_CHOICES = [
        ('Brouillon', 'Brouillon'),
        ('En attente', 'En attente'),
        ('Soumis', 'Soumis'),
        ('Publie', 'Publié'),
        ('Archive', 'Archivé')
    ]

    id_article = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    resume = models.TextField(blank=True, null=True)
    contenu = models.TextField()
    image_une = models.ImageField(upload_to='articles/', blank=True, null=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='Brouillon')
    nombre_vues = models.IntegerField(default=0, editable=False)
    date_publication = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='articles', db_column='id_utilisateur')
    id_categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='articles', db_column='id_categorie')

    class Meta:
        db_table = 'article'
        verbose_name = 'Article'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    id_commentaire = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commentaires', db_column='id_utilisateur')
    id_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires', db_column='id_article')

    class Meta:
        db_table = 'commentaire'
        verbose_name = 'Commentaire'

    def __str__(self):
        return f"Commentaire de {self.id_utilisateur} sur {self.id_article}"


class LikeArticle(models.Model):
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='likes', db_column='id_utilisateur')
    id_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', db_column='id_article')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'like_article'
        verbose_name = 'Like Article'
        unique_together = ('id_utilisateur', 'id_article')

    def __str__(self):
        return f"{self.id_utilisateur} likes {self.id_article}"
