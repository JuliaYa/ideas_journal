from rest_framework import serializers

from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    main_picture = serializers.ImageField(required=False, allow_null=True, default=None)

    class Meta:
        model = Idea
        fields = '__all__'

    def to_internal_value(self, data):
        if 'main_picture' in data and data['main_picture'] == '':
            data = data.copy()
            data['main_picture'] = None
        return super().to_internal_value(data)
