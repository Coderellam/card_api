from django.contrib import admin
from .models import Card, Holder, Transaction_history

admin.site.register(Card)
admin.site.register(Holder)
admin.site.register(Transaction_history)

