from rest_framework import serializers
from .models import CV,SendMail

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'file']



class SendMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMail
        fields = ['full_name', 'email', 'subject', 'message']
