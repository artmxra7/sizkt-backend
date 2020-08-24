import os

from django.db import models

from sizakat.validators import validate_numeric_character


class Muzakki(models.Model):
    no_ktp = models.CharField(
        max_length=32, unique=True,
        validators=[validate_numeric_character]
    )
    name = models.CharField(max_length=150)
    phone = models.CharField(
        max_length=32, blank=True, null=True,
        validators=[validate_numeric_character]
    )


class ZakatType(models.Model):
    class ItemType(models.TextChoices):
        MONEY = ('MONEY', 'Uang')
        RICE = ('RICE', 'Beras')
        GOLD = ('GOLD', 'Emas')
        CHECK = ('CHECK', 'Cek')

    name = models.CharField(max_length=50)
    item_type = models.CharField(max_length=32, choices=ItemType.choices)

    def __str__(self):
        return '%s - %s' % (self.name, self.ItemType[self.item_type].label)


class Transaction(models.Model):
    class PaymentType(models.TextChoices):
        CASH = ('CASH', 'Tunai')
        TRANSFER = ('TRANSFER', 'Transfer')

    class GoodsDeliveryType(models.TextChoices):
        PICKUP = ('PICKUP', 'Dijemput')
        DELIVER = ('DELIVER', 'Diantar')

    payment_type = models.CharField(
        max_length=32, choices=PaymentType.choices, blank=True, null=True
    )
    goods_delivery_type = models.CharField(
        max_length=32, choices=GoodsDeliveryType.choices, blank=True, null=True
    )
    pick_up_address = models.TextField(blank=True, null=True)
    transfer_receipt = models.FileField(
        upload_to=os.path.join('images', 'transaction'), blank=True, null=True
    )
    payment_confirmation = models.BooleanField(default=False)
    goods_confirmation = models.BooleanField(default=False)
    # TODO: foreign key to user


class ZakatTransaction(models.Model):
    value = models.DecimalField(max_digits=15, decimal_places=2)
    zakat_type = models.ForeignKey(ZakatType, on_delete=models.CASCADE)
    muzakki = models.ForeignKey(Muzakki, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
