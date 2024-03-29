from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидация: username != me."""

    if value.lower() == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
