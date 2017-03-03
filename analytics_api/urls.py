from django.conf.urls import url, include
from django.contrib import admin
from archives import views as api_views
from archives import view_reports as unit_report
from fetch_data import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^truth/$', api_views.TruthView),
    url(r'^truth-mirror/$', api_views.MirrorView),
    url(r'^battalion/$', api_views.BattalionView.as_view({
        'get': 'list'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/$', api_views.BattalionView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/$', api_views.PostView.as_view({
        'get': 'list'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/$', api_views.PostView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/$', api_views.MorchaView.as_view({
        'get': 'retrieve'
    })),
    url(r'^intrusion/', include('archives.urls_intrusion')),
    url(r'^unit/post/(?P<pk>[0-9a-z-]+)/status/$', api_views.PostRecentStatus.as_view({
        'get': 'retrieve'
    })),
    url(r'^unit/', include('archives.urls_unit')),
    url(r'^', include('fetch_data.urls'), name='home'),
    url(r'^insert/$', api_views.insert),
    url(r'^test/$', api_views.test)
]
