from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/$', IntrusionDetail.as_view({
        'get': 'retrieve'
    })),
]