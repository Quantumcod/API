from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Cryptocurrencies, Fees
from ..updates.models import Updates


def executeUpdate(tableName, registerID, action):
    a, c = Updates.objects.update_or_create(
        TableName=tableName,
        RegisterID=registerID,
        defaults={
            'Action': action,
            'Updated': timezone.now()
        })


@receiver(post_save, sender=Cryptocurrencies)
def saveCryptocurrencies(sender, instance, created, **kwargs):

    if created:
        executeUpdate('Cryptocurrencies', instance.pk, 'Created')
    else:
        executeUpdate('Cryptocurrencies', instance.pk, 'Updated')


@receiver(post_save, sender=Fees)
def saveFees(sender, instance, created, **kwargs):
    if instance.Active == True and instance.Type == 'SEND':
        Fees.objects.filter(Type='SEND').exclude(pk=instance.pk) \
            .update(Active=False)
    else:
        Fees.objects.filter(Type='EXCHANGE').exclude(pk=instance.pk) \
            .update(Active=False)
    if created:
        executeUpdate('Fees', instance.pk, 'Created')
    else:
        executeUpdate('Fees', instance.pk, 'Updated')
