from rest_framework import serializers

from apps.image_tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data: dict):
        ticket = Ticket.objects.create(**validated_data)
        ticket.save()
