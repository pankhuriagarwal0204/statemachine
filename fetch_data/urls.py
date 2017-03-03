from django.conf.urls import url
from fetch_data import views

urlpatterns = [
    url(r'morchas/$', views.fetch_morchas),
    url(r'morchas/(?P<morcha_id>[0-9a-f-]+)/$', views.fetch_intruded_morcha_details),
    url(r'all-online/$', views.all_online),
    url(r'one-offline/$', views.one_offline),
    url(r'neutralize-intrusion/laser/$', views.neutralize_intrusion_laser),
    url(r'neutralize-intrusion/infrared/$', views.neutralize_intrusion_infrared),
    url(r'verify-intrusion/laser/$', views.verify_intrusion_laser),
    url(r'verify-intrusion/infrared/$', views.verify_intrusion_infrared),
    url(r'detect-intrusion/laser/$', views.detect_intrusion_laser),
    url(r'detect-intrusion/infrared/$', views.detect_intrusion_infrared),
    url(r'delete-intrusions/$', views.delete_intrusions),
    url(r'remote/$', views.remote),
]