from django.core.validators import RegexValidator

validate_numeric_character = RegexValidator(
    r'^[0-9]*$', 'Numeric character only.'
)


def validate_photo(photo):
    valid_extensions = ['jpg', 'png']
    photo_extension = photo.name.split('.')[-1]
    return photo_extension in valid_extensions
