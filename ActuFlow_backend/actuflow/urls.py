from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, UtilisateurViewSet, CategorieViewSet,
    SousCategorieViewSet, ArticleViewSet, CommentaireViewSet,
    LikeArticleViewSet
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'sous-categories', SousCategorieViewSet, basename='souscategorie')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'commentaires', CommentaireViewSet, basename='commentaire')
router.register(r'likes', LikeArticleViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
]
