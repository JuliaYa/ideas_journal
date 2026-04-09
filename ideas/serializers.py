from rest_framework import serializers

from .models import Idea, NoteEntry, NoteImage


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


class NoteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteImage
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class NoteEntrySerializer(serializers.ModelSerializer):
    images = NoteImageSerializer(many=True, read_only=True)

    class Meta:
        model = NoteEntry
        fields = [
            'id',
            'idea',
            'note_type',
            'text',
            'audio_file',
            'transcription',
            'images',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'idea', 'transcription', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context['request']
        note = NoteEntry.objects.create(**validated_data)
        images = request.FILES.getlist('images')
        for img in images:
            NoteImage.objects.create(note=note, image=img)
        return note
