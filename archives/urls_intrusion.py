from django.conf.urls import url
from archives import views as api_views


urlpatterns = [
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/all/$', api_views.MorchaAllView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/day/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.MorchaDayView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.MorchaWeekView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.MorchaMonthView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/recent/$', api_views.PostRecentView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/day/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.PostDayView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.PostWeekView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.PostMonthView.as_view({
        'get': 'retrieve'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/recent/$', api_views.BattalionRecentView.as_view({
        'get': 'retrieve'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$',
        api_views.BattalionWeekView.as_view({
            'get': 'retrieve'
        })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$',
        api_views.BattalionMonthView.as_view({
            'get': 'retrieve'
        })),
    url(r'^dashboard/battalion/$', api_views.BattalionDashboardView.as_view({
        'get': 'retrieve'
    }))
]
