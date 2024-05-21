from rest_framework import serializers

from apps.image_tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    def create(self, validated_data: dict):
        ticket = Ticket.objects.create(**validated_data)
        ticket.save()
        return ticket

    def validate_max_image_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "max_image_quantity must be greater than 0"
            )
        return value


class ImageUploadSerializer(serializers.Serializer):
    image_url = serializers.RegexField(
        regex="^https://.+",
    )
