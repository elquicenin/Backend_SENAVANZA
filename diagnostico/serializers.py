from Users.models import programa_formacion
from rest_framework import serializers

class ProgramaFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = programa_formacion
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        if not data.get('nombre'):
            raise serializers.ValidationError("El nombre del programa de formación es obligatorio.")
        return data
    
    def create(self, validated_data):
        return programa_formacion.objects.create(**validated_data)

