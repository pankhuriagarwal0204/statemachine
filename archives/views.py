import pytz
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from fetch_data import models
import serializers
import datetime
import calendar_utils
from widget_processors import Widgets
import json


def TruthView(request):
    events = models.Event.objects.all().order_by('-id')
    return render(request, 'truthview.html', {'events': events})


def MirrorView(request):
    events = models.Event.objects.all().order_by('-id')
    return render(request, 'mirrorview.html', {'events': events})


class BattalionView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Battalion.objects.all()
    serializer_class = serializers.BattalionSerializer


class PostView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostMorchaSerializer


class MorchaView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Morcha.objects.all()
    serializer_class = serializers.MorchaSerializer


class MorchaDayView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='day', pk=pk, level='morcha')
        error, message = self.widgets.check_object_exists()
        if error:
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return JsonResponse({
                'count': self.widgets.total_count(),
                'intrusions': self.widgets.get_intrusion_report(),
                'area_secure': self.widgets.get_security_update()
            })


class MorchaWeekView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='week', pk=pk, level='morcha')
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'longest_intrusion': self.widgets.longest_intrusion(),
                'count': self.widgets.total_count(),
                'report': self.widgets.get_intrusion_report()
            })


class MorchaMonthView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='month', pk=pk, level='morcha')
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'longest_intrusion': self.widgets.longest_intrusion(),
                'count': self.widgets.total_count(),
                'report': self.widgets.get_intrusion_report(),
            })


class MorchaAllView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        morcha_instance = get_object_or_404(models.Morcha, pk=pk)
        morcha_intrusions = models.Intrusion.objects.filter(morcha=pk)
        verified_intrusions = morcha_intrusions.filter(verified_datetime__isnull=False)
        neutralized_intrusions = morcha_intrusions.filter(neutralized_datetime__isnull=False)
        non_human_intrusions = morcha_intrusions.filter(non_human_intrusion_datetime__isnull=False)
        recent = verified_intrusions | neutralized_intrusions | non_human_intrusions
        recent_intrusion = recent.extra(
            select={'confirmed_time': 'greatest(verified_datetime, detected_datetime, neutralized_datetime)'}).order_by(
            '-confirmed_time').first()
        if recent_intrusion:
            data = recent_intrusion.confirmed_time
        else:
            data = None
        print data
        return Response({
            'total': 0,
            'recent': data
        })


class PostDayView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='day', pk=pk, level='post')
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'report': self.widgets.get_intrusion_report()
            })


class PostWeekView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='week', level='post', pk=pk)
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({
                'count': self.widgets.total_count(),
                'longest': self.widgets.longest_intrusion(),
                'vulnerable': list(self.widgets.get_vulnerable_morcha()),
                'report': self.widgets.get_intrusion_report()
            })


class PostMonthView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='month', level='post', pk=pk)
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({
                'count': self.widgets.total_count(),
                'longest': self.widgets.longest_intrusion(),
                'vulnerable': list(self.widgets.get_vulnerable_morcha()),
                'report': self.widgets.get_intrusion_report()
            })


class PostRecentView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        self.widgets = Widgets(timespan='recent', level='post', pk=pk)
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'recent': self.widgets.get_intrusion_report(),
                'vulnerable': self.widgets.get_vulnerable_morcha(),
                'hour': self.widgets.get_hypersensitive_hour()
            })


class PostRecentStatus(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        post_instance = get_object_or_404(models.Post, pk=pk)
        morcha_set = post_instance.morchas.all()
        res = {}
        for morcha in morcha_set:
            device_set = morcha.devices.all()
            res[morcha.name] = []
            for device in device_set:
                if not device.active:
                    res[morcha.name].append(device.repr)

        return Response(res)


class BattalionRecentView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        self.widgets = Widgets(timespan='recent', level='battalion', pk=pk)
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'vulnerable': self.widgets.get_vulnerable_post(),
                'recent': self.widgets.get_intrusion_report()
            })


class BattalionWeekView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='week', level='battalion', pk=pk)
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'count': self.widgets.total_count(),
                'longest': self.widgets.longest_intrusion(),
                'vulnerable': self.widgets.get_vulnerable_post(),
                'report': self.widgets.get_intrusion_report()
            })


class BattalionMonthView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='month', level='battalion', pk=pk)
        error, message = self.widgets.check_object_exists()
        if error:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'count': self.widgets.total_count(),
                'longest': self.widgets.longest_intrusion(),
                'vulnerable': self.widgets.get_vulnerable_post(),
                'report': self.widgets.get_intrusion_report()
            })


class BattalionDashboardView(viewsets.ViewSet):
    def retrieve(self, request):
        self.calendar = calendar_utils.calendar_iterators()
        start, end = self.calendar.lastmonthstartend()
        battalions = models.Battalion.objects.all()
        obj = {}
        for battalion in battalions:
            data = {}
            data['battalion_name'] = battalion.name
            posts = battalion.posts.all()
            data['post_count'] = posts.count()
            morcha_count = 0
            for post in posts:
                morcha_count += post.morchas.count()
            data['morcha_count'] = morcha_count
            pk = battalion.uuid
            data['intrusions'] = models.Intrusion.objects.filter(morcha__post__battalion = pk).\
                exclude(verified_datetime__isnull=True, neutralized_datetime__isnull=True,
                        non_human_intrusion_datetime__isnull=True).count()
            obj[str(pk)] = data
        return Response(obj)


def insert(request):
    morcha_instance = models.Morcha.objects.get(name='morcha3')
    post_instance = models.Post.objects.get(name=morcha_instance.post)
    print post_instance
    obj = calendar_utils.calendar_iterators()
    counter = 1
    # date = datetime.datetime(2017, 1, 2).replace(tzinfo=pytz.UTC)
    for date in obj.lastmonthiterator('2017-02-01'):
        print date.tzinfo
        data = models.Intrusion()
        data.morcha = morcha_instance
        data.post = post_instance
        data.detected_datetime = date
        newdate = date + datetime.timedelta(hours=2, minutes=10)
        data.verified_datetime = newdate

        if (counter < 6):
            data.non_human_intrusion_datetime = newdate

        if (counter == 10 or counter == 15):
            data.neutralized_datetime = newdate + datetime.timedelta(days=1)
        elif (counter == 11):
            pass
        else:
            data.neutralized_datetime = newdate + datetime.timedelta(hours=2, minutes=10)
        data.duration = 2000.0
        data.save()
        counter += 1


def test(request):
    return Response("nothing :P !!")
