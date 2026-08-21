from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    """
    Autorise seulement les administrateurs (is_staff=True ou rôle Administrateur)
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.is_staff or request.user.roles.filter(nom='Administrateur').exists()


class IsJournalist(BasePermission):
    """
    Autorise seulement les rédacteurs/journalistes (rôle Redacteur) ou Administrateurs
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.roles.filter(nom__in=['Redacteur', 'Administrateur']).exists()


class IsModerator(BasePermission):
    """
    Autorise seulement les modérateurs ou Administrateurs
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.roles.filter(nom__in=['Moderateur', 'Administrateur']).exists()


class IsOwnerOrReadOnly(BasePermission):
    """
    Autorise tous les utilisateurs à lire (GET, HEAD, OPTIONS)
    Autorise seulement le propriétaire (id_utilisateur) à modifier/supprimer
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(obj, 'id_utilisateur', None) == request.user
        )


class IsAuthenticated(BasePermission):
    """
    Autorise seulement les utilisateurs authentifiés
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwner(BasePermission):
    """
    Autorise seulement le propriétaire de l'objet (id_utilisateur)
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(obj, 'id_utilisateur', None) == request.user
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Autorise le propriétaire de l'objet (id_utilisateur) ou les admins
    """
    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False
            
        if request.user.is_staff or request.user.roles.filter(nom='Administrateur').exists():
            return True
        
        return getattr(obj, 'id_utilisateur', None) == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Autorise la lecture pour tous
    Autorise la modification/suppression seulement pour les admins
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.is_staff or request.user.roles.filter(nom='Administrateur').exists()


class IsArticleAuthorOrAdmin(BasePermission):
    """
    Permission spéciale pour les articles
    Lecture : publique pour articles publiés, auteur/admin/modérateur pour le reste
    Écriture : auteur ou admin/modérateur
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if getattr(obj, 'statut', None) == 'Publie':
                return True
            if not (request.user and request.user.is_authenticated):
                return False
            if request.user.is_staff or request.user.roles.filter(nom__in=['Administrateur', 'Moderateur']).exists():
                return True
            return getattr(obj, 'id_utilisateur', None) == request.user
        
        if not (request.user and request.user.is_authenticated):
            return False
            
        if request.user.is_staff or request.user.roles.filter(nom__in=['Administrateur', 'Moderateur']).exists():
            return True
        return getattr(obj, 'id_utilisateur', None) == request.user


class IsSuperUser(BasePermission):
    """
    Autorise seulement les super utilisateurs
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
