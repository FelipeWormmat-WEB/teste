from rest_framework import serializers
from cambio.models import Currency, Cambio

class CambiosSerializer(serializers.ModelSerializer):
    target_currency = serializers.StringRelatedField()

    class Meta:
        model = Cambio
        fields = ["id", "target_currency", "date", "price"]

class CambiosFilterSerializer(serializers.Serializer):
    symbol = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        try:
            if "start_date" in data and "end_date" in data and data["end_date"] < data["start_date"]:
                raise serializers.ValidationError("A data final deve ser maior ou igual a data inicial.")

            symbol = data.get("symbol")
            if symbol and not Currency.objects.filter(symbol=symbol).exists():
                print(f"Símbolo de moeda inválido: {symbol}")
                print(f"Currency objects: {Currency.objects.all()}")
                raise serializers.ValidationError(f"Símbolo de moeda inválido: {symbol}")
        except serializers.ValidationError as e:
            print(f"Validation Error: {e.detail}")
            raise  # Re-raise the exception after printing

        return data
