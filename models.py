#from _typeshed import Self
from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

def validatordiffTotalFeeSecurity(Security,TotalFee):
    if TotalFee - Security<=0:
        raise ValidationError(
                {'Security': "TotalFee should grant that Security"})

class Cryptocurrencies(models.Model):
    """
    Author: Suling Vera
    Modification date: 09/08/2021
    Description: 
    This class represents a Cryptocurrency
    01 - Modification 01
    """
    PRIORITY = (
        ('HIGH','HIGH'),
        ('MEDIUM','MEDIUM'),
        ('LOW','LOW'),
    )
    Symbol = models.CharField(
        blank = True,
        max_length = 100,
    )
    Name = models.CharField(
        blank = True,
        max_length = 30,
    )
    Logo = models.ImageField(
		upload_to='logos',
		null=True,
        blank = True
		)
    Priority = models.CharField(
        max_length = 6,
        choices = PRIORITY,
        default = '',
        help_text='Cryptocurrency priority'
    )
    MinerFeeAverage = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0,
        help_text='Value in dolars, Autocalculated automatically'
    )
    MinerFee = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0,
        help_text='Value in dolars,8 decimals'
    )
    Min = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0,
        help_text='Value min ltc,btc ..,8 decimals'
    )
    TotalFee = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0,
        help_text='Value in dolars,8 decimals'
    )
    Security = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0,
        help_text='Value in dolars,8 decimals',
        #validators =[validatordiffTotalFeeSecurity(self.TotalFee)]
    )
    ModifiableMinerfee= models.BooleanField(
        default = True
    )
    GasLimit = models.DecimalField(
        null=True,
        max_digits = 20,
        decimal_places = 8,
        blank=True,
        help_text='Value in 8 decimals'
    )
    Price = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0,
        help_text='Value in dolars, 8 decimals'
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
            self.Name
            )

    def TotalFeeToBTC(self):
        response=((self.TotalFee/self.Price))
        return f"{(response):.8f}"
    def MinerFeeToBTC(self):
        response=(self.MinerFee / self.Price)
        return f"{(response):.8f}"
    def MinerFeeToSatoshi(self):
        response=int(Decimal(self.MinerFeeToBTC()) * 100000000)
        return response
    def SecurityToBTC(self):
        if self.Price>0:
            response = (self.Security / self.Price)
            return f"{(response):.8f}"
        else:
            return f"{(0.00000001):.8f}"
    class Meta:
        ordering = ['pk']
        verbose_name = 'Cryptocurrency'
        verbose_name_plural = 'Cryptocurrencies'
        unique_together = ('Symbol',)
        db_table = 'Cryptocurrencies'

class Commission(models.Model):

    Cryptocurrency = models.ForeignKey(
        Cryptocurrencies,
        on_delete = models.CASCADE,
        related_name = 'ComissionByCryptocurrency',
    )
    Min = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0,
        help_text='Value in dolars, 8 decimals'
    )
    Max = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 100.0,
        help_text='Value in dolars, 8 decimals'
    )
    Percentage = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        default = 1.0,
    )
    Fixed = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 1.0,
        help_text='Value in dolars, 8 decimals'
    )
    Created = models.DateTimeField(
        auto_now_add=True
    )
    Update = models.DateTimeField(
        auto_now=True
    )
    Variable = models.BooleanField(
        default = True
    )
    Active = models.BooleanField(
        default = True
        )
    Deleted = models.BooleanField(
        default = False
        )
    def __str__(self):
        return '{} - {}% -{} '.format(
            self.Cryptocurrency,
            self.Percentage,
            self.Fixed
            )
    class Meta:
        ordering = ['pk']
        verbose_name = 'Comission'
        verbose_name_plural = 'Comissiones'
        db_table = 'Comissiones'


class Fees(models.Model):
    """
    Author: Suling Vera
    Modification date: 09/08/2021
    Description: 
    This class represents the Company Profit as Fees:
    01 - Modification 01
    """
    TYPES = (
        ('EXCHANGE','EXCHANGE'),
        ('SEND','SEND'),
    ) 
    #TYPES_AMOUNT = (
    #    ('VARIABLE','VARIABLE'),
    #    ('STATIC','STATIC'),
    #)
    Type = models.CharField(
        max_length = 15,
        choices = TYPES,
        default = ''
    )
    #Cryptocurrency = models.ForeignKey(
    #    Cryptocurrencies,
    #    on_delete = models.CASCADE,
    #    related_name = 'FeesCryptocurrency',
    #)
    #TypeAmount = models.CharField(
    #    max_length = 10,
    #    choices = TYPES_AMOUNT,
    #    default = 'STATIC'
    #)
    AverageMinerFee = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0
    )
    Security = models.DecimalField(
        max_digits = 20,
        decimal_places = 8,
        default = 0.0
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
        return '{} - {}'.format(
            self.Type,
            self.AverageMinerFee
            )
    class Meta:
        ordering = ['pk']
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'
        db_table = 'Fees'

class ExchangeRate(models.Model):
    """
    Author: Yessica Chuctaya 
    Modification date: 01/10/2021
    Description: 
    This class represents the exchange rate from dollar to soles 
    01 - Modification 01
    """
    Divisa = models.CharField(
        max_length = 10,
        default = 'USD'
    )
    Created = models.DateTimeField(
        auto_now_add = True
        )
    RatePurchase = models.DecimalField(
        max_digits = 20,
        decimal_places = 4,
        default = 0.0
    )
    RateSale = models.DecimalField(
        max_digits = 20,
        decimal_places = 4,
        default = 0.0
    )
    Created = models.DateTimeField(
        auto_now_add=True
    )
    Update = models.DateTimeField(
        auto_now=True
    )
    Active = models.BooleanField(
        default = True
        )
    Deleted = models.BooleanField(
        default = False
        )
    def __str__(self):
        return '{} - {}'.format(
            self.Type,
            self.AverageMinerFee
            )
    class Meta:
        ordering = ['pk']
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'
        db_table = 'Rates'

