import graphene

from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.types import ErrorType
from sizakat.validators import validate_photo

from .forms import MuzakkiForm, TransactionForm, ZakatTransactionForm
from .types import MuzakkiType, TransactionType, ZakatTransactionType


class MuzakkiMutation(DjangoModelFormMutation):
    muzakki = graphene.Field(MuzakkiType)

    class Meta:
        form_class = MuzakkiForm


class TransactionMutation(DjangoModelFormMutation):
    transaction = graphene.Field(TransactionType)

    class Meta:
        form_class = TransactionForm

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        form = cls.get_form(root, info, **input)
        transfer_receipt = info.context.FILES.get('transfer_receipt', None)
        if transfer_receipt and not validate_photo(transfer_receipt):
            form.add_error('transfer_receipt', 'invalid format')

        if form.is_valid():
            transaction = form.save(commit=False)
            if transfer_receipt:
                transaction.transfer_receipt = transfer_receipt
            transaction.save()
            kwargs = {cls._meta.return_field_name: transaction}
            return cls(errors=[], **kwargs)
        else:
            errors = ErrorType.from_errors(form.errors)
            return cls(errors=errors)


class ZakatTransactionMutation(DjangoModelFormMutation):
    zakat_trasaction = graphene.Field(ZakatTransactionType)

    class Meta:
        form_class = ZakatTransactionForm
