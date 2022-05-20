from django.db import models
from ..cryptocurrencies.models import Cryptocurrencies
from django.db.models.signals import post_save
from django.dispatch import receiver


class CompanyWallets(models.Model):
    """
    Description: This class represents the Company Wallets
    Author: Suling Vera
    Date Created:  09/08/2021
    Date of last modification: 29/03/2022
    """
    Address = models.CharField(
        max_length=150,
    )
    Cryptocurrency = models.ForeignKey(
        Cryptocurrencies,
        on_delete=models.CASCADE,
        related_name='CompanyWalletsCryptocurrencies',
    )
    Quantity = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0.0,
        help_text='Value in btc,satoshis'
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
            self.Cryptocurrency,
            self.Address
        )

    class Meta:
        ordering = ['pk']
        verbose_name = 'CompanyWallet'
        verbose_name_plural = 'CompanyWallets'
        db_table = 'CompanyWallets'


@receiver(post_save, sender=CompanyWallets)
def saveCompanyWallets(sender, instance, created, **kwargs):
    """
    signals to activate only one company wallet and deactivate all others 
    of cryptocurrency
    """
    if created:
        listCompanyWallet = instance.Cryptocurrency\
            .CompanyWalletsCryptocurrencies.filter(Active=True)
        for idx in range(0, len(listCompanyWallet)-1):
            listCompanyWallet[idx].Active = False
            listCompanyWallet[idx].save()
