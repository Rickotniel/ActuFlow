from rest_framework import serializers
from django.utils import timezone
from .models import Role, Utilisateur, Categorie, SousCategorie, Article, Commentaire, LikeArticle

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UtilisateurSerializer(serializers.ModelSerializer):
    role_names = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='nom',
        source='roles'
    )

    class Meta:
        model = Utilisateur
        fields = [
            'id_utilisateur', 'email', 'password', 'prenom', 'nom',
            'biographie', 'photo_profil', 'est_actif', 'is_staff',
            'date_creation', 'date_modification', 'roles', 'role_names'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'roles': {'required': False}
        }

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        password = validated_data.pop('password', None)
        user = Utilisateur.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        if roles:
            user.roles.set(roles)
        else:
            lecteur_role = Role.objects.filter(nom='Lecteur').first()
            if lecteur_role:
                user.roles.add(lecteur_role)
        return user

class ProfilSerializer(serializers.ModelSerializer):
    """Champs modifiables par l'utilisateur sur son propre profil."""
    role_names = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='nom', source='roles'
    )

    class Meta:
        model = Utilisateur
        fields = [
            'id_utilisateur', 'email', 'prenom', 'nom', 'biographie',
            'photo_profil', 'est_actif', 'is_staff', 'date_creation',
            'date_modification', 'role_names'
        ]
        read_only_fields = [
            'id_utilisateur', 'email', 'est_actif', 'is_staff',
            'date_creation', 'date_modification', 'role_names'
        ]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        roles = validated_data.pop('roles', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        if roles is not None:
            instance.roles.set(roles)
        instance.save()
        return instance

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
