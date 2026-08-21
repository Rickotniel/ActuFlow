from django.contrib import admin
from .models import Role, Utilisateur, Categorie, SousCategorie, Article, Commentaire, LikeArticle

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'est_actif', 'date_creation')
    list_filter = ('est_actif',)
    search_fields = ('nom',)

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('email', 'prenom', 'nom', 'est_actif', 'is_staff', 'date_creation')
    list_filter = ('est_actif', 'is_staff', 'roles')
    search_fields = ('email', 'prenom', 'nom')
    filter_horizontal = ('roles',)

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'date_creation')
    search_fields = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(SousCategorie)
class SousCategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'id_categorie', 'date_creation')
    list_filter = ('id_categorie',)
    search_fields = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'id_utilisateur', 'id_categorie', 'statut', 'nombre_vues', 'date_creation')
    list_filter = ('statut', 'id_categorie', 'date_creation')
    search_fields = ('titre', 'resume', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('id_commentaire', 'id_utilisateur', 'id_article', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('contenu',)

@admin.register(LikeArticle)
class LikeArticleAdmin(admin.ModelAdmin):
    list_display = ('id_utilisateur', 'id_article', 'date_creation')
    list_filter = ('date_creation',)
