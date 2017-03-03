from rest_framework import serializers
from fetch_data.models import *


class GeospaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geospace
        fields = ('latitude', 'longitude')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('repr')


class MorchaSerializer(serializers.ModelSerializer):
    geospace = GeospaceSerializer()
    devices = DeviceSerializer(many=True)

    class Meta:
        model = Morcha
        fields = ('name', 'geospace', 'uuid')


class MorchaNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Morcha
        fields = ('name', 'uuid')


class PostMorchaSerializer(serializers.ModelSerializer):
    morchas = MorchaNameSerializer(many=True, read_only=True)
    geospace = GeospaceSerializer()

    class Meta:
        model = Post
        fields = ('name', 'geospace', 'uuid', 'morchas', )


class PostNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('name', 'uuid')


class BattalionSerializer(serializers.ModelSerializer):
    geospace = GeospaceSerializer()
    posts = PostNameSerializer(many=True)

    class Meta:
        model = Morcha
        fields = ('name', 'geospace', 'uuid', 'posts')


class IntrusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intrusion
        fields = ('detected_datetime', 'verified_datetime', 'neutralized_datetime',
                  'non_human_intrusion_datetime', 'duration')


class MorchaPostNameSerializer(serializers.ModelSerializer):
    post = PostNameSerializer()

    class Meta:
        model = Morcha
        fields = ('name', 'uuid', 'post')


class LongestIntrusionSerializer(serializers.ModelSerializer):
    morcha = MorchaPostNameSerializer()

    class Meta:
        model = Intrusion
        fields = ('detected_datetime', 'verified_datetime', 'neutralized_datetime',
                  'non_human_intrusion_datetime', 'duration', 'morcha')


class WeaksignalSerializer(serializers.ModelSerializer):
    unit = DeviceSerializer()

    class Meta:
        model = Weaksignal
        fields = ('unit', 'start', 'end')


class OfflineSerializer(serializers.ModelSerializer):
    unit = DeviceSerializer()

    class Meta:
        model = Offline
        fields = ('unit', 'start', 'end', 'duration')


class BackupSerializer(serializers.ModelSerializer):
    unit = DeviceSerializer()

    class Meta:
        model = Backup
        fields = ('unit', 'start', 'end', 'duration')
