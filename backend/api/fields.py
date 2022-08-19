import webcolors
from rest_framework import serializers


class Hex2NameColor(serializers.Field):
    """Сериализатор работы с HEX-кодом"""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError(
                'Для этого цвета нет имени. Доступные: К.О.Ж.З.С.Ф.')
        return data
