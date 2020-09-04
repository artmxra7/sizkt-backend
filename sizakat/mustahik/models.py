import os

from django.db import models
from django.utils import timezone

from sizakat.validators import validate_numeric_character


class Mustahik(models.Model):
    class Status(models.TextChoices):
        FAKIR = ('FAKIR', 'Fakir')
        MISKIN = ('MISKIN', 'Miskin')
        AMIL = ('AMIL', 'Amil')
        MUALAF = ('MUALAF', 'Mualaf')
        GHARIM = ('GHARIM', 'Gharim')
        FISABILILLAH = ('FISABILILLAH', 'Fisabilillah')
        MUSAFIR = ('MUSAFIR', 'Musafir')

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
    address = models.CharField(max_length=255)
    birthdate = models.DateField()
    status = models.CharField(max_length=32, choices=Status.choices)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    photo = models.ImageField(
        upload_to=os.path.join('images', 'mustahik'),
        default=os.path.join('images', 'default_photo.jpg')
    )
    data_source = models.ForeignKey('DataSource', on_delete=models.CASCADE)

    def calculate_age(self):
        return timezone.now().year - self.birthdate.year


class DataSource(models.Model):
    class Category(models.TextChoices):
        WARGA = ('WARGA', 'Warga')
        INSTITUSI = ('INSTITUSI', 'Institusi')
        PEKERJA = ('PEKERJA', 'Pekerja')

    category = models.CharField(max_length=32, choices=Category.choices)

    def get_source_detail(self):
        if self.category == DataSource.Category.INSTITUSI:
            return DataSourceInstitusi.objects.get(data_source=self)
        if self.category == DataSource.Category.PEKERJA:
            return DataSourcePekerja.objects.get(data_source=self)
        if self.category == DataSource.Category.WARGA:
            return DataSourceWarga.objects.get(data_source=self)


class DataSourceDetail(models.Model):
    class Meta:
        abstract = True

    pic_name = models.CharField(max_length=150)
    pic_ktp = models.CharField(
        max_length=32,
        validators=[validate_numeric_character]
    )
    pic_phone = models.CharField(
        max_length=32,
        validators=[validate_numeric_character]
    )
    pic_position = models.CharField(max_length=50)


class DataSourceWarga(DataSourceDetail):
    province = models.CharField(max_length=50)
    regency = models.CharField(max_length=50)
    sub_district = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    rt = models.CharField(
        max_length=3, validators=[validate_numeric_character]
    )
    rw = models.CharField(
        max_length=3, validators=[validate_numeric_character]
    )
    data_source = models.OneToOneField(
        'DataSource', on_delete=models.CASCADE,
        limit_choices_to={'category': DataSource.Category.WARGA}
    )


class DataSourceInstitusi(DataSourceDetail):
    name = models.CharField(max_length=150)
    province = models.CharField(max_length=50)
    regency = models.CharField(max_length=50)
    sub_district = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    rt = models.CharField(
        max_length=3, validators=[validate_numeric_character]
    )
    rw = models.CharField(
        max_length=3, validators=[validate_numeric_character]
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    data_source = models.OneToOneField(
        'DataSource', on_delete=models.CASCADE,
        limit_choices_to={'category': DataSource.Category.INSTITUSI}
    )
    pic_position = models.CharField(max_length=50, blank=True, null=True)


class DataSourcePekerja(DataSourceDetail):
    profession = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    data_source = models.OneToOneField(
        'DataSource', on_delete=models.CASCADE,
        limit_choices_to={'category': DataSource.Category.PEKERJA}
    )
