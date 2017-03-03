from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from fetch_data import models as fetch_data_models
import models as fsm_models
import serializers

# Create your views here.

class IntrusionDetail(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            morcha = fetch_data_models.Morcha.objects.get(uuid=pk)
        except ObjectDoesNotExist as e:
            return Response('detail not found', status=status.HTTP_400_BAD_REQUEST)
        intrusions = fsm_models.newIntrusion.objects.filter(morcha=pk)
        latest = intrusions.order_by('-start_time')[:3]

        return JsonResponse({
            'total': intrusions.count(),
            'recent': serializers.newIntrusionSerializer(latest, many=True).data
        })


