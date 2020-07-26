from django.core.validators import RegexValidator

validate_numeric_character = RegexValidator(
    r'^[0-9]*$', 'Numeric character only.'
)
