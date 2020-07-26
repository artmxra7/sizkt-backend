from django.db import models

from django.core.validators import RegexValidator

numeric_only = RegexValidator(r'^[0-9]*$', 'Numeric only.')


class Mustahik(models.Model):
    class Status(models.TextChoices):
        JANDA = ('JANDA', 'Janda')
        MISKIN = ('MISKIN', 'Miskin')
        YATIM = ('YATIM', 'Yatim')

    name = models.CharField(max_length=150)
    no_ktp = models.CharField(
        max_length=32, unique=True,
        validators=[numeric_only]
    )
    phone = models.CharField(
        max_length=32, blank=True, null=True,
        validators=[numeric_only]
    )
    address = models.TextField()
    province = models.CharField(max_length=32)
    regency = models.CharField(max_length=50)
    rt = models.CharField(max_length=4, validators=[numeric_only])
    rw = models.CharField(max_length=4, validators=[numeric_only])
    birthdate = models.DateField()
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.MISKIN,
    )
    family_size = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
