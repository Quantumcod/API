from django.contrib import admin

# Register your models here.
from .models import Cryptocurrencies, Fees,Commission

admin.site.register(Cryptocurrencies)
admin.site.register(Fees)
admin.site.register(Commission)