from rest_framework import serializers
import models as fsm_models

class newIntrusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = fsm_models.newIntrusion
        fields = ('start_time', 'end_time', 'attempts')