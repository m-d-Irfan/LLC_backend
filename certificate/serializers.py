from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    class Meta:
        model = Certificate
        fields = ["id", "certificate_id", "course", "issued_at" ]
    
        read_only_fields = ["id", "certificate_id", "course", "issued_at" ]

