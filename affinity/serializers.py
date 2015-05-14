from rest_framework import serializers


class BrandSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=256)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)


class ProfileSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
