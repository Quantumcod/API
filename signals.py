from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CompanyWallets
from ..updates.models import Updates


def executeUpdate(tableName, registerID, action):
    """
    function to register in the update table 
    in case the companywallet table is created 
    """
    a, c = Updates.objects.update_or_create(
        TableName=tableName,
        RegisterID=registerID,
        defaults={
            'Action': action,
            'Updated': timezone.now()
        })


@receiver(post_save, sender=CompanyWallets)
def saveCompanyWallets(sender, instance, created, **kwargs):
    """
    function of signals to register companywallet creations or upgrades
    """
    if created:
        executeUpdate('CompanyWallets', instance.pk, 'Created')
    else:
        executeUpdate('CompanyWallets', instance.pk, 'Updated')
