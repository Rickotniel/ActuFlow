from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Role, Utilisateur, Categorie, SousCategorie, Article, Commentaire, LikeArticle
from .serializers import (
    RoleSerializer, UtilisateurSerializer, CategorieSerializer,
    SousCategorieSerializer, ArticleSerializer, CommentaireSerializer,
    LikeArticleSerializer
)
from core.permissions import (
    IsAdmin, IsJournalist, IsOwnerOrReadOnly, IsAdminOrReadOnly, 
    IsArticleAuthorOrAdmin, IsOwnerOrAdmin
)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAdmin]

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAdminOrReadOnly]

class SousCategorieViewSet(viewsets.ModelViewSet):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer
    permission_classes = [IsAdminOrReadOnly]

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsArticleAuthorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        
        # Visiteur anonyme : voit uniquement les articles publiés
        if not user or user.is_anonymous:
            return Article.objects.filter(statut='Publie')
            
        # Admin ou modérateur : voit absolument tout (y compris en attente et brouillons de tout le monde)
        if user.is_staff or user.roles.filter(nom__in=['Administrateur', 'Moderateur']).exists():
            return Article.objects.all()
            
        # Utilisateur classique / Rédacteur : voit les articles publiés + ses propres brouillons/soumissions
        return Article.objects.filter(
            Q(statut='Publie') | Q(id_utilisateur=user)
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Incrémente le nombre de vues lors de la consultation d'un article
        instance.nombre_vues += 1
        instance.save(update_fields=['nombre_vues'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Associe automatiquement l'auteur de l'article à l'utilisateur connecté
        # Si le statut est défini comme 'Publie' (par un admin/modérateur autorisé via la validation du serializer)
        statut = serializer.validated_data.get('statut', 'Brouillon')
        date_publication = timezone.now() if statut == 'Publie' else None
        
        serializer.save(
            id_utilisateur=self.request.user,
            date_publication=date_publication
        )

    def perform_update(self, serializer):
        statut = serializer.validated_data.get('statut')
        # Si le statut passe à 'Publie', on enregistre la date de publication
        if statut == 'Publie' and serializer.instance.statut != 'Publie':
            serializer.save(date_publication=timezone.now())
        else:
            serializer.save()

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)

class LikeArticleViewSet(viewsets.ModelViewSet):
    queryset = LikeArticle.objects.all()
    serializer_class = LikeArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)
