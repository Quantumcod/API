from django.db import models
from django.contrib.auth.models import User


class Permissions(models.Model):
    """
    Description: This class represents the Permissions for users
    Author: Suling Vera
    Creation date : 2021
    Modification date: 21/07/2021
    """
    Name = models.CharField(
        blank=True,
        max_length=40
    )
    Description = models.CharField(
        blank=True,
        max_length=50
    )
    Icon = models.CharField(
        blank=True,
        max_length=50
    )
    Url = models.CharField(
        blank=True,
        max_length=70
    )
    Created = models.DateTimeField(
        auto_now_add=True
    )
    Active = models.BooleanField(
        default=True
    )
    Deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return 'Permission [ {} ] - {}'.format(
            self.pk,
            self.Name
        )

    class Meta:
        ordering = ['pk']
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        db_table = 'Permissions'


class Roles(models.Model):
    """
    Description: This class represents the Roles for users
    Author: Suling Vera
    Creation date : 2021
    Modification date: 21/07/2021
    """
    Name = models.CharField(
        blank=True,
        max_length=40
    )
    Description = models.CharField(
        blank=True,
        max_length=50
    )
    Permissions = models.ManyToManyField(
        Permissions,
        through='PermissionsRoles',
        through_fields=('Role', 'Permission'),
        related_name='PermissionsRoles'
    )
    Created = models.DateTimeField(
        auto_now_add=True
    )
    Active = models.BooleanField(
        default=True
    )
    Deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '{} - {}'.format(
            self.pk,
            self.Name
        )

    class Meta:
        ordering = ['Name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        db_table = 'Roles'


class PermissionsRoles(models.Model):
    """
    Description: This class represents the intermediate relationship between 
    Permissions and Role for users
    Author: Suling Vera
    Creation date : 2021
    Modification date: 21/07/2021
    """
    Permission = models.ForeignKey(
        Permissions,
        on_delete=models.CASCADE,
        related_name='PermissionPermissionRoles'
    )
    Role = models.ForeignKey(
        Roles,
        on_delete=models.CASCADE,
        related_name='RolePermissionRoles'
    )
    Read = models.BooleanField(
        default=False
    )
    Update = models.BooleanField(
        default=False
    )
    Delete = models.BooleanField(
        default=False
    )
    Create = models.BooleanField(
        default=False
    )
    Created = models.DateTimeField(
        auto_now_add=True
    )
    Active = models.BooleanField(
        default=True
    )
    Deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return 'Id[ {} ] - {} -  {}'.format(
            self.pk,
            self.Permission.Url,
            self.Role.Name
        )

    class Meta:
        ordering = ['pk']
        verbose_name = 'Permission Role'
        verbose_name_plural = 'Permissions Roles'
        db_table = 'PermissionsRoles'


class Users(User):
    """
    Description: This class implements Users class from Django through 
    inheritance
    Author: Suling Vera
    Creation date : 2021
    Modification date: 21/07/2021
    """
    Created = models.DateTimeField(
        auto_now_add=True
    )
    Roles = models.ManyToManyField(
        Roles,
    )

    def __str__(self):
        return '{} - {}'.format(
            self.pk,
            self.username
        )

    class Meta:
        ordering = ['pk']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'User'