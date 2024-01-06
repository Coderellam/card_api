from rest_framework.serializers import ModelSerializer
from .models import Holder, Card

from datetime import datetime


class HolderSerializer(ModelSerializer):
    class Meta:
        model = Holder
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data["card"] = CardSerializer(Card.objects.filter(holder=data["id"]), many=True).data

        return data


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ('card_number', 'expire', 'created_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["timestamp"] = datetime.now()
        data["holder"] = HolderSerializer(Holder.objects.filter(id=data["holder"]).first()).data

        return data
