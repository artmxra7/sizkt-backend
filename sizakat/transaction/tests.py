from django.test import TestCase

from .models import Muzakki, Transaction, ZakatType, ZakatTransaction


class TransactionModelTestCase(TestCase):
    def setUp(self):
        muzakki = Muzakki.objects.create(
            no_ktp='1234567890',
            name='tester',
            phone='081234567890'
        )
        zakat_type = ZakatType.objects.create(
            name='Zakat Fitrah',
            item_type=ZakatType.ItemType.MONEY
        )
        transaction = Transaction.objects.create(
            payment_type=Transaction.PaymentType.CASH,
        )
        ZakatTransaction.objects.create(
            value=50000,
            zakat_type=zakat_type,
            muzakki=muzakki,
            transaction=transaction
        )

    def test_muzakki_creation(self):
        muzakki = Muzakki.objects.get(no_ktp='1234567890')
        self.assertTrue(isinstance(muzakki, Muzakki))

    def test_zakat_type_creation(self):
        zakat_type = ZakatType.objects.get(name='Zakat Fitrah')
        self.assertTrue(isinstance(zakat_type, ZakatType))

    def test_transaction_creation(self):
        transactions = Transaction.objects.all()
        transaction = Transaction.objects.get(pk=transactions[0].pk)
        self.assertTrue(isinstance(transaction, Transaction))

    def test_zakat_transaction_creation(self):
        zakat_transactions = ZakatTransaction.objects.all()
        zakat_transaction = ZakatTransaction.objects.get(
            pk=zakat_transactions[0].pk
        )
        self.assertTrue(isinstance(zakat_transaction, ZakatTransaction))
