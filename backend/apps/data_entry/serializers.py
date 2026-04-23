from rest_framework import serializers

from apps.data_entry.models import EntryMonthlyData, EntryMonthlyItem


class EntryMonthlyItemSerializer(serializers.ModelSerializer):
    """Serialize monthly data detail items."""

    class Meta:
        model = EntryMonthlyItem
        fields = "__all__"


class EntryMonthlyDataSerializer(serializers.ModelSerializer):
    """Serialize monthly data headers and nested items."""
    items = EntryMonthlyItemSerializer(many=True)

    class Meta:
        model = EntryMonthlyData
        fields = "__all__"

    def create(self, validated_data):
        """Create monthly header and all nested detail items."""
        items = validated_data.pop("items", [])
        instance = EntryMonthlyData.objects.create(**validated_data)
        EntryMonthlyItem.objects.bulk_create([EntryMonthlyItem(entry=instance, **item) for item in items])
        return instance

    def update(self, instance, validated_data):
        """Update monthly header and replace nested detail items."""
        items = validated_data.pop("items", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if items is not None:
            instance.items.all().delete()
            EntryMonthlyItem.objects.bulk_create([EntryMonthlyItem(entry=instance, **item) for item in items])
        return instance
