from django.db import models

# Create your models here.


class Mustahik(models.Model):

    class Status(models.TextChoices):
        JANDA = ('JANDA', 'Janda')
        MISKIN = ('MISKIN', 'Miskin')
        YATIM = ('YATIM', 'Yatim')

    name = models.CharField(max_length=32)
    no_ktp = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=32, blank=True)
    address = models.TextField()
    province = models.CharField(max_length=32)
    regency = models.CharField(max_length=32)
    rt = models.CharField(max_length=4)
    rw = models.CharField(max_length=4)
    birthdate = models.DateField()
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.MISKIN,
    )
    family_size = models.PositiveSmallIntegerField()
    description = models.TextField()
