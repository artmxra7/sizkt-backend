from django import forms

from .models import Muzakki, Transaction, ZakatTransaction


class MuzakkiForm(forms.ModelForm):
    class Meta:
        model = Muzakki
        fields = [
            'no_ktp',
            'name',
            'phone',
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'payment_type',
            'goods_delivery_type',
            'pick_up_address',
            'transfer_receipt',
            'payment_confirmation',
            'goods_confirmation',
        ]


class ZakatTransactionForm(forms.ModelForm):
    class Meta:
        model = ZakatTransaction
        fields = [
            'value',
            'zakat_type',
            'muzakki',
            'transaction',
        ]
