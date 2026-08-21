from rest_framework import serializers
from django.utils import timezone
from .models import Role, Utilisateur, Categorie, SousCategorie, Article, Commentaire, LikeArticle

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id_utilisateur', 'email', 'prenom', 'nom', 'biographie', 'photo_profil', 'est_actif', 'date_creation', 'date_modification', 'roles']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        password = validated_data.pop('password', None)
        user = Utilisateur.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        user.roles.set(roles)
        return user

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id_utilisateur', 'nombre_vues', 'date_publication']

    def validate_statut(self, value):
        request = self.context.get('request')
        if not request or not request.user:
            return value

        user = request.user
        # Seuls les admins ou modérateurs peuvent publier ou archiver
        is_staff_or_moderator = user.is_staff or user.roles.filter(nom__in=['Administrateur', 'Moderateur']).exists()
        
        if value in ['Publie', 'Archive'] and not is_staff_or_moderator:
            raise serializers.ValidationError(
                "Vous n'avez pas la permission de publier ou d'archiver directement un article. "
                "Vous pouvez uniquement l'enregistrer comme 'Brouillon' ou le mettre 'En attente'."
            )
        return value

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = '__all__'
        read_only_fields = ['id_utilisateur']

class LikeArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeArticle
        fields = '__all__'
        read_only_fields = ['id_utilisateur']
