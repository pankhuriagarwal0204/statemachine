from django.conf.urls import url
from archives import view_reports as unit_report

urlpatterns = [
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/day/(?P<date>\d{4}-\d{2}-\d{2})/$', unit_report.MorchaDayView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$', unit_report.MorchaWeekView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$', unit_report.MorchaMonthView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/day/(?P<date>\d{4}-\d{2}-\d{2})/$', unit_report.PostDayView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$', unit_report.PostWeekView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$', unit_report.PostMonthView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/live/$', unit_report.PostLiveView.as_view({
        'get': 'retrieve'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/live/$', unit_report.BattalionLiveView.as_view({
        'get': 'retrieve'
    })),
    url(r'^bms/(?P<pk>[0-9a-z-]+)/$', unit_report.bms_demo.as_view({
        'get': 'retrieve'
    }))
]