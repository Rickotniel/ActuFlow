from django.db.models import Q
from django.utils import timezone
from rest_framework import filters, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Role, Utilisateur, Categorie, SousCategorie, Article, Commentaire, LikeArticle
from .serializers import (
    RoleSerializer, UtilisateurSerializer, CategorieSerializer,
    SousCategorieSerializer, ArticleSerializer, CommentaireSerializer,
    LikeArticleSerializer, ProfilSerializer
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

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'me':
            return [permissions.IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        self.serializer_class = ProfilSerializer
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id_categorie', 'statut', 'id_utilisateur']
    search_fields = ['titre', 'resume', 'contenu']

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='mine')
    def mine(self, request):
        queryset = self.filter_queryset(
            Article.objects.filter(id_utilisateur=request.user).order_by('-date_modification')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(queryset, many=True).data)

    def get_queryset(self):
        user = self.request.user
        
        # Visiteur anonyme : voit uniquement les articles publiés
        if not user or user.is_anonymous:
            return Article.objects.filter(statut='Publie').order_by('-date_publication', '-date_creation')
            
        # Admin ou modérateur : voit absolument tout (y compris en attente et brouillons de tout le monde)
        if user.is_staff or user.roles.filter(nom__in=['Administrateur', 'Moderateur']).exists():
            return Article.objects.all().order_by('-date_publication', '-date_creation')
            
        # Utilisateur classique / Rédacteur : voit les articles publiés + ses propres brouillons/soumissions
        return Article.objects.filter(
            Q(statut='Publie') | Q(id_utilisateur=user)
        ).order_by('-date_publication', '-date_creation')

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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id_article']
    ordering = '-date_creation'

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)

class LikeArticleViewSet(viewsets.ModelViewSet):
    queryset = LikeArticle.objects.all()
    serializer_class = LikeArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id_article', 'id_utilisateur']
    ordering = '-date_creation'

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)
