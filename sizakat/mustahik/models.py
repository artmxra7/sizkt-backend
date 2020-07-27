from django.db import models
from django.utils import timezone

from sizakat.validators import validate_numeric_character


class Mustahik(models.Model):
    class Status(models.TextChoices):
        JANDA = ('JANDA', 'Janda')
        MISKIN = ('MISKIN', 'Miskin')
        YATIM = ('YATIM', 'Yatim')

    class Gender(models.TextChoices):
        LAKILAKI = ('L', 'Laki-Laki')
        PEREMPUAN = ('P', 'Perempuan')

    name = models.CharField(max_length=150)
    no_ktp = models.CharField(
        max_length=32, unique=True,
        validators=[validate_numeric_character]
    )
    phone = models.CharField(
        max_length=32, blank=True, null=True,
        validators=[validate_numeric_character]
    )
    address = models.TextField()
    province = models.CharField(max_length=32)
    regency = models.CharField(max_length=50)
    rt = models.CharField(
        max_length=4, validators=[validate_numeric_character]
    )
    rw = models.CharField(
        max_length=4, validators=[validate_numeric_character]
    )
    birthdate = models.DateField()
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.MISKIN,
    )
    family_size = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)

    def calculate_age(self):
        return timezone.now().year - self.birthdate.year
