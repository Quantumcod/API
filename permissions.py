from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Users


class Create(BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_superuser or request.user.is_staff or
                request.user.is_superuser):
            return True
        return request.method in ['POST']


class Update(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_superuser or request.user.is_staff or
                request.user.is_superuser):
            return True
        return request.method in ['PUT']


class Delete(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_superuser or request.user.is_staff or
                request.user.is_superuser):
            return True
        return request.method in ['DELETE']


class Get(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_superuser or request.user.is_staff or
                request.user.is_superuser):
            return True
        return request.method in ['GET']


class NotAllowed(BasePermission):
    def has_permission(self, request, view):
        return False


def permissionRoles(request, permiso, permission_class):
    if request.user.is_anonymous:
        clase_permiso = [NotAllowed]
        return clase_permiso
    response = permission_class
    create = permission_class
    get = permission_class
    update = permission_class
    delete = permission_class
    userRoles = Users.objects.get(pk=request.user.pk).Roles.all()

    if len(userRoles) > 0:
        for userRol in userRoles:
            permissionRol = userRol.RolePermissionRoles.filter(
                Permission__Url=permiso, Active=True).first()
            if permissionRol:
                if permissionRol.Create:
                    create = [Create, IsAuthenticated]
                if permissionRol.Read:
                    get = [Get, IsAuthenticated]
                if permissionRol.Update:
                    update = [Update, IsAuthenticated]
                if permissionRol.Delete:
                    delete = [Delete, IsAuthenticated]
    if request.method == 'POST':
        return create  # clase_permiso_crear
    elif request.method == 'PUT':
        return update  # clase_permiso_editar
    elif request.method == 'DELETE':
        return delete  # clase_permiso_eliminar
    else:
        return get  # clase_permiso_listar
