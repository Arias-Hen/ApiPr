from rest_framework import serializers

from rest_framework import serializers

class PredictionInputSerializer(serializers.Serializer):
    ciudad = serializers.CharField()
    distrito = serializers.CharField()
    barrio = serializers.CharField()
    calle = serializers.CharField()
    tipo_vivienda = serializers.CharField()
    m2 = serializers.FloatField()
    num_habitaciones = serializers.IntegerField()
    num_banos = serializers.IntegerField()
    planta = serializers.CharField()
    terraza = serializers.CharField()
    balcon = serializers.CharField()
    ascensor = serializers.CharField()
    estado = serializers.IntegerField()

