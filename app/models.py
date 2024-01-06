import uuid, random
import requests
from django.conf import settings
from django.db import models
from datetime import timedelta, date


"""P_TYPES bu choice, model emas!"""
P_TYPES = (
    ("HUMO", "humo"),
    ("UZCARD", "uzcard"),
    ("VISA", "visa"),
)
STATUS = (
    ("SUCCESSFULL", "successfull"),
    ("UNSUFFICIENT_BALANCE", "unsufficient_balance"),
    ("HOLDER_NOTFOUND", "holder_notfound")
)


class Holder(models.Model):
    name = models.CharField(max_length=20)
    holder_phone = models.CharField(max_length=12)
    email = models.EmailField()
    birth_date = models.DateField()

    def __str__(self):
        return str(self.name)


class Card(models.Model):
    type = models.CharField(max_length=20, choices=P_TYPES, default="uzcard")
    holder = models.ForeignKey(Holder, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expire = models.DateField(blank=True, null=True)
    balance = models.FloatField(default=0, )

    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    """def post => viewda yoziladi , modelda => def save yoziladi, logikasi deyarli bir xil, sqalashdan oldingi.... 
    class ichidagi vorisni ozgartirib oladi """

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.card_number = random.randint(8600000000133245, 8600999999999999)
        self.expire = self.generate_expire_date()
        message_str = f"Congratulations Dear {self.holder.name}, you obtained a/an {self.type} card from our bank" \
                      f"Your card number is {self.card_number}"\

        requests.get(settings.TELEGRAM_URL.format(message_str))
        return super().save(force_insert, force_update, using, update_fields)

    """ expire ni ham shu logikada shu funksiya ichida yozish (tepadagi kod,) """
    def generate_expire_date(self):
        current_date = date.today()
        expire_date = current_date + timedelta(days=3 * 365)
        requests.get(settings.TELEGRAM_URL.format(expire_date))
        return expire_date


class Transaction_history(models.Model):
    from_card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="card")
    to_card = models.ForeignKey(Card, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS)
    amount = models.FloatField(default=0)


