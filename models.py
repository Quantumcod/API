from django.db import models


class Clients(models.Model):
    """
    Description: This class represents a Client:
    Author: Suling Vera
    Date Created:   09/08/2021
    Date of last modification: 28/03/2022
    """
    uuid = models.CharField(
        blank = True,
        max_length = 100,
        unique = True
    )
    Created = models.DateTimeField(
        auto_now_add = True
        )
    Active = models.BooleanField(
        default = True
        )
    Deleted = models.BooleanField(
        default = False
        )
    def __str__(self):
        return '{}'.format(
            self.uuid
            )
    class Meta:
        ordering = ['pk']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        unique_together = ['id', 'uuid']
        db_table = 'Clients'

class Addresses(models.Model):
    """
    Description: This class models the relationship of a Client
                through its address
    Author: Yessica Chuctaya
    Date Created:   nn/10/2021
    Date of last modification: 28/03/2022
    """
    uuid = models.ForeignKey(
        Clients,
        null=True,
        on_delete = models.CASCADE,
        related_name = 'CompanyWalletsCryptocurrencies',
    )
    Address = models.CharField(
        max_length = 150,
    )
    Created = models.DateTimeField(
        auto_now_add = True
        )
    Updated = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return '{}'.format(
            self.uuid
            )
    class Meta:
        ordering = ['pk']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        db_table = 'Address'
